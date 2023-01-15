import vampytest

from ....integration import Integration

from ..application_role_connection import RoleManagerMetadataApplicationRoleConnection

from .test__RoleManagerMetadataApplicationRoleConnection__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataApplicationRoleConnection__copy():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.copy`` works as intended.
    """
    integration_id = 202301150007
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id,
    )
    copy = metadata.copy()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataApplicationRoleConnection__copy_with__0():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.to_data`` works as intended.
    
    Case: No fields given.
    """
    integration_id = 202301150008
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id,
    )
    copy = metadata.copy_with()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)

def test__RoleManagerMetadataApplicationRoleConnection__copy_with__1():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.to_data`` works as intended.
    
    Case: All fields given.
    """
    old_integration_id = 202301150009
    new_integration_id = 202301150010
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = old_integration_id,
    )
    copy = metadata.copy_with(
        integration_id = new_integration_id,
    )
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_is_not(copy, metadata)
    
    vampytest.assert_eq(copy.integration_id, new_integration_id)


def test__RoleManagerMetadataApplicationRoleConnection__manager_id():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.manager_id`` works as intended.
    """
    integration_id = 202301150011
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id,
    )
    vampytest.assert_eq(metadata.manager_id, integration_id)


def test__RoleManagerMetadataApplicationRoleConnection__manager():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.manager`` works as intended.
    """
    integration_id = 202301150012
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id,
    )
    vampytest.assert_is(metadata.manager, Integration.precreate(integration_id))
