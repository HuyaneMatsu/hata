import vampytest

from ..fields import put_manager_into
from ..preinstanced import RoleManagerType


def test__put_manager_into():
    """
    Tests whether ``put_manager_into`` works as intended.
    """
    entity_id = 202211020002
    
    for input_value, defaults, expected_output in (
        ((RoleManagerType.unset, 0), False, {'managed': True}),
        ((RoleManagerType.none, 0), False, {}),
        ((RoleManagerType.none, 0), True, {'managed': False}),
        ((RoleManagerType.unknown, 0), False, {'managed': True}),
        ((RoleManagerType.bot, entity_id), False, {'managed': True, 'tags': {'bot_id': str(entity_id)}}),
        ((RoleManagerType.booster, 0), False, {'managed': True, 'tags': {'premium_subscriber': None}}),
        ((RoleManagerType.integration, entity_id), False, {'managed': True, 'tags': {'integration_id': str(entity_id)}}),
    ):
        output = put_manager_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
