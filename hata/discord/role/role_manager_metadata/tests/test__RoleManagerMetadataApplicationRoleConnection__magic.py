import vampytest

from ..application_role_connection import RoleManagerMetadataApplicationRoleConnection


def test__RoleManagerMetadataApplicationRoleConnection__repr():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.__repr__`` works as intended.
    """
    integration_id = 202301150001
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id,
    )
    
    vampytest.assert_instance(repr(metadata), str)


def test__RoleManagerMetadataApplicationRoleConnection__hash():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.__hash__`` works as intended.
    """
    integration_id = 202301150002
    
    metadata = RoleManagerMetadataApplicationRoleConnection(
        integration_id = integration_id,
    )
    
    vampytest.assert_instance(hash(metadata), int)


def test__RoleManagerMetadataApplicationRoleConnection__eq():
    """
    Tests whether ``RoleManagerMetadataApplicationRoleConnection.__hash__`` works as intended.
    """
    integration_id = 202301150003
    
    keyword_parameters = {
        'integration_id': integration_id
    }
    
    metadata = RoleManagerMetadataApplicationRoleConnection(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('integration_id', 202301150004),
    ):
        test_metadata = RoleManagerMetadataApplicationRoleConnection(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
