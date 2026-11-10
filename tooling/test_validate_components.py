"""Synthetic coverage for the Joomla ownership and readiness manifest."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from string import ascii_lowercase
import tempfile
import unittest

from validate_components import RESERVED_COLUMNS, validate_component_map

UUID = {'type': 'string', 'format': 'uuid'}
COURSE = 'com_lmscourse'
FOUNDATION = 'com_lmsfoundation'
PRESENTER = 'com_lmspresenter'


def entity(name, domain, *fields):
    return {
        'name': name,
        'owner': domain,
        'identity': 'id',
        'unique_keys': [['id']],
        'fields': [
            {'name': 'id', 'schema': UUID.copy(), 'required': True, 'nullable': False},
            *fields,
        ],
    }


def reference(name, target):
    return {
        'name': name,
        'schema': UUID.copy(),
        'references': target,
        'reference_scope': 'Resolve the referenced entity in the authorized institution.',
    }


def admin_view(code, name, route, workspace=False):
    return {
        'entity': name,
        'definition_key': f'{code}.{route}',
        'single_code': route,
        'list_code': f'{route}_rows',
        'table': f'#__{code.removeprefix("com_")}_{route}',
        'visibility': 'workspace' if workspace else 'internal',
    }


def component(code, domain, contract, views, *, referenced=(), required=()):
    return {
        'code': code,
        'domain': domain,
        'title': 'Synthetic responsibility',
        'purpose': 'Own one reviewed lifecycle.',
        'grouping_rationale': 'Keep the same aggregate writes under one owner.',
        'separation_boundary': 'Other owners remain independently authorized.',
        'workspaces': [],
        'admin_views': views,
        'custom_admin_views': [],
        'normalized_edit_groups': [],
        'referenced_components': list(referenced),
        'provided_contracts': [{'contract': contract, 'api_major': 1, 'schema_revision': 3}],
        'required_components': list(required),
    }


def requirement(code, contract, *, major=1, minimum=1):
    return {
        'component': code,
        'contract': contract,
        'api_major': major,
        'minimum_schema_revision': minimum,
        'reason': 'The feature needs this owner ready before activation.',
    }


def workspace(key, entry_kind, entry):
    return {
        'key': key,
        'label': 'Synthetic workspace',
        'entry_kind': entry_kind,
        'entry': entry,
        'workflow': 'Review a scoped queue.',
        'access': 'Apply generated Joomla actions and the academic scope guard.',
    }


class ComponentMapTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        letters = ascii_lowercase[:24]
        lessons = [entity(f'Lesson{letter.upper()}', 'curriculum') for letter in letters]
        lessons[0]['fields'].append(reference('provider_id', 'IntegrationConnection'))
        lessons[1]['fields'].append(reference('parent_id', 'LessonA'))
        connection = entity(
            'IntegrationConnection', 'platform',
            reference('course_id', 'LessonA'),
            {'name': 'provider_kind', 'schema': {'type': 'string', 'enum': ['document', 'authoring']}},
        )
        self.catalogs = {'curriculum': lessons, 'platform': [connection]}
        course = component(
            COURSE, 'curriculum', 'lms.course',
            [admin_view(COURSE, lesson['name'], f'lesson_{letter}', workspace=letter in 'ab')
             for letter, lesson in zip(letters, lessons, strict=True)],
            referenced=[FOUNDATION],
            required=[requirement(FOUNDATION, 'lms.identity')],
        )
        course['workspaces'] = [
            workspace('review-published', 'admin_view', 'LessonA'),
            workspace('author-drafts', 'admin_view', 'LessonB'),
            workspace('learner-course', 'site_view', 'learner_course'),
        ]
        course['normalized_edit_groups'] = [
            {'parent_entity': 'LessonA', 'child_entities': ['LessonB'], 'mutation_authority': 'owner_command'},
        ]
        foundation = component(
            FOUNDATION, 'platform', 'lms.identity',
            [admin_view(FOUNDATION, 'IntegrationConnection', 'connection')],
            referenced=[COURSE],
        )
        presenter = component(
            PRESENTER, 'curriculum', 'lms.presenter', [],
            required=[requirement(COURSE, 'lms.course')],
        )
        presenter['custom_admin_views'] = [
            {'definition_key': f'{PRESENTER}.workbench', 'view_code': 'workbench',
             'purpose': 'Compose authorized views without another record owner.'},
        ]
        presenter['workspaces'] = [workspace('workbench', 'custom_admin_view', 'workbench')]
        self.manifest = {
            'manifest_version': '2.0.0',
            'components': [course, foundation, presenter],
            'persistence_policy': {
                'reserved_generated_columns': sorted(RESERVED_COLUMNS),
                'reserved_domain_column_prefix': 'lms_',
                'application_id_column': 'guid',
                'local_joomla_primary_key': 'id',
                'sql_prefix_budget': 12,
            },
            'host_requirements': {
                'joomla_major': 6,
                'shared_library': 'lib_lmscontracts',
                'php_version_policy': 'Use the tested host release range.',
                'database_profiles': ['mysql_innodb'],
                'bootstrap_components': [FOUNDATION],
            },
            'activation_sets': [],
            'feature_dependencies': [
                {'feature_key': 'documents', 'required_components': [COURSE, FOUNDATION],
                 'provider_profile_kinds': ['document'], 'reason': 'Available for a configured document provider.'},
            ],
        }

    def check(self, *, update_counts=True):
        spec = self.root / 'specification'
        for domain, records in self.catalogs.items():
            folder = spec / domain
            folder.mkdir(parents=True, exist_ok=True)
            (folder / 'catalog.json').write_text(json.dumps({'domain': domain, 'entities': records}))
        components = self.manifest['components']
        if update_counts:
            self.manifest['counts'] = {
                'domains': len(self.catalogs),
                'components': len(components),
                'persisted_entities': sum(map(len, self.catalogs.values())),
                'admin_view_definitions': sum(len(row['admin_views']) for row in components),
                'custom_admin_view_definitions': sum(len(row['custom_admin_views']) for row in components),
                'maximum_attached_per_component': max(
                    (len(row['admin_views']) + len(row['custom_admin_views']) for row in components), default=0,
                ),
                'by_domain': {
                    domain: {
                        'components': sum(row['domain'] == domain for row in components),
                        'entities': len(records),
                    }
                    for domain, records in self.catalogs.items()
                },
            }
        folder = spec / 'joomla'
        folder.mkdir(exist_ok=True)
        (folder / 'component-map.json').write_text(json.dumps(self.manifest))
        return validate_component_map(self.root)

    def assert_problem(self, message):
        errors = self.check()
        self.assertTrue(any(message in error for error in errors), errors)

    def test_cohesive_component_with_many_views_and_multiple_workspaces(self):
        course, _, presenter = self.manifest['components']
        self.assertGreater(len(course['admin_views']), 20)
        self.assertGreater(len(course['workspaces']), 1)
        self.assertEqual(presenter['admin_views'], [])
        # The mutual catalog reference is legitimate. Required readiness goes in one direction.
        self.assertEqual(self.check(), [])

    def test_unrelated_domain_cannot_own_the_component_entities(self):
        self.manifest['components'][0]['domain'] = 'platform'
        self.assert_problem('owner domain is curriculum, found platform')

    def test_duplicate_persisted_owner_is_rejected(self):
        self.manifest['components'][2]['admin_views'].append(admin_view(PRESENTER, 'LessonA', 'lesson_copy'))
        self.assert_problem(f'entity already allocated to {COURSE}')

    def test_custom_view_cannot_own_persistence(self):
        self.manifest['components'][2]['custom_admin_views'][0]['entity'] = 'LessonA'
        self.assert_problem('a Custom Admin View cannot own a persisted entity or table')

    def test_hidden_admin_view_cannot_be_a_declared_workspace(self):
        self.manifest['components'][0]['workspaces'][0]['entry'] = 'LessonC'
        self.assert_problem('admin entry LessonC is not an attached workspace view here')

    def test_native_identity_must_be_a_required_unique_uuid(self):
        self.catalogs['curriculum'][0]['fields'][0]['schema'] = {'type': 'integer'}
        self.assert_problem('application identity must be a required, non-null, independently unique UUID')

    def test_normalized_child_needs_scoped_scalar_parent_reference(self):
        self.catalogs['curriculum'][1]['fields'][1]['schema'] = {'type': 'array', 'items': UUID.copy()}
        self.assert_problem('normalized child LessonB lacks a typed parent reference to LessonA')

    def test_catalog_reference_needs_an_exact_owner_and_scope(self):
        relation = self.catalogs['curriculum'][0]['fields'][1]
        del relation['reference_scope']
        relation['references'] = 'UnallocatedProvider'
        errors = self.check()
        self.assertTrue(any('reference_scope: expected nonempty text' in error for error in errors), errors)
        self.assertTrue(any("no mapped owner for reference 'UnallocatedProvider'" in error for error in errors), errors)

    def test_provider_not_in_package_is_rejected(self):
        self.manifest['components'][0]['required_components'][0]['component'] = 'com_lmsabsent'
        self.assert_problem("required provider 'com_lmsabsent' is absent from the package")

    def test_provider_must_declare_matching_contract_and_compatible_schema(self):
        course, _, _ = self.manifest['components']
        course['required_components'] = [requirement(FOUNDATION, 'lms.identity', major=2)]
        self.assert_problem('does not declare lms.identity at API major 2')
        course['required_components'] = [requirement(FOUNDATION, 'lms.identity', minimum=4)]
        self.assert_problem('declares lms.identity schema revision 3, below 4')

    def test_required_cycle_needs_explicit_coactivation(self):
        _, foundation, _ = self.manifest['components']
        foundation['required_components'] = [requirement(COURSE, 'lms.course')]
        self.assert_problem('cyclic required installation plan')
        self.manifest['activation_sets'] = [
            {'key': 'local-foundation', 'members': [COURSE, FOUNDATION], 'required_sets': [],
             'reason': 'Two mutually dependent owners activate under one barrier.'},
        ]
        self.manifest['host_requirements']['bootstrap_components'] = [COURSE, FOUNDATION]
        self.assertEqual(self.check(), [])

    def test_required_sets_cannot_cycle_across_activation_barriers(self):
        self.manifest['activation_sets'] = [
            {'key': 'identity', 'members': [FOUNDATION], 'required_sets': ['delivery'], 'reason': 'Identity barrier.'},
            {'key': 'delivery', 'members': [COURSE], 'required_sets': [], 'reason': 'Delivery barrier.'},
        ]
        self.assert_problem('cyclic required installation plan')

    def test_bootstrap_must_include_whole_activation_set(self):
        self.manifest['activation_sets'] = [
            {'key': 'local-foundation', 'members': [COURSE, FOUNDATION], 'required_sets': [],
             'reason': 'Open these foundational owners together.'},
        ]
        self.assert_problem(f'bootstrap omits required components {COURSE}')

    def test_provider_profiles_are_optional_and_use_catalog_vocabulary(self):
        self.manifest['feature_dependencies'][0]['provider_profile_kinds'] = ['unregistered']
        self.assert_problem("provider profile kinds: unknown identifier 'unregistered'")

    def test_counts_report_actual_definitions_without_setting_a_budget(self):
        self.assertEqual(self.check(), [])
        original = deepcopy(self.manifest['counts'])
        self.manifest['counts']['maximum_attached_per_component'] = original['maximum_attached_per_component'] - 1
        self.assertIn('Component allocation: published count summary disagrees with verified definitions',
                      self.check(update_counts=False))


if __name__ == '__main__':
    unittest.main()
