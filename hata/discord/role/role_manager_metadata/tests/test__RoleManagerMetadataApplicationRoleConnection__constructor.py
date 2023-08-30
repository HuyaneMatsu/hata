import vampytest

from ..application_role_connection import RoleManagerMetadataApplicationRoleConnection


def _assert_fields_set(metadata):
    """
    Asserts whether every attributes are set of the given role manager metadata.
    
    Parameters
    ----------
    metadata : ``RoleManagerMetadataApplicationRoleConnection``
        The metadata to assert.
    """
    vampytest.assert_instance(metadata, RoleManagerMetadataApplicationRoleConnection)


def test__RoleManagerMetadataApplicationRoleConnection__new__0():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.__new__`` works as intended.
    
    Case: No fields given.
    """
    metadata = RoleManagerMetadataApplicationRoleConnection()
    _assert_fields_set(metadata)


def test__RoleManagerMetadataApplicationRoleConnection__new__1():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.__new__`` works as intended.
    
    Case: all fields given
    """
    integration_id = 202301150000
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id,
    )
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.integration_id, integration_id)
