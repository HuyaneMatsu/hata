import vampytest

from ...role_manager_metadata import (
    RoleManagerMetadataBase, RoleManagerMetadataBooster, RoleManagerMetadataBot, RoleManagerMetadataIntegration
)

from ..fields import parse_manager
from ..preinstanced import RoleManagerType


def test__parse_manager():
    """
    Tests whether ``parse_manager`` works as intended.
    """
    entity_id = 202211020001
    
    for input_value, expected_output in (
        ({}, (RoleManagerType.none, RoleManagerMetadataBase())),
        ({'managed': False}, (RoleManagerType.none, RoleManagerMetadataBase())),
        ({'managed': True}, (RoleManagerType.unset, RoleManagerMetadataBase())),
        (
            {'managed': True, 'tags': {'bot_id': str(entity_id)}},
            (RoleManagerType.bot, RoleManagerMetadataBot(bot_id = entity_id)),
        ),
        (
            {'managed': True, 'tags': {'premium_subscriber': None}},
            (RoleManagerType.booster, RoleManagerMetadataBooster()),
        ),
        (
            {'managed': True, 'tags': {'integration_id': str(entity_id)}},
            (RoleManagerType.integration, RoleManagerMetadataIntegration(integration_id = entity_id)),
        ),
    ):
        output = parse_manager(input_value)
        vampytest.assert_eq(output, expected_output)
