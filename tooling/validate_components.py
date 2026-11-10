"""Validate the Joomla component allocation against the authored domain catalogs."""

from __future__ import annotations

import json
import re
from collections import Counter
from itertools import chain
from pathlib import Path

VIEW_CODE = re.compile(r'[a-z]+(?:_[a-z]+)*')
COMPONENT_CODE = re.compile(r'com_lms[a-z]+')
VIEW_LIMIT = 5
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
    if manifest.get('manifest_version') != '1.0.0':
        errors.append('Component allocation: unsupported manifest version')
    if manifest.get('component_admin_view_limit') != VIEW_LIMIT:
        errors.append(f'Component allocation: hard limit is {VIEW_LIMIT} attached definitions')
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
    if type(prefix_budget) is not int or not 1 <= prefix_budget <= 32:
        errors.append('Component allocation: SQL prefix budget must be an integer from 1 through 32')
        prefix_budget = 12

    component_codes: set[str] = set()
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
        if not views or total_attached > VIEW_LIMIT:
            errors.append(f'{code}: {total_attached} attached definitions with {len(views)} table views, expected at least one table view and at most {VIEW_LIMIT} attachments')

        route_codes = {code.removeprefix('com_')}
        workspace_entities = []
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
                continue

            if not isinstance(name, str) or name not in entities:
                errors.append(f'{label}: unknown catalog entity')
                continue
            if name in allocations:
                errors.append(f'{label}: entity already allocated to {allocations[name]}')
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
                workspace_entities.append(name)
            elif visibility != 'internal':
                errors.append(f'{label}: unsupported visibility {visibility!r}')

        if workspace_entities != [component.get('workspace_entity')]:
            errors.append(f'{code}: expected exactly the declared primary workspace')

    missing = sorted(set(entities) - allocations.keys())
    if missing:
        errors.append(f'Component allocation: missing entities {", ".join(missing)}')

    entity_targets = {}
    for name, (_, record) in entities.items():
        targets = set()
        columns: set[str] = set()
        for field in _records(record, 'fields', name, errors):
            logical = field.get('name')
            if isinstance(logical, str):
                physical = logical
                if logical == record.get('identity'):
                    physical = 'guid'
                elif logical in RESERVED_COLUMNS:
                    physical = 'lms_' + logical
                _track(physical, columns, f'{name}.{logical} physical column', errors)
            target = field.get('references')
            if target is None:
                continue
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
                    and field.get('schema', {}).get('type') == 'string'
                    and field.get('schema', {}).get('format') == 'uuid'
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
    return errors
