#!/usr/bin/env python3
"""Validate the authored LMS catalogs and build deterministic contract references."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from validate_components import validate_component_map
from validate_scopes import validate_scope_registry

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'specification'
GENERATED = ROOT / 'reference'
SCHEMA_URI = 'https://json-schema.org/draft/2020-12/schema'
COLLECTIONS = ('entities', 'commands', 'events', 'permissions', 'scenarios')


def load_catalogs():
    result = []
    for path in sorted(SPEC.glob('*/catalog.json')):
        with path.open(encoding='utf-8') as source:
            result.append((path, json.load(source)))
    return result


def schema_for_entity(entity):
    properties = {}
    required = []
    for field in entity['fields']:
        schema = copy.deepcopy(field['schema'])
        if field['nullable']:
            schema = {'anyOf': [schema, {'type': 'null'}]}
        schema['description'] = field['description']
        if field.get('references'):
            schema['x-entity-reference'] = field['references']
            schema['x-reference-scope'] = field.get('reference_scope', '')
        properties[field['name']] = schema
        if field['required']:
            required.append(field['name'])
    return {
        '$schema': SCHEMA_URI,
        'title': entity['name'],
        'description': entity['description'],
        'type': 'object',
        'properties': properties,
        'required': required,
        'additionalProperties': False,
        'x-owner': entity['owner'],
        'x-unique-keys': entity['unique_keys'],
        'x-invariants': entity['invariants'],
    }


def validate(catalogs):
    errors = []
    if not catalogs:
        return ['No authored catalogs were found.']
    registries = {key: {} for key in COLLECTIONS}
    domains = set()
    catalog_schema = json.loads((ROOT / 'tooling' / 'catalog.schema.json').read_text())
    catalog_validator = Draft202012Validator(catalog_schema)
    for path, catalog in catalogs:
        for error in catalog_validator.iter_errors(catalog):
            errors.append(f'{path} at {list(error.absolute_path)}: {error.message}')
        domain = catalog.get('domain')
        if not domain or domain in domains:
            errors.append(f'{path}: missing or duplicate domain {domain!r}')
        domains.add(domain)
        if catalog.get('catalog_version') != '1.0.0':
            errors.append(f'{path}: unsupported catalog version')
        for collection in COLLECTIONS:
            values = catalog.get(collection)
            if not isinstance(values, list):
                errors.append(f'{path}: {collection} must be an array')
                continue
            key = 'key' if collection == 'permissions' else 'id' if collection == 'scenarios' else 'name'
            for value in values:
                name = value.get(key)
                if not name or name in registries[collection]:
                    errors.append(f'{path}: missing or duplicate {collection} identifier {name!r}')
                registries[collection][name] = (domain, value)
    if errors:
        return errors
    routes = set()
    for domain, entity in registries['entities'].values():
        name = entity['name']
        fields = entity.get('fields', [])
        names = [field['name'] for field in fields]
        if len(names) != len(set(names)):
            errors.append(f'{name}: duplicate field name')
        if entity.get('identity') not in names:
            errors.append(f'{name}: identity does not name a field')
        for required in ('description', 'owner', 'unique_keys', 'indexes', 'invariants', 'retention'):
            if not entity.get(required):
                errors.append(f'{name}: missing {required}')
        for field in fields:
            label = f"{name}.{field['name']}"
            for required in ('schema', 'required', 'nullable', 'description'):
                if required not in field:
                    errors.append(f'{label}: missing {required}')
            target = field.get('references')
            if target and target not in registries['entities']:
                errors.append(f'{label}: unresolved entity {target}')
            if target and not field.get('reference_scope'):
                errors.append(f'{label}: missing reference scope')
            try:
                Draft202012Validator.check_schema(field.get('schema', {}))
            except Exception as exc:
                errors.append(f'{label}: invalid schema {exc}')
        for key in entity.get('unique_keys', []):
            for field in key:
                if field not in names:
                    errors.append(f'{name}: unique key references absent field {field}')
        for index in entity.get('indexes', []):
            for field in index['fields']:
                if field not in names:
                    errors.append(f'{name}: index references absent field {field}')
        states = entity.get('states', [])
        for transition in entity.get('transitions', []):
            for side in ('from', 'to'):
                if transition[side] not in states:
                    errors.append(f"{name}: transition {side}={transition[side]} is absent from states")
            command = transition.get('command')
            if command and command not in registries['commands']:
                errors.append(f'{name}: transition references absent command {command}')
        try:
            Draft202012Validator.check_schema(schema_for_entity(entity))
        except Exception as exc:
            errors.append(f'{name}: generated entity schema failed {exc}')
    for domain, command in registries['commands'].values():
        name = command['name']
        route = (command.get('method'), re.sub(r'\{[^}]+\}', '{}', command.get('path', '')))
        if route in routes:
            errors.append(f'{name}: duplicate route {route}')
        routes.add(route)
        for field, location in command.get('parameter_locations', {}).items():
            if field not in command['request_schema'].get('properties', {}):
                errors.append(f'{name}: parameter location names absent field {field}')
        if command.get('permission') not in registries['permissions']:
            errors.append(f"{name}: unresolved permission {command.get('permission')}")
        for schema_key in ('request_schema', 'response_schema'):
            try:
                Draft202012Validator.check_schema(command[schema_key])
                for instance in command.get(schema_key.replace('_schema', '_examples'), []):
                    Draft202012Validator(command[schema_key], format_checker=FormatChecker()).validate(instance)
            except Exception as exc:
                errors.append(f'{name}.{schema_key}: {exc}')
        if command.get('idempotency') not in ('required', 'optional', 'none'):
            errors.append(f'{name}: unsupported idempotency value')
        for event in command.get('events', []):
            if event not in registries['events']:
                errors.append(f'{name}: unresolved event {event}')
        for error in command.get('errors', []):
            if not all(key in error for key in ('status', 'code', 'condition', 'recovery')):
                errors.append(f'{name}: error missing required detail')
    for domain, event in registries['events'].values():
        try:
            Draft202012Validator.check_schema(event['payload_schema'])
        except Exception as exc:
            errors.append(f"{event['name']}: invalid event schema {exc}")
    coverage_targets = set(registries['entities']) | set(registries['commands']) | set(registries['events']) | set(registries['permissions'])
    for domain, scenario in registries['scenarios'].values():
        for target in scenario.get('covers', []):
            if target not in coverage_targets:
                errors.append(f"{scenario['id']}: unresolved coverage target {target}")
        for phase in ('given', 'when', 'then'):
            if not scenario.get(phase):
                errors.append(f"{scenario['id']}: missing {phase}")
    covered_commands = {target for domain, scenario in registries['scenarios'].values() for target in scenario['covers']}
    for name in registries['commands']:
        if name not in covered_commands:
            errors.append(f'{name}: no authored acceptance scenario covers this operation')
    for path in SPEC.rglob('*.schema.json'):
        try:
            Draft202012Validator.check_schema(json.loads(path.read_text()))
        except Exception as exc:
            errors.append(f'{path}: invalid standalone schema {exc}')
    return errors


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def markdown_value(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def entity_reference(entity, domain):
    lines = [f"# {entity['name']}", '', entity['description'], '', f"Owned by **{domain}**.", '', '## Fields', '']
    for field in entity['fields']:
        presence = 'Required' if field['required'] else 'Optional'
        nullability = 'Nullable' if field['nullable'] else 'Null is rejected'
        lines += [f"### {field['name']}", '', field['description'], '', f'{presence}. {nullability}.', '']
        if field.get('references'):
            lines += [f"References [{field['references']}]({field['references']}.md). {field['reference_scope']}", '']
        lines += ['```json', json.dumps(field['schema'], ensure_ascii=False, indent=2), '```', '']
    lines += ['## Integrity', '']
    lines += [f'- {rule}' for rule in entity['invariants']]
    lines += ['', '## Unique keys', '']
    lines += ['- `' + ', '.join(key) + '`' for key in entity['unique_keys']]
    lines += ['', '## Query indexes', '', '| Fields | Query purpose |', '| --- | --- |']
    for index in entity['indexes']:
        lines.append(f"| {', '.join(index['fields'])} | {markdown_value(index['purpose'])} |")
    lines += ['', '## Retention', '', entity['retention'], '']
    if entity.get('transitions'):
        lines += ['## Transitions', '', '| From | To | Command | Guard and effects |', '| --- | --- | --- | --- |']
        for transition in entity['transitions']:
            lines.append('| ' + ' | '.join(markdown_value(value) for value in [transition['from'], transition['to'], transition['command'], transition['guard'] + ' ' + ' '.join(transition['effects'])]) + ' |')
        lines.append('')
    return '\n'.join(lines)


def build_openapi(catalogs):
    field_error = {
        'type': 'object',
        'required': ['pointer', 'code'],
        'properties': {
            'pointer': {'type': 'string'},
            'code': {'type': 'string'},
            'message': {'type': 'string'},
        },
        'additionalProperties': False,
    }
    problem = {
        'type': 'object',
        'required': ['type', 'title', 'status', 'code', 'request_id'],
        'properties': {
            'type': {'type': 'string', 'format': 'uri-reference'},
            'title': {'type': 'string'},
            'status': {'type': 'integer', 'minimum': 400, 'maximum': 599},
            'code': {'type': 'string'},
            'detail': {'type': 'string'},
            'request_id': {'type': 'string', 'format': 'uuid'},
            'errors': {'type': 'array', 'items': field_error},
        },
        'additionalProperties': False,
    }
    result = {
        'openapi': '3.1.1',
        'info': {
            'title': 'Learning management domain API contracts',
            'version': '1.0.0',
            'description': (
                'Proposed owner command contracts generated from the reviewed catalogs. '
                'Dedicated standards wire handlers follow the adapter profiles and invoke '
                'these commands after authenticating and normalizing the external request.'
            ),
        },
        'jsonSchemaDialect': SCHEMA_URI,
        'security': [{'bearerAuth': []}],
        'paths': {},
        'components': {
            'securitySchemes': {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'description': (
                        'Provider-neutral service authentication. Host session adapters '
                        'enforce equivalent object scopes and anti-forgery controls.'
                    ),
                },
            },
            'schemas': {'Problem': problem},
        },
    }
    common_errors = {
        400: 'The protocol envelope is invalid.',
        401: 'Authentication is missing or expired.',
        403: 'The actor lacks an applicable permission.',
        404: 'The authorized target cannot be resolved.',
        409: 'The request conflicts with authoritative state or its prior receipt.',
        422: 'The payload violates a schema or business invariant.',
        429: 'The scoped workload limit was reached. Honor the retry time.',
        503: 'The owner cannot acknowledge durability. Query the receipt before replaying.',
    }
    for path, catalog in catalogs:
        result['components']['securitySchemes'].update(catalog.get('security_schemes', {}))
        for command in catalog['commands']:
            success = {'description': 'The specified authoritative result is available.'}
            if command['success_status'] == 202:
                success['description'] = 'Durable work was accepted. Completion remains asynchronous.'
            if command['success_status'] != 204:
                media = {'schema': command['response_schema']}
                if command.get('response_examples'):
                    media['examples'] = {
                        f'case-{index + 1}': {'value': example}
                        for index, example in enumerate(command['response_examples'])
                    }
                success['content'] = {'application/json': media}
            response_fields = command['response_schema'].get('properties', {})
            if 'if-match' in command['concurrency'].lower() or 'version' in response_fields:
                success['headers'] = {'ETag': {'description': 'Opaque strong revision tag for the authorized owner representation. Supply it unchanged to If-Match on the guarded mutation.', 'schema': {'type': 'string', 'minLength': 3, 'maxLength': 256}}}
            if command.get('response_headers'):
                success.setdefault('headers', {}).update(command['response_headers'])
            parameters = []
            path_fields = set(re.findall(r'\{([^{}]+)\}', command['path']))
            request_schema = copy.deepcopy(command['request_schema'])
            request_fields = request_schema.get('properties', {})
            required = request_schema.get('required', [])
            extracted_fields = set()
            for field in sorted(path_fields):
                default_schema = {'type': 'string', 'minLength': 1}
                if field.endswith('_id'):
                    default_schema = {'type': 'string', 'format': 'uuid'}
                parameters.append({
                    'name': field,
                    'in': 'path',
                    'required': True,
                    'schema': request_fields.get(field, default_schema),
                })
            for field, location in command.get('parameter_locations', {}).items():
                parameters.append({
                    'name': location['name'],
                    'in': location['in'],
                    'required': field in required,
                    'schema': request_fields[field],
                })
                extracted_fields.add(field)
            if command['idempotency'] != 'none':
                parameters.append({
                    'name': 'Idempotency-Key',
                    'in': 'header',
                    'required': command['idempotency'] == 'required',
                    'schema': {'type': 'string', 'minLength': 16, 'maxLength': 128},
                    'description': 'Opaque request key scoped to institution, actor, operation and payload.',
                })
            if 'if-match' in command['concurrency'].lower():
                parameters.append({
                    'name': 'If-Match',
                    'in': 'header',
                    'required': True,
                    'schema': {'type': 'string', 'minLength': 1, 'maxLength': 256},
                    'description': 'Strong owner-issued revision tag from the current authorized resource.',
                })
            operation = {
                'operationId': command['name'],
                'tags': [catalog['domain']],
                'description': command['description'],
                'parameters': parameters,
                'responses': {str(command['success_status']): success},
                'x-permission': command['permission'],
                'x-concurrency': command['concurrency'],
                'x-preconditions': command['preconditions'],
                'x-transaction': command['transaction'],
                'x-events': command['events'],
            }
            if 'security' in command:
                operation['security'] = command['security']
            if command['method'] in ('GET', 'HEAD'):
                for name, schema in request_fields.items():
                    if name in path_fields or name in extracted_fields:
                        continue
                    parameter = {
                        'name': name,
                        'in': 'query',
                        'required': name in required,
                        'schema': schema,
                    }
                    if schema.get('type') == 'object':
                        parameter.update({'style': 'deepObject', 'explode': True})
                    parameters.append(parameter)
            else:
                for name in extracted_fields:
                    request_fields.pop(name, None)
                request_schema['required'] = [name for name in required if name not in extracted_fields]
                media = {'schema': request_schema}
                if command.get('request_examples'):
                    media['examples'] = {
                        f'case-{index + 1}': {
                            'value': {key: value for key, value in example.items() if key not in extracted_fields}
                        }
                        for index, example in enumerate(command['request_examples'])
                    }
                operation['requestBody'] = {
                    'required': True,
                    'content': {'application/json': media},
                }
            statuses = set(common_errors) | {error['status'] for error in command['errors']}
            for status in sorted(statuses):
                errors = [error for error in command['errors'] if error['status'] == status]
                description = ' '.join(error['condition'] + ' ' + error['recovery'] for error in errors)
                response = {
                    'description': description or common_errors[status],
                    'content': {
                        'application/problem+json': {'schema': {'$ref': '#/components/schemas/Problem'}},
                    },
                }
                if errors:
                    response['x-domain-errors'] = errors
                operation['responses'][str(status)] = response
            result['paths'].setdefault(command['path'], {})[command['method'].lower()] = operation
    return result

def build(catalogs, output_dir=GENERATED):
    expected = set()
    manifest_path = output_dir / 'manifest.json'
    previous_files = []
    if manifest_path.exists():
        previous_files = json.loads(manifest_path.read_text()).get('files', [])
    index = ['# Domain contract reference', '', 'This reference is generated from the authored catalogs in `specification/`. Edit the owning catalog and regenerate it with `python tooling/specification.py build`.', '', '| Domain | Records | Commands | Events | Permissions | Scenarios |', '| --- | --- | --- | --- | --- | --- |']
    for path, catalog in catalogs:
        domain = catalog['domain']
        index.append('| ' + ' | '.join([domain] + [str(len(catalog[key])) for key in COLLECTIONS]) + ' |')
        for entity in catalog['entities']:
            json_path = output_dir / 'entities' / (entity['name'] + '.schema.json')
            markdown_path = output_dir / 'entities' / (entity['name'] + '.md')
            write_json(json_path, schema_for_entity(entity))
            markdown_path.write_text(entity_reference(entity, domain), encoding='utf-8')
            expected.update((json_path, markdown_path))
        for event in catalog['events']:
            event_path = output_dir / 'events' / (event['name'] + '.schema.json')
            write_json(event_path, {'$schema': SCHEMA_URI, 'title': event['name'], 'description': event['description'], **event['payload_schema'], 'x-version': event['version'], 'x-producer': event['producer'], 'x-ordering': event['ordering'], 'x-deduplication': event['deduplication'], 'x-privacy': event['privacy']})
            expected.add(event_path)
        scenario_path = output_dir / 'scenarios' / (domain + '.md')
        lines = [f'# {domain.capitalize()} acceptance scenarios', '']
        for scenario in catalog['scenarios']:
            lines += [f"## {scenario['id']} — {scenario['title']}", '', 'Covers ' + ', '.join('`' + name + '`' for name in scenario['covers']) + '.', '']
            for phase in ('given', 'when', 'then'):
                lines += [f'### {phase.capitalize()}', ''] + ['- ' + step for step in scenario[phase]] + ['']
            if scenario.get('fixtures'):
                lines += ['### Fixture values', '', '```json', json.dumps(scenario['fixtures'], ensure_ascii=False, indent=2), '```', '']
        scenario_path.parent.mkdir(parents=True, exist_ok=True)
        scenario_path.write_text('\n'.join(lines), encoding='utf-8')
        expected.add(scenario_path)
    openapi_path = output_dir / 'openapi.json'
    write_json(openapi_path, build_openapi(catalogs))
    expected.add(openapi_path)
    index += ['', '## Entity dictionary', '']
    for path, catalog in catalogs:
        index += [f"### {catalog['domain'].capitalize()}", '']
        index += [f"- [{entity['name']}](entities/{entity['name']}.md)" for entity in catalog['entities']]
        index.append('')
    index += ['## Interface and test contracts', '', '- [OpenAPI description](openapi.json)', '']
    index += [f"- [{catalog['domain'].capitalize()} acceptance scenarios](scenarios/{catalog['domain']}.md)" for path, catalog in catalogs]
    index.append('')
    readme = output_dir / 'README.md'
    readme.write_text('\n'.join(index), encoding='utf-8')
    expected.add(readme)
    expected_paths = {path.resolve() for path in expected}
    for relative_path in previous_files:
        existing = (output_dir / relative_path).resolve()
        if not existing.is_relative_to(output_dir.resolve()):
            raise ValueError('Generated manifest contains a path outside its directory')
        if existing.is_file() and existing not in expected_paths:
            existing.unlink()
    write_json(manifest_path, {'generator': 'tooling/specification.py', 'files': sorted(str(path.relative_to(output_dir)) for path in expected)})
    counts = {key: sum(len(catalog[key]) for path, catalog in catalogs) for key in COLLECTIONS}
    print(json.dumps({'domains': len(catalogs), **counts, 'generated_files': len(expected)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('validate', 'build', 'check'))
    args = parser.parse_args()
    catalogs = load_catalogs()
    errors = validate(catalogs)
    if not errors:
        errors.extend(validate_component_map(ROOT))
        errors.extend(validate_scope_registry(ROOT))
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    if args.action == 'build':
        build(catalogs)
    elif args.action == 'check':
        with tempfile.TemporaryDirectory(prefix='lms-spec-check-') as temporary:
            expected_root = Path(temporary) / 'reference'
            build(catalogs, expected_root)
            differences = []
            for expected_file in expected_root.rglob('*'):
                if not expected_file.is_file():
                    continue
                relative_path = expected_file.relative_to(expected_root)
                actual_file = GENERATED / relative_path
                if not actual_file.exists() or actual_file.read_bytes() != expected_file.read_bytes():
                    differences.append(str(relative_path))
            if differences:
                print('Generated contracts differ from their authored source:', file=sys.stderr)
                print('\n'.join(differences), file=sys.stderr)
                return 1
            print('Generated contracts match the authored catalogs.')
    else:
        print(f'Validated {len(catalogs)} domain catalogs, schemas and cross-domain references.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
