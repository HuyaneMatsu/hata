import vampytest

from ...role_manager_metadata import (
    RoleManagerMetadataBase, RoleManagerMetadataBooster, RoleManagerMetadataBot, RoleManagerMetadataIntegration
)

from ..fields import put_manager
from ..preinstanced import RoleManagerType


def test__put_manager():
    """
    Tests whether ``put_manager`` works as intended.
    """
    entity_id = 202211020002

    for input_value, defaults, expected_output in (
        ((RoleManagerType.unset, RoleManagerMetadataBase()), False, {'managed': True, 'tags': {}}),
        ((RoleManagerType.none, RoleManagerMetadataBase()), False, {}),
        ((RoleManagerType.none, RoleManagerMetadataBase()), True, {'managed': False, 'tags': {}}),
        ((RoleManagerType.unknown, RoleManagerMetadataBase()), False, {'managed': True, 'tags': {}}),
        (
            (RoleManagerType.bot, RoleManagerMetadataBot(bot_id = entity_id)),
            False,
            {'managed': True, 'tags': {'bot_id': str(entity_id)}},
        ),
        (
            (RoleManagerType.booster, RoleManagerMetadataBooster()),
            False,
            {'managed': True, 'tags': {'premium_subscriber': None}},
        ),
        (
            (RoleManagerType.integration, RoleManagerMetadataIntegration(integration_id = entity_id)),
            False,
            {'managed': True, 'tags': {'integration_id': str(entity_id)}},
        ),
    ):
        output = put_manager(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
