import vampytest

from ...role_manager_metadata import (
    RoleManagerMetadataApplicationRoleConnection, RoleManagerMetadataBase, RoleManagerMetadataBooster,
    RoleManagerMetadataBot, RoleManagerMetadataIntegration, RoleManagerMetadataSubscription
)

from ..fields import parse_manager
from ..preinstanced import RoleManagerType


def test__parse_manager():
    """
    Tests whether ``parse_manager`` works as intended.
    """
    entity_id_0 = 202211020001
    entity_id_1 = 202301150013
    
    for input_value, expected_output in (
        ({}, (RoleManagerType.none, RoleManagerMetadataBase())),
        ({'managed': False}, (RoleManagerType.none, RoleManagerMetadataBase())),
        ({'managed': True}, (RoleManagerType.unset, RoleManagerMetadataBase())),
        (
            {'managed': True, 'tags': {'bot_id': str(entity_id_0)}},
            (RoleManagerType.bot, RoleManagerMetadataBot(bot_id = entity_id_0)),
        ),
        (
            {'managed': True, 'tags': {'premium_subscriber': None}},
            (RoleManagerType.booster, RoleManagerMetadataBooster()),
        ),
        (
            {'managed': True, 'tags': {'integration_id': str(entity_id_0)}},
            (RoleManagerType.integration, RoleManagerMetadataIntegration(integration_id = entity_id_0)),
        ),
        (
            {'managed': True, 'tags': {'integration_id': str(entity_id_0), 'subscription_listing_id': str(entity_id_1)}},
            (
                RoleManagerType.subscription,
                RoleManagerMetadataSubscription(
                    integration_id = entity_id_0,
                    subscription_listing_id = entity_id_1,
                    purchasable = False,
                ),
            ),
        ),
        (
            {'managed': True, 'tags': {'integration_id': str(entity_id_0), 'guild_connections': None}},
            (
                RoleManagerType.application_role_connection,
                RoleManagerMetadataApplicationRoleConnection(integration_id = entity_id_0),
            ),
        ),
    ):
        output = parse_manager(input_value)
        vampytest.assert_eq(output, expected_output)
