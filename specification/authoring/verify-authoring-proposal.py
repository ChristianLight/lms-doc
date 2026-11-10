#!/usr/bin/env python3
"""Validate local review proposals and the synthetic authoring fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from collections import defaultdict, deque
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

HERE = Path(__file__).resolve().parent
TASK = HERE / 'authoring-task.schema.json'
PROPOSAL = HERE / 'proposal-bundle.schema.json'
FIXTURE = HERE / 'synthetic-source-to-course.json'
LEARNING = HERE.parent / 'curriculum' / 'learning-definition.schema.json'
ASSESSMENT = HERE.parent / 'assessment' / 'catalog.json'
CURRICULUM = HERE.parent / 'curriculum' / 'catalog.json'
MAX_SOURCE_BYTES = 50 * 1024 * 1024
MAX_REVIEW_ARTIFACT_BYTES = 20 * 1024 * 1024
MAX_PROPOSAL_READ_BYTES = 256 * 1024 * 1024
MAX_JSON_DEPTH = 64
SOURCE_ID_PREFIX = 'urn:lms:source:sha256:'
IDENTITY_NAME = 'proposal-identity.json'
LOCAL_KEY = re.compile(r'^[a-z][a-z0-9_.:-]{0,239}$')
STAGES = ('coverage_plan', 'course_plan', 'learning_blocks', 'assessment_candidates', 'verification')
STORAGE_FIELDS = {'storage_object_id', 'content_sha256', 'purpose'}
OWNER_FIELDS = {'institution_id', 'principal_id', 'agent_principal_id', 'platform_job_id',
                'authoring_run_id', 'extraction_run_id', 'lease_id', 'owner_receipt_id',
                'expected_draft_revision', 'expected_draft_version', 'approved_by_id'}
CANDIDATE_REFERENCES = {
    'asset_version_id': 'asset', 'poster_asset_version_id': 'asset',
    'transcript_asset_version_id': 'asset', 'audio_description_asset_version_id': 'asset',
    'alternative_content_node_version_id': 'content_node', 'marking_rule_version_id': 'marking_rule',
    'fixed_item_version_id': 'item', 'delivery_binding_policy_id': 'policy',
    'adapter_policy_version_id': 'policy', 'eligibility_policy_id': 'policy',
    'content_node_version_id': 'content_node', 'activity_version_id': 'activity',
    'assessment_version_id': 'assessment', 'rule_version_id': 'policy',
    'launch_policy_version_id': 'policy', 'participation_policy_id': 'policy',
}
PLACEMENT_REFERENCES = {'placement_key', 'alternative_placement_key'}
ASSESSMENT_ACTIVITY_TYPES = {'self_check', 'quiz', 'exam', 'assignment'}
RESOURCE_TYPES = {'rich_text', 'image', 'document', 'video', 'audio', 'external_link',
                  'internal_link', 'imported_unresolved'}


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def synthetic_digest(value):
    # Fixture values use integer scalars and ASCII property names.
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        demand(key not in result, f'Duplicate JSON property {key!r}')
        result[key] = value
    return result


def decode(data):
    def invalid_constant(value):
        raise ValueError(f'Invalid JSON constant {value}')

    parsed = json.loads(data.decode('utf-8'), object_pairs_hook=unique_object, parse_constant=invalid_constant)
    pending = [(parsed, 0)]
    while pending:
        value, depth = pending.pop()
        demand(depth <= MAX_JSON_DEPTH, 'JSON exceeds the private proposal depth limit')
        if isinstance(value, dict):
            pending.extend((child, depth + 1) for child in value.values())
        elif isinstance(value, list):
            pending.extend((child, depth + 1) for child in value)
    return parsed


def validator(schema):
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def read_limited(path, limit=MAX_REVIEW_ARTIFACT_BYTES):
    demand(path.is_file(), f'Expected a regular file at {path}')
    with path.open('rb') as source:
        data = source.read(limit + 1)
    demand(0 < len(data) <= limit, f'File is empty or exceeds the allowed size at {path}')
    return data


def source_description(path):
    data = read_limited(path, MAX_SOURCE_BYTES)
    demand(b'%PDF-' in data[:1024], 'The input does not have a PDF header')
    digest = sha(data)
    return {'source_namespace': SOURCE_ID_PREFIX + digest, 'sha256': digest, 'bytes': len(data)}


def proposal_scope(value):
    demand(isinstance(value, str), 'Expected a proposal scope string')
    scope = uuid.UUID(value)
    demand(scope.version == 4 and str(scope) == value, 'Expected a canonical UUIDv4 proposal scope')
    return scope


def read_identity(path, observed):
    demand(not path.is_symlink(), 'Proposal identity must not be a symlink')
    identity = decode(read_limited(path))
    demand(isinstance(identity, dict) and set(identity) == {'proposal_id', 'source_namespace', 'sha256', 'bytes'},
           'Invalid persisted proposal identity')
    proposal_scope(identity['proposal_id'])
    demand(all(identity[key] == value for key, value in observed.items()),
           'This proposal scope already belongs to different source bytes')
    return identity


def init_proposal(directory, pdf):
    demand(directory.is_dir() and not directory.is_symlink(),
           'Use an existing private directory for the proposal')
    directory = directory.resolve()
    demand(not directory.is_relative_to(HERE.parents[1])
           and not any((parent / '.git').exists() for parent in (directory, *directory.parents)),
           'Keep private proposal identity and evidence outside repository checkouts')
    metadata = directory.stat()
    demand(metadata.st_uid == os.geteuid() and metadata.st_mode & 0o077 == 0,
           'Use a directory owned by the current user with owner-only permissions')
    observed = source_description(pdf)
    path = directory / IDENTITY_NAME
    if path.exists() or path.is_symlink():
        return read_identity(path, observed)
    identity = {'proposal_id': str(uuid.uuid4()), **observed}
    # Write a complete immutable identity then atomically link it into the directory.
    # Losing concurrent initializers read the winner rather than allocate a new scope.
    staged = directory / f'.proposal-identity-{uuid.uuid4()}.tmp'
    fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            json.dump(identity, output)
            output.write('\n')
        try:
            os.link(staged, path)
        except FileExistsError:
            pass
    finally:
        staged.unlink(missing_ok=True)
    return read_identity(path, observed)


def local_id(proposal_id, key):
    demand(LOCAL_KEY.fullmatch(key), 'Use a stable lowercase local key of at most 240 characters')
    return str(uuid.uuid5(proposal_scope(proposal_id), key))


def local_artifact(root, relative_path, expected_hash):
    rel = PurePosixPath(relative_path)
    demand(not rel.is_absolute() and '..' not in rel.parts and rel.as_posix() == relative_path,
           f'Noncanonical or escaping artifact path {relative_path!r}')
    path = root
    for part in rel.parts:
        path /= part
        demand(not path.is_symlink(), f'Symlink is forbidden at {relative_path!r}')
    demand(path.resolve().is_relative_to(root), f'Artifact escapes proposal root {relative_path!r}')
    data = read_limited(path)
    demand(sha(data) == expected_hash, f'Artifact digest mismatch at {relative_path!r}')
    return data


class ProposalFiles:
    def __init__(self, root):
        self.root = root
        self.bytes_read = 0

    def read(self, path, digest):
        data = local_artifact(self.root, path, digest)
        self.bytes_read += len(data)
        demand(self.bytes_read <= MAX_PROPOSAL_READ_BYTES, 'Proposal exceeds the total private read budget')
        return data

    def from_ref(self, ref):
        return self.read(ref['relative_path'], ref['sha256'])


def task_projection(value):
    """Reuse the task schemas while replacing installed storage with local evidence."""
    if isinstance(value, list):
        return [task_projection(item) for item in value]
    if not isinstance(value, dict):
        return value
    projected = {key: task_projection(child) for key, child in value.items()}
    properties = projected.get('properties', {})
    if set(properties) == STORAGE_FIELDS:
        del properties['storage_object_id']
        properties['relative_path'] = {
            'type': 'string', 'pattern': r'^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*$', 'maxLength': 240}
        projected['required'] = [key if key != 'storage_object_id' else 'relative_path'
                                 for key in projected['required']]
    return projected


def without_fields(schema, field_names):
    return {**schema,
            'properties': {key: value for key, value in schema['properties'].items()
                           if key not in field_names},
            'required': [key for key in schema['required'] if key not in field_names]}


def reject_owner_fields(value):
    if isinstance(value, list):
        for entry in value:
            reject_owner_fields(entry)
    elif isinstance(value, dict):
        installed = OWNER_FIELDS.intersection(value)
        demand(not installed, f'Installed identity or owner receipt in offline data: {sorted(installed)}')
        for child in value.values():
            reject_owner_fields(child)


def references(value, key):
    if isinstance(value, list):
        for item in value:
            yield from references(item, key)
    elif isinstance(value, dict):
        for name, child in value.items():
            if name == key:
                yield child
            yield from references(child, key)


def assert_acyclic(vertices, edges, label):
    pending = {}
    dependents = defaultdict(list)
    for key in vertices:
        dependencies = set(edges.get(key, ()))
        demand(dependencies.issubset(vertices), f'Missing reference in {label}')
        pending[key] = len(dependencies)
        for prerequisite in dependencies:
            dependents[prerequisite].append(key)
    ready = deque(key for key, count in pending.items() if count == 0)
    processed = 0
    while ready:
        prerequisite = ready.popleft()
        processed += 1
        for key in dependents[prerequisite]:
            pending[key] -= 1
            if pending[key] == 0:
                ready.append(key)
    demand(processed == len(vertices), f'Cycle in {label}')


def check_candidate_references(value, candidates, placements, dependencies):
    if isinstance(value, list):
        for child in value:
            check_candidate_references(child, candidates, placements, dependencies)
    elif isinstance(value, dict):
        for key, child in value.items():
            if key in CANDIDATE_REFERENCES and child is not None:
                demand(child in dependencies and candidates[child]['kind'] == CANDIDATE_REFERENCES[key],
                       f'Typed local dependency required for {key}')
            elif key in PLACEMENT_REFERENCES:
                demand(child in placements, f'Missing local placement for {key}')
            elif key.endswith('_id') or key.endswith('_ids'):
                demand(child is None, f'Owner-bound reference {key} requires LMS admission')
            check_candidate_references(child, candidates, placements, dependencies)


def verify_proposal(manifest, pdf):
    demand(not manifest.is_symlink(), 'Proposal manifest must not be a symlink')
    files = ProposalFiles(manifest.parent.resolve())
    proposal = decode(read_limited(manifest))
    validator(decode(read_limited(PROPOSAL))).validate(proposal)
    observed = source_description(pdf)
    source = proposal['source']
    namespace = proposal['source_namespace']
    proposal_id = proposal['proposal_id']
    identity = read_identity(files.root / IDENTITY_NAME, observed)
    demand(identity['proposal_id'] == proposal_id, 'Proposal ID does not match the persisted scope')
    demand(namespace == observed['source_namespace'] and source['sha256'] == observed['sha256']
           and source['bytes'] == observed['bytes'], 'Source bytes do not match this proposal')
    selected = source['selected_page_indices']
    demand(selected == sorted(selected) and selected[-1] < source['physical_page_count'],
           'Selected pages must be ascending and inside the source page count')
    review = files.from_ref(proposal['review']).decode('utf-8')
    demand(proposal['review']['relative_path'].endswith('.md') and review.strip(),
           'Review brief must be a nonempty Markdown file')

    defs = decode(read_limited(TASK))['$defs']
    page_schema = without_fields(task_projection(defs['source_page_evidence']),
                                 {'extraction_run_id'})
    page_validator = validator(page_schema)
    pages_seen = set()
    regions = set()
    usable_regions = set()
    for ref in proposal['source_pages']:
        page = decode(files.from_ref(ref))
        page_validator.validate(page)
        transform = page['transform']
        index = transform['physical_page_index']
        demand(index in selected and index not in pages_seen, 'Missing or duplicate page binding')
        pages_seen.add(index)
        demand(transform['physical_page_count'] == source['physical_page_count']
               and page['source_digest'] == source['sha256'], 'Page evidence has the wrong source')
        shard = page['evidence_object']
        files.read(shard['relative_path'], shard['content_sha256'])
        width, height = transform['upright_extent_mpt']
        for region in page['regions']:
            rid = local_id(proposal_id, f'region:{index}:{region["ordinal"]}')
            x0, y0, x1, y1 = region['bbox_mpt']
            demand(rid not in regions and 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height,
                   'Duplicate region ordinal or region outside the upright page')
            regions.add(rid)
            if page['state'] == 'ready' and region['review_state'] == 'candidate':
                usable_regions.add(rid)
    demand(pages_seen == set(selected), 'Source evidence must cover all selected page indices')

    stage_data = {}
    for stage in STAGES:
        body = decode(files.from_ref(proposal['stages'][stage]))
        validator(task_projection(defs[stage + '_manifest']['properties']['body'])).validate(body)
        reject_owner_fields(body)
        for ids in references(body, 'source_region_ids'):
            demand(set(ids).issubset(regions), f'Source region binding missing in {stage}')
        stage_data[stage] = body
    outline = stage_data['course_plan']['outline']
    outline_by_key = {row['placement_key']: row for row in outline}
    placement_keys = set(outline_by_key)
    objectives = {row['objective_id'] for row in stage_data['course_plan']['objectives']}
    demand(len(placement_keys) == len(outline), 'Duplicate placement key')
    demand(len(objectives) == len(stage_data['course_plan']['objectives']), 'Duplicate objective ID')
    demand(all(set(row['objective_ids']).issubset(objectives) for row in outline),
           'A placement refers to an unknown objective')
    demand(all(set(row['source_region_ids']).issubset(usable_regions)
               for row in outline + stage_data['course_plan']['objectives']),
           'Course plan refers to excluded or unresolved material source evidence')
    assert_acyclic(placement_keys,
                   {row['placement_key']: [row['parent_key']] for row in outline if row['parent_key']},
                   'placement tree')
    assert_acyclic(objectives, {row['objective_id']: row['prerequisite_objective_ids']
                               for row in stage_data['course_plan']['objectives']}, 'objective prerequisites')
    sibling_positions = defaultdict(list)
    for row in outline:
        sibling_positions[row['parent_key']].append(row['position'])
    for positions in sibling_positions.values():
        demand(sorted(positions) == list(range(len(positions))), 'Sibling positions must start at zero without gaps')

    candidates = {}
    typed_payloads = {}
    definition_validator = validator(decode(read_limited(LEARNING)))
    curriculum = decode(read_limited(CURRICULUM))
    curriculum_commands = {row['name']: row['request_schema'] for row in curriculum['commands']}
    outline_operations = curriculum_commands['MutateDraftOutline']['properties']['operations']['items']['oneOf']
    placement_shape = next(operation['properties']['placement'] for operation in outline_operations
                           if 'placement' in operation['properties'])
    activity_shape = without_fields(curriculum_commands['SealActivityVersion'], {'base_revision'})
    activity_validator = validator(activity_shape)
    placement_validator = validator(placement_shape)
    assessment = decode(read_limited(ASSESSMENT))
    assessment_commands = {row['name']: row['request_schema'] for row in assessment['commands']}
    assessment_projections = {
        'item': validator(without_fields(assessment_commands['SaveItemDraft'], {'expected_draft_version'})),
        'marking_rule': validator(without_fields(assessment_commands['ApproveMarkingRule'],
                                                 {'institution_id', 'evaluator_release_id'})),
        'assessment': validator(without_fields(assessment_commands['SaveAssessmentDraft'],
                                               {'expected_draft_version'})),
    }
    for stage in ('learning_blocks', 'assessment_candidates'):
        for candidate in stage_data[stage]['candidates']:
            key = candidate['candidate_id']
            demand(key not in candidates, 'A candidate ID must appear once in the current proposal')
            candidates[key] = candidate
            payload = candidate['payload']
            data = files.read(payload['relative_path'], payload['content_sha256'])
            demand(candidate['digest'] == payload['content_sha256'],
                   'Offline candidate digest must pin its exact payload file')
            kind = candidate['kind']
            if kind in ('content_node', 'activity', 'placement') or kind in assessment_projections:
                body = decode(data)
                typed_payloads[key] = body
                reject_owner_fields(body)
                if kind in ('content_node', 'activity'):
                    if kind == 'activity':
                        activity_validator.validate(body)
                    definition = body['payload'] if kind == 'activity' else body
                    definition_validator.validate(definition)
                    demand(all(variant['review_state'] == 'draft' for variant in definition['variants']),
                           'Unbound learning variants must remain draft')
                elif kind == 'placement':
                    placement_validator.validate(body)
                else:
                    assessment_projections[kind].validate(body)
            for claim in candidate['claims']:
                if claim['classification'] in ('extracted', 'source_supported_paraphrase', 'derived'):
                    demand(claim['source_region_ids'] and set(claim['source_region_ids']).issubset(usable_regions),
                           'Source-supported claim has excluded, unresolved or missing exact source evidence')
                if claim['classification'] == 'derived':
                    demand(claim['verification_evidence'] is not None,
                           'Derived claim has no protected verification evidence')
                if claim['verification_evidence'] is not None:
                    evidence = claim['verification_evidence']
                    files.read(evidence['relative_path'], evidence['content_sha256'])
    assert_acyclic(candidates,
                   {key: value['dependency_candidate_ids'] for key, value in candidates.items()},
                   'candidate dependency graph')
    issue_sets = [body['issues'] for body in stage_data.values()]
    issue_sets.extend(candidate['issues'] for candidate in candidates.values())
    blockers = {(issue['code'], issue['path'], tuple(issue['source_region_ids']))
                for issues in issue_sets for issue in issues if issue['severity'] == 'blocking'}
    blocked_paths = {(code, path) for code, path, _ in blockers}
    placements = set()
    for key, payload in typed_payloads.items():
        kind = candidates[key]['kind']
        check_candidate_references(payload, candidates, placement_keys,
                                   set(candidates[key]['dependency_candidate_ids']))
        if kind == 'activity':
            activity_type = payload['payload']['type_key']
            assessment_id = payload.get('assessment_version_id')
            if activity_type in ASSESSMENT_ACTIVITY_TYPES:
                demand(assessment_id is not None or
                       ('ASSESSMENT_BINDING_MISSING', f'/candidates/{key}') in blocked_paths,
                       'Assessed activity requires one local assessment or an explicit blocker')
            else:
                demand(assessment_id is None, 'Non-assessment activity cannot bind an assessment definition')
        elif kind == 'placement':
            placement_key = payload['placement_key']
            demand(placement_key not in placements, 'More than one typed binding for an outline placement')
            placements.add(placement_key)
            planned = outline_by_key[placement_key]
            demand(all(payload[field] == planned[field] for field in ('parent_key', 'position', 'required')),
                   'Typed placement differs from reviewed outline identity or order')
            expected_type = planned['kind']
            actual_type = payload['kind']
            demand(actual_type == expected_type or (expected_type == 'resource' and actual_type in RESOURCE_TYPES),
                   'Typed placement kind is inconsistent with the outline')
            content_id = payload['content_node_version_id']
            activity_id = payload['activity_version_id']
            demand((actual_type == 'activity' and activity_id is not None and content_id is None) or
                   (actual_type != 'activity' and content_id is not None and activity_id is None),
                   'Typed placement needs exactly one matching content or activity dependency')
            if content_id is not None:
                demand(typed_payloads[content_id]['type_key'] == actual_type,
                       'Placement and content definition have different kinds')
    for key in placement_keys - placements:
        demand(('PLACEMENT_BINDING_MISSING', f'/outline/{key}') in blocked_paths,
               'Outline placement has no typed local binding or explicit blocker')
    for evaluation in stage_data['verification']['evaluations']:
        demand(evaluation['evaluator_release_id'] is None,
               'Offline verification cannot claim an installed evaluator release')
        candidate = candidates.get(evaluation['candidate_id'])
        demand(candidate and candidate['revision'] == evaluation['candidate_revision'],
               'Verification must pin an exact local candidate revision')
        rules = [candidate] + [candidates[key] for key in candidate['dependency_candidate_ids']]
        demand(any(rule['kind'] == 'marking_rule' and rule['digest'] == evaluation['rule_digest'] for rule in rules),
               'Verification does not pin an exact local marking rule')
        demand(evaluation['failed_count'] <= evaluation['test_count'], 'Failed vectors exceed total vectors')
        evidence = evaluation['verification_object']
        files.read(evidence['relative_path'], evidence['content_sha256'])
    return {'state': proposal['state'], 'proposal_id': proposal_id, 'source_namespace': namespace,
            'selected_pages': len(selected), 'regions': len(regions),
            'candidates': len(candidates),
            'blocking_issues': len(blockers),
            'admitted': False, 'published': False, 'exported': False}


def verify_synthetic():
    task_schema = decode(read_limited(TASK))
    task_validator = validator(task_schema)
    bundle_validator = validator(decode(read_limited(PROPOSAL)))
    fixture = decode(read_limited(FIXTURE))
    for example in task_schema['examples'] + fixture['contract_examples']:
        task_validator.validate(example)
    demand(fixture['classification'] == 'wholly_synthetic', 'Expected synthetic fixture')
    demand(synthetic_digest(fixture['source_payload']) == fixture['source_payload_digest_sha256'],
           'Synthetic source digest changed')
    for payload, region in zip(fixture['source_payload'], fixture['accepted_regions'], strict=True):
        demand(synthetic_digest(payload) == region['payload_digest_sha256'], 'Synthetic region digest changed')
        demand(payload['page_index'] == region['page_index'] and payload['bbox_mpt'] == region['bbox_mpt'],
               'Synthetic region coordinate mismatch')
    _, request, coverage, receipt, plan = fixture['contract_examples']
    demand(request['effect_key'] == receipt['effect_key'], 'Synthetic effect receipt mismatch')
    demand(synthetic_digest(coverage) == receipt['output_manifest']['content_sha256']
           == plan['parent_manifest_digest'], 'Synthetic stage digest chain mismatch')
    choice, expression, blocked = fixture['assessment_candidates']
    demand(choice['staff_only_key']['expected_option_id'] == f'c_{3 * 60}', 'Synthetic conversion key incorrect')
    demand(expression['staff_only_key']['normalized_coefficients_high_to_low'] == [str(3 * 1), str(3 * 2)],
           'Synthetic symbolic key incorrect')
    demand(blocked['status'] == 'blocked' and blocked['staff_only_key'] is None and blocked['vectors'] == [],
           'Synthetic incomplete item must have no answer key')
    demand(blocked['candidate_id'] not in fixture['approved_selection']['selected_candidate_ids'],
           'Synthetic blocked candidate selected')
    demand(fixture['portability_cases'][2]['status'] == 'blocked',
           'Synthetic unsupported standalone grading must remain blocked')
    demand(not bundle_validator.is_valid({'state': 'published'}), 'Proposal envelope accepts publication claim')
    first = '00000000-0000-4000-8000-000000000001'
    second = '00000000-0000-4000-8000-000000000002'
    key = 'region:0:0'
    demand(local_id(first, key) == local_id(first, key), 'Proposal-local identity is not stable')
    demand(local_id(first, key) != local_id(second, key), 'Independent proposal scope collision')
    demand(local_id(first, key) != local_id(first, 'region:0:1'), 'Local region ID collision')
    return {'fixture': FIXTURE.name, 'status': 'verified',
            'assessment_candidates': 3, 'blocked_incomplete_candidates': 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('self-test', help='Validate existing wholly synthetic evidence and keys')
    source = commands.add_parser('source', help='Print byte identity of a local source PDF')
    source.add_argument('pdf', type=Path)
    initialize = commands.add_parser('init', help='Allocate or reopen the persisted proposal scope')
    initialize.add_argument('directory', type=Path)
    initialize.add_argument('--source', type=Path, required=True)
    identity = commands.add_parser('local-id', help='Derive a deterministic proposal-local UUID')
    identity.add_argument('proposal_id')
    identity.add_argument('key')
    verify = commands.add_parser('verify', help='Validate a local unbound review proposal')
    verify.add_argument('proposal', type=Path)
    verify.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == 'self-test':
            result = verify_synthetic()
        elif args.action == 'source':
            result = source_description(args.pdf)
        elif args.action == 'init':
            result = init_proposal(args.directory, args.source)
        elif args.action == 'local-id':
            result = {'local_id': local_id(args.proposal_id, args.key)}
        else:
            result = verify_proposal(args.proposal, args.source)
        print(json.dumps(result, indent=2))
        return 0
    except ValidationError as exc:
        path = '/'.join(str(part) for part in exc.absolute_path) or '(root)'
        print(f'Authoring verification failed: {exc.validator} at {path}', file=sys.stderr)
        return 1
    except RecursionError:
        print('Authoring verification failed: excessive JSON nesting', file=sys.stderr)
        return 1
    except (ValueError, OSError) as exc:
        print(f'Authoring verification failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
