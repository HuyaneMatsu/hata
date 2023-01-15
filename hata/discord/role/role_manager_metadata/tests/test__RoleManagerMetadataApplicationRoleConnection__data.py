import vampytest

from ..application_role_connection import RoleManagerMetadataApplicationRoleConnection

from .test__RoleManagerMetadataApplicationRoleConnection__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataApplicationRoleConnection__from_data():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.from_data`` works as intended.
    """
    integration_id = 202301150005
    
    data = {
        'integration_id': str(integration_id)
    }
    
    metadata = RoleManagerMetadataApplicationRoleConnection.from_data(data)
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.integration_id, integration_id)


def test__RoleManagerMetadataApplicationRoleConnection__to_data():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.to_data`` works as intended.
    """
    integration_id = 202301150006
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id
    )
    
    expected_data = {
        'integration_id': str(integration_id),
        'guild_connections': None,
    }
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_data
    )
