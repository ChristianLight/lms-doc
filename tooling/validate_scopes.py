"""Validate canonical permission contexts and their typed authority paths."""

from __future__ import annotations

import json
from pathlib import Path


def _field_index(entity: dict) -> dict[str, dict]:
    return {field["name"]: field for field in entity.get("fields", [])}


def _path_endpoint(
    start: str,
    path: object,
    entities: dict[str, dict],
    label: str,
    errors: list[str],
    polymorphic: dict | None = None,
) -> str | None:
    if not isinstance(path, list) or not all(isinstance(part, str) and part for part in path):
        errors.append(f"{label}: expected an array of exact entity field names")
        return None
    if polymorphic is not None and len(path) != 1:
        errors.append(f"{label}: guarded polymorphic references must be a single field")
        return None
    current = start
    for part in path:
        entity = entities.get(current)
        if entity is None:
            errors.append(f"{label}: unresolved entity {current}")
            return None
        fields = _field_index(entity)
        field = fields.get(part)
        if field is None:
            errors.append(f"{label}: {current} has no field {part}")
            return None
        target = field.get("references")
        if polymorphic is not None:
            discriminator = fields.get(polymorphic.get("field"), {})
            target = polymorphic.get("value")
            if (
                field.get("references")
                or field.get("schema", {}).get("format") != "uuid"
                or target not in discriminator.get("schema", {}).get("enum", [])
            ):
                errors.append(f"{label}: invalid guarded reference {current}.{part}")
                return None
        if target not in entities:
            errors.append(f"{label}: {current}.{part} has no resolved entity reference")
            return None
        current = target
    return current


def validate_scope_registry(root: Path) -> list[str]:
    """Check the platform scope registry against every authored domain catalog."""
    specification = root / "specification"
    path = specification / "platform" / "scope-registry.json"
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
        catalogs = [
            json.loads(item.read_text(encoding="utf-8"))
            for item in sorted(specification.glob("*/catalog.json"))
        ]
    except (OSError, ValueError) as exc:
        return [f"Scope registry cannot be loaded: {exc}"]

    errors: list[str] = []
    entities = {
        entity["name"]: entity for catalog in catalogs for entity in catalog.get("entities", [])
    }
    permissions = {
        permission["key"]: permission
        for catalog in catalogs
        for permission in catalog.get("permissions", [])
    }
    if registry.get("registry_version") != "1.0.0":
        errors.append("Scope registry: unsupported registry_version")

    contexts: dict[str, dict] = {}
    registered_entities: set[str] = set()
    for record in registry.get("contexts", []):
        name = record.get("context")
        entity = record.get("entity")
        if not name or name in contexts:
            errors.append(f"Scope registry: missing or duplicate context {name!r}")
            continue
        contexts[name] = record
        if entity not in entities or entity in registered_entities:
            errors.append(f"Scope {name}: missing or duplicate canonical entity {entity!r}")
            continue
        registered_entities.add(entity)
        if type(record.get("assignable")) is not bool:
            errors.append(f"Scope {name}: assignable must be a boolean")
        if not isinstance(record.get("owner_guard"), str) or not record["owner_guard"].strip():
            errors.append(f"Scope {name}: missing domain owner guard")
        end = _path_endpoint(entity, record.get("tenant_path"), entities, f"Scope {name} tenant_path", errors)
        if end is not None and end != "Institution":
            errors.append(f"Scope {name}: tenant_path ends at {end}, expected Institution")

    for name, record in contexts.items():
        entity = record.get("entity")
        parents = record.get("authority_parents")
        if not isinstance(parents, list):
            errors.append(f"Scope {name}: authority_parents must be an array")
            continue
        seen: set[tuple[str, tuple[str, ...]]] = set()
        for parent in parents:
            target = parent.get("context")
            label = f"Scope {name} authority parent {target}"
            if target not in contexts:
                errors.append(f"{label}: target context does not exist")
                continue
            parent_path = parent.get("path")
            if not isinstance(parent_path, list) or not parent_path:
                errors.append(f"{label}: expected a nonempty reference path")
                continue
            end = _path_endpoint(entity, parent_path, entities, label, errors, parent.get("polymorphic"))
            if end is None:
                continue
            key = (target, tuple(parent_path))
            if key in seen:
                errors.append(f"{label}: duplicate authority path")
            seen.add(key)
            if end != contexts[target].get("entity"):
                errors.append(f"{label}: path resolves {end}, expected {contexts[target].get('entity')}")
            if parent.get("polymorphic") and not parent.get("when"):
                errors.append(f"{label}: missing guard for polymorphic path")

        queries = record.get("authority_queries", [])
        if not isinstance(queries, list):
            errors.append(f"Scope {name}: authority_queries must be an array")
            continue
        for query in queries:
            target = query.get("context")
            relation = query.get("relation")
            label = f"Scope {name} authority query {relation} to {target}"
            if relation not in entities or target not in contexts or entity not in entities:
                errors.append(f"{label}: unresolved source, relation or target")
                continue
            relation_fields = _field_index(entities[relation])
            if query.get("from_field") != entities[entity].get("identity"):
                errors.append(f"{label}: query must begin from the canonical source identity")
            for property_name, expected in (
                ("match_field", entity),
                ("target_field", contexts[target]["entity"]),
            ):
                if relation_fields.get(query.get(property_name), {}).get("references") != expected:
                    errors.append(f"{label}: {property_name} must reference {expected}")
            for property_name in ("effective_from_field", "effective_to_field"):
                if relation_fields.get(query.get(property_name), {}).get("schema", {}).get("format") != "date-time":
                    errors.append(f"{label}: {property_name} must be a date-time field")
            if not query.get("when"):
                errors.append(f"{label}: missing effective authority guard")

    for key, permission in permissions.items():
        scopes = permission.get("scopes", [])
        if not scopes or len(scopes) != len(set(scopes)):
            errors.append(f"Permission {key}: expected at least one distinct target scope")
        for scope in scopes:
            if scope not in contexts:
                errors.append(f"Permission {key}: unregistered scope {scope!r}")

    assignable = {name for name, record in contexts.items() if record.get("assignable") is True}
    assignment = _field_index(entities.get("RoleAssignment", {})).get("scope_type", {})
    actual = set(assignment.get("schema", {}).get("enum", []))
    if actual != assignable:
        errors.append(
            f"RoleAssignment.scope_type: missing {sorted(assignable - actual)}, "
            f"unassignable {sorted(actual - assignable)}"
        )
    bootstrap = registry.get("bootstrap", {})
    if (
        bootstrap.get("permission") != "platform.institution.bootstrap"
        or bootstrap.get("permission") not in permissions
        or bootstrap.get("context") != "DeploymentControlPlane"
        or bootstrap.get("context") in contexts
        or bootstrap.get("assignable") is not False
        or "entity" not in bootstrap
        or bootstrap["entity"] is not None
        or not bootstrap.get("entry_rule")
    ):
        errors.append("Scope registry: invalid separate deployment bootstrap context")
    return errors
