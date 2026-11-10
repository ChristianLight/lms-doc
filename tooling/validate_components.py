"""Validate the Joomla component allocation against the authored domain catalogs."""

from __future__ import annotations

import json
import re
from collections import Counter
from graphlib import CycleError, TopologicalSorter
from itertools import chain
from pathlib import Path

VIEW_CODE = re.compile(r'[a-z]+(?:_[a-z]+)*')
COMPONENT_CODE = re.compile(r'com_lms[a-z]+')
COLUMN_CODE = re.compile(r'[a-z][a-z0-9_]*')
WORKSPACE_KEY = re.compile(r'[a-z][a-z0-9]*(?:[_-][a-z0-9]+)*')
CONTRACT_KEY = re.compile(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+')
RESERVED_COLUMNS = frozenset({
    'access', 'asset_id', 'checked_out', 'checked_out_time', 'created',
    'created_by', 'guid', 'hits', 'id', 'modified', 'modified_by',
    'ordering', 'published', 'version',
})


def _read_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        errors.append(f'{path}: {exc}')
        return {}
    if not isinstance(value, dict):
        errors.append(f'{path}: expected a JSON object')
        return {}
    return value


def _records(data: dict, key: str, label: str, errors: list[str]) -> list[dict]:
    values = data.get(key)
    if not isinstance(values, list):
        errors.append(f'{label}.{key}: expected an array of objects')
        return []
    if any(not isinstance(value, dict) for value in values):
        errors.append(f'{label}.{key}: each entry must be an object')
    return [value for value in values if isinstance(value, dict)]


def _strings(value: object, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f'{label}: expected an array of strings')
        return []
    return value


def _track(key: object, registry: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(key, str) or not key:
        errors.append(f'{label}: missing identifier')
    elif key in registry:
        errors.append(f'{label}: duplicate identifier {key}')
    else:
        registry.add(key)


def _require_text(data: dict, fields: tuple[str, ...], label: str, errors: list[str]) -> None:
    for field in fields:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f'{label}.{field}: expected nonempty text')


def _is_uuid(schema: object) -> bool:
    return isinstance(schema, dict) and schema.get('type') == 'string' and schema.get('format') == 'uuid'


def _known_values(value: object, known: set[str], label: str, errors: list[str]) -> set[str]:
    result: set[str] = set()
    for key in _strings(value, label, errors):
        _track(key, result, label, errors)
        if key not in known:
            errors.append(f'{label}: unknown identifier {key!r}')
    return result & known


def _version(value: object) -> bool:
    return type(value) is int and value > 0


def _check_workspaces(
    component: dict, workspace_entities: set[str], custom_routes: set[str], errors: list[str],
) -> None:
    code = component['code']
    workspace_keys: set[str] = set()
    admin_entries: set[str] = set()
    for workspace in _records(component, 'workspaces', code, errors):
        key = workspace.get('key')
        label = f'{code}.workspaces[{key!r}]'
        if not isinstance(key, str) or not WORKSPACE_KEY.fullmatch(key):
            errors.append(f'{label}: invalid workspace key')
        _track(key, workspace_keys, f'{code} workspace key', errors)
        _require_text(workspace, ('label', 'workflow', 'access'), label, errors)
        kind, entry = workspace.get('entry_kind'), workspace.get('entry')
        if not isinstance(entry, str) or not entry:
            errors.append(f'{label}: missing workspace entry')
        elif kind == 'admin_view':
            admin_entries.add(entry)
            if entry not in workspace_entities:
                errors.append(f'{label}: admin entry {entry} is not an attached workspace view here')
        elif kind == 'custom_admin_view':
            if entry not in custom_routes:
                errors.append(f'{label}: custom admin entry {entry} is not attached here')
        elif kind == 'site_view':
            if not VIEW_CODE.fullmatch(entry):
                errors.append(f'{label}: invalid site view route {entry!r}')
        else:
            errors.append(f'{label}: unsupported entry kind {kind!r}')
    if admin_entries != workspace_entities:
        errors.append(f'{code}: attached admin workspace views must match the declared admin entries')


def _required_providers(components: dict[str, dict], errors: list[str]) -> dict[str, set[str]]:
    provides: dict[tuple[str, str, int], int] = {}
    for code, component in components.items():
        for contract in _records(component, 'provided_contracts', code, errors):
            name, major, revision = (
                contract.get('contract'), contract.get('api_major'), contract.get('schema_revision'),
            )
            if not isinstance(name, str) or not CONTRACT_KEY.fullmatch(name) or not (
                _version(major) and _version(revision)
            ):
                errors.append(f'{code}: provider needs a contract key and positive API major and schema revision')
                continue
            key = (code, name, major)
            if key in provides:
                errors.append(f'{code}: duplicate provided contract {name} at API major {major}')
            else:
                provides[key] = revision

    required: dict[str, set[str]] = {code: set() for code in components}
    for code, component in components.items():
        seen: set[tuple[str, str, int]] = set()
        for dependency in _records(component, 'required_components', code, errors):
            provider = dependency.get('component')
            name = dependency.get('contract')
            major = dependency.get('api_major')
            minimum = dependency.get('minimum_schema_revision')
            _require_text(dependency, ('reason',), f'{code}.required_components', errors)
            if not isinstance(provider, str) or provider not in components:
                errors.append(f'{code}: required provider {provider!r} is absent from the package')
                continue
            if provider == code:
                errors.append(f'{code}: required component cannot depend on itself')
                continue
            required[code].add(provider)
            if not isinstance(name, str) or not CONTRACT_KEY.fullmatch(name) or not (
                _version(major) and _version(minimum)
            ):
                errors.append(f'{code}: required provider {provider} needs a contract key and positive API major and minimum schema revision')
                continue
            key = (provider, name, major)
            if key in seen:
                errors.append(f'{code}: duplicate required contract {name} at API major {major} from {provider}')
            seen.add(key)
            revision = provides.get(key)
            if revision is None:
                errors.append(f'{code}: required provider {provider} does not declare {name} at API major {major}')
            elif revision < minimum:
                errors.append(f'{code}: required provider {provider} declares {name} schema revision {revision}, below {minimum}')
    return required


def _install_graph(
    manifest: dict, required: dict[str, set[str]], errors: list[str],
) -> tuple[dict[str, tuple[str, str]], dict[tuple[str, str], set[tuple[str, str]]]]:
    # Use disjoint vertex types so a set key can never alias a component code.
    sets: dict[str, dict] = {}
    vertex_for = {code: ('component', code) for code in required}
    component_codes = set(required)
    for activation in _records(manifest, 'activation_sets', 'component map', errors):
        key = activation.get('key')
        if not isinstance(key, str) or not WORKSPACE_KEY.fullmatch(key):
            errors.append(f'Component allocation: invalid activation set key {key!r}')
            continue
        if key in sets:
            errors.append(f'Component allocation: duplicate activation set {key}')
            continue
        sets[key] = activation
        _require_text(activation, ('reason',), f'activation set {key}', errors)
        members = _known_values(activation.get('members'), component_codes, f'activation set {key} members', errors)
        if not members:
            errors.append(f'activation set {key}: no known member components')
        for code in sorted(members):
            if vertex_for[code][0] == 'set':
                errors.append(f'{code}: belongs to more than one activation set')
            else:
                vertex_for[code] = ('set', key)

    graph = {vertex: set() for vertex in sorted(set(vertex_for.values()) | {('set', key) for key in sets})}
    for code, providers in required.items():
        vertex = vertex_for[code]
        graph[vertex].update(vertex_for[provider] for provider in providers if vertex_for[provider] != vertex)
    for key, activation in sets.items():
        prerequisites = _known_values(activation.get('required_sets'), set(sets), f'activation set {key} required sets', errors)
        graph[('set', key)].update(('set', target) for target in prerequisites)
    return vertex_for, graph


def _check_dependencies(
    manifest: dict, components: dict[str, dict], provider_kinds: set[str], errors: list[str],
) -> None:
    component_codes = set(components)
    vertex_for, graph = _install_graph(manifest, _required_providers(components, errors), errors)
    feature_keys: set[str] = set()
    for feature in _records(manifest, 'feature_dependencies', 'component map', errors):
        key = feature.get('feature_key')
        label = f'feature dependency {key!r}'
        if not isinstance(key, str) or not WORKSPACE_KEY.fullmatch(key):
            errors.append(f'{label}: invalid feature key')
        _track(key, feature_keys, 'Feature key', errors)
        _require_text(feature, ('reason',), label, errors)
        _known_values(feature.get('required_components'), component_codes, f'{label} components', errors)
        _known_values(feature.get('provider_profile_kinds'), provider_kinds, f'{label} provider profile kinds', errors)

    host = manifest.get('host_requirements')
    if not isinstance(host, dict):
        errors.append('Component allocation: missing host requirements')
        host = {}
    if type(host.get('joomla_major')) is not int or host['joomla_major'] != 6:
        errors.append('Component allocation: host requirements must target Joomla 6')
    _require_text(host, ('php_version_policy',), 'host requirements', errors)
    library = host.get('shared_library')
    if not isinstance(library, str) or not re.fullmatch(r'lib_[a-z][a-z0-9_]*', library):
        errors.append('Component allocation: invalid shared library code')
    database_profiles: set[str] = set()
    for profile in _strings(host.get('database_profiles'), 'host database profiles', errors):
        _track(profile, database_profiles, 'Host database profile', errors)
    if not database_profiles:
        errors.append('Component allocation: declare a host database profile')
    bootstrap = _known_values(host.get('bootstrap_components'), component_codes, 'bootstrap components', errors)

    try:
        tuple(TopologicalSorter({vertex: sorted(prerequisites) for vertex, prerequisites in graph.items()}).static_order())
    except CycleError as exc:
        cycle = ' -> '.join(f'{kind} {key}' for kind, key in exc.args[1])
        errors.append(f'Component allocation: cyclic required installation plan: {cycle}')
        return

    bootstrap_vertices = {vertex_for[code] for code in bootstrap}
    pending = list(bootstrap_vertices)
    while pending:
        prerequisites = graph[pending.pop()] - bootstrap_vertices
        bootstrap_vertices.update(prerequisites)
        pending.extend(prerequisites)
    missing = {
        code for code, vertex in vertex_for.items() if vertex in bootstrap_vertices and code not in bootstrap
    }
    if missing:
        errors.append(f'Component allocation: bootstrap omits required components {", ".join(sorted(missing))}')


def validate_component_map(root: Path) -> list[str]:
    """Return structural, ownership and relationship errors for the design map."""
    errors: list[str] = []
    spec = root / 'specification'
    path = spec / 'joomla' / 'component-map.json'
    manifest = _read_json(path, errors)
    if errors:
        return errors

    entities: dict[str, tuple[str, dict]] = {}
    domains: set[str] = set()
    for path in sorted(spec.glob('*/catalog.json')):
        catalog = _read_json(path, errors)
        domain = catalog.get('domain')
        if not isinstance(domain, str) or not domain:
            errors.append(f'{path}: missing catalog domain')
            continue
        _track(domain, domains, str(path), errors)
        for record in _records(catalog, 'entities', domain, errors):
            name = record.get('name')
            if not isinstance(name, str) or not name:
                errors.append(f'{path}: entity has no name')
                continue
            if name in entities:
                errors.append(f'{path}: duplicate catalog entity {name}')
            if record.get('owner') != domain:
                errors.append(f'{name}: entity owner must match catalog domain {domain}')
            entities[name] = (domain, record)
    if not entities:
        errors.append('Component allocation: no persisted catalog entities found')
    if manifest.get('manifest_version') != '2.0.0':
        errors.append('Component allocation: unsupported manifest version')
    if 'component_admin_view_limit' in manifest:
        errors.append('Component allocation: remove the obsolete attachment limit from the manifest')
    policy = manifest.get('persistence_policy')
    if not isinstance(policy, dict):
        errors.append('Component allocation: missing persistence policy')
        policy = {}
    reserved = _strings(policy.get('reserved_generated_columns'), 'Generated reserved columns', errors)
    if set(reserved) != RESERVED_COLUMNS or len(reserved) != len(RESERVED_COLUMNS):
        errors.append('Component allocation: generated reserved columns do not match the physical mapping policy')
    if policy.get('reserved_domain_column_prefix') != 'lms_':
        errors.append('Component allocation: reserved domain column prefix must be lms_')
    if policy.get('application_id_column') != 'guid' or policy.get('local_joomla_primary_key') != 'id':
        errors.append('Component allocation: application GUID and Joomla local ID must use distinct physical columns')
    prefix_budget = policy.get('sql_prefix_budget')
    if type(prefix_budget) is not int or not 1 <= prefix_budget < 64:
        errors.append('Component allocation: SQL prefix budget must leave room within the 64-character identifier limit')
        prefix_budget = 12

    component_codes: set[str] = set()
    components_by_code: dict[str, dict] = {}
    definition_keys: set[str] = set()
    tables: set[str] = set()
    allocations: dict[str, str] = {}
    components = _records(manifest, 'components', 'component map', errors)
    component_counts: Counter[str] = Counter()
    admin_count = custom_count = maximum_attached = 0
    for component in components:
        code = component.get('code')
        if not isinstance(code, str) or not COMPONENT_CODE.fullmatch(code):
            errors.append(f'Component allocation: invalid component code {code!r}')
            continue
        _track(code, component_codes, 'Component code', errors)
        components_by_code.setdefault(code, component)
        _require_text(component, ('title', 'purpose', 'grouping_rationale', 'separation_boundary'), code, errors)
        if 'workspace_entity' in component:
            errors.append(f'{code}: declare workspaces in the workspaces array')
        domain = component.get('domain')
        if not isinstance(domain, str) or domain not in domains:
            errors.append(f'{code}: unknown catalog domain {domain!r}')
        else:
            component_counts[domain] += 1

        views = _records(component, 'admin_views', code, errors)
        custom_views = _records(component, 'custom_admin_views', code, errors)
        total_attached = len(views) + len(custom_views)
        admin_count += len(views)
        custom_count += len(custom_views)
        maximum_attached = max(maximum_attached, total_attached)
        route_codes = {code.removeprefix('com_')}
        workspace_entities: set[str] = set()
        custom_routes: set[str] = set()
        for view, custom in chain(((view, False) for view in views), ((view, True) for view in custom_views)):
            name = view.get('entity')
            label = f'{code}.{name or view.get("view_code", "custom view")}'
            _track(view.get('definition_key'), definition_keys, f'{label} definition key', errors)
            code_keys = ('view_code',) if custom else ('single_code', 'list_code')
            for key in code_keys:
                route = view.get(key)
                if not isinstance(route, str) or not VIEW_CODE.fullmatch(route):
                    errors.append(f'{label}: invalid {key} {route!r}')
                _track(route, route_codes, f'{code} route', errors)
            primary_code = view.get(code_keys[0])
            if view.get('definition_key') != f'{code}.{primary_code}':
                errors.append(f'{label}: definition key must be the component code and primary route')
            if custom:
                _require_text(view, ('purpose',), label, errors)
                if 'entity' in view or 'table' in view:
                    errors.append(f'{label}: a Custom Admin View cannot own a persisted entity or table')
                if isinstance(primary_code, str) and VIEW_CODE.fullmatch(primary_code):
                    custom_routes.add(primary_code)
                continue

            if not isinstance(name, str) or name not in entities:
                errors.append(f'{label}: unknown catalog entity')
                continue
            if name in allocations:
                errors.append(f'{label}: entity already allocated to {allocations[name]}')
            else:
                allocations[name] = code
            if entities[name][0] != domain:
                errors.append(f'{label}: owner domain is {entities[name][0]}, found {domain}')
            table = view.get('table')
            expected_table = f'#__{code.removeprefix("com_")}_{primary_code}'
            if table != expected_table:
                errors.append(f'{label}: table must match {expected_table}')
            elif len(table) - len('#__') + prefix_budget > 64:
                errors.append(f'{label}: table exceeds the SQL identifier limit with the declared prefix budget')
            _track(table, tables, f'{label} table', errors)
            visibility = view.get('visibility')
            if visibility == 'workspace':
                workspace_entities.add(name)
            elif visibility != 'internal':
                errors.append(f'{label}: unsupported visibility {visibility!r}')

        _check_workspaces(component, workspace_entities, custom_routes, errors)

    missing = sorted(set(entities) - allocations.keys())
    if missing:
        errors.append(f'Component allocation: missing entities {", ".join(missing)}')

    entity_targets = {}
    for name, (_, record) in entities.items():
        targets = set()
        columns: set[str] = set()
        fields = _records(record, 'fields', name, errors)
        identity = record.get('identity')
        unique_keys = record.get('unique_keys')
        identity_fields = [field for field in fields if field.get('name') == identity]
        if (
            not isinstance(identity, str) or len(identity_fields) != 1
            or not _is_uuid(identity_fields[0].get('schema'))
            or identity_fields[0].get('required') is not True
            or identity_fields[0].get('nullable') is not False
            or not isinstance(unique_keys, list) or [identity] not in unique_keys
        ):
            errors.append(f'{name}: application identity must be a required, non-null, independently unique UUID')
        for field in fields:
            logical = field.get('name')
            if isinstance(logical, str):
                physical = logical
                if logical == identity:
                    physical = 'guid'
                elif logical in RESERVED_COLUMNS:
                    physical = 'lms_' + logical
                if not COLUMN_CODE.fullmatch(physical) or len(physical) > 64:
                    errors.append(f'{name}.{logical}: invalid physical column {physical!r}')
                _track(physical, columns, f'{name}.{logical} physical column', errors)
            target = field.get('references')
            if target is None:
                continue
            schema = field.get('schema')
            if not _is_uuid(schema) and not (
                isinstance(schema, dict) and schema.get('type') == 'array' and _is_uuid(schema.get('items'))
            ):
                errors.append(f'{name}.{logical}: mapped reference must contain a UUID or UUID array')
            _require_text(field, ('reference_scope',), f'{name}.{logical}', errors)
            if not isinstance(target, str) or target not in allocations:
                errors.append(f'{name}.{field.get("name")}: no mapped owner for reference {target!r}')
            else:
                targets.add(target)
        entity_targets[name] = targets

    for component in components:
        code = component.get('code')
        if not isinstance(code, str) or code not in component_codes:
            continue
        owned_names = {name for name, owner in allocations.items() if owner == code}
        expected_refs = {
            allocations[target]
            for name in owned_names
            for target in entity_targets[name]
            if allocations[target] != code
        }
        declared_refs = _strings(component.get('referenced_components'), f'{code}.referenced_components', errors)
        if sorted(declared_refs) != sorted(expected_refs):
            errors.append(f'{code}: referenced components do not match catalog links, expected {", ".join(sorted(expected_refs))}')

        seen_pairs: set[tuple[str, str]] = set()
        for group in _records(component, 'normalized_edit_groups', code, errors):
            parent = group.get('parent_entity')
            if not isinstance(parent, str) or parent not in owned_names:
                errors.append(f'{code}: normalized editor parent {parent!r} is not attached here')
                continue
            children = _strings(group.get('child_entities'), f'{code}.{parent}.child_entities', errors)
            if not children or group.get('mutation_authority') != 'owner_command':
                errors.append(f'{code}.{parent}: normalized group needs attached children and owner-command authority')
            for child in children:
                pair = (parent, child)
                if pair in seen_pairs:
                    errors.append(f'{code}: duplicate normalized edit link {parent} to {child}')
                seen_pairs.add(pair)
                if child == parent or child not in owned_names:
                    errors.append(f'{code}: normalized child {child} is not a separate attached table here')
                elif not any(
                    field.get('references') == parent
                    and _is_uuid(field.get('schema'))
                    for field in _records(entities[child][1], 'fields', child, errors)
                ):
                    errors.append(f'{code}: normalized child {child} lacks a typed parent reference to {parent}')

    entity_counts = Counter(domain for domain, _ in entities.values())
    expected_counts = {
        'domains': len(domains),
        'components': len(components),
        'persisted_entities': len(entities),
        'admin_view_definitions': admin_count,
        'custom_admin_view_definitions': custom_count,
        'maximum_attached_per_component': maximum_attached,
        'by_domain': {
            domain: {'components': component_counts[domain], 'entities': entity_counts[domain]}
            for domain in sorted(domains)
        },
    }
    if manifest.get('counts') != expected_counts:
        errors.append('Component allocation: published count summary disagrees with verified definitions')

    provider_kinds: set[str] = set()
    if 'IntegrationConnection' in entities:
        _, connection = entities['IntegrationConnection']
        for field in _records(connection, 'fields', 'IntegrationConnection', errors):
            if field.get('name') == 'provider_kind' and isinstance(field.get('schema'), dict):
                provider_kinds = set(_strings(field['schema'].get('enum'), 'IntegrationConnection provider kinds', errors))
    _check_dependencies(manifest, components_by_code, provider_kinds, errors)
    return errors
