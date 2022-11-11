import vampytest

from ..fields import parse_manager
from ..preinstanced import RoleManagerType


def test__parse_manager():
    """
    Tests whether ``parse_manager`` works as intended.
    """
    entity_id = 202211020001
    
    for input_value, expected_output in (
        ({}, (RoleManagerType.none, 0)),
        ({'managed': False}, (RoleManagerType.none, 0)),
        ({'managed': True}, (RoleManagerType.unset, 0)),
        ({'managed': True, 'tags': {'bot_id': str(entity_id)}}, (RoleManagerType.bot, entity_id)),
        ({'managed': True, 'tags': {'premium_subscriber': None}}, (RoleManagerType.booster, 0)),
        ({'managed': True, 'tags': {'integration_id': str(entity_id)}}, (RoleManagerType.integration, entity_id)),
    ):
        output = parse_manager(input_value)
        vampytest.assert_eq(output, expected_output)
