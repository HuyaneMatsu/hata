import vampytest

from ..connection import ApplicationRoleConnection

from .test__ApplicationRoleConnection__constructor import _assert_is_all_attribute_set


def test__ApplicationRoleConnection__from_data():
    """
    Tests whether ``ApplicationRoleConnection.from_data`` works as intended.
    """
    platform_name = 'buta'
    platform_user_name = 'otome'
    metadata_values = {'old': '1'}
    
    data = {
        'platform_name': platform_name,
        'platform_username': platform_user_name,
        'metadata': metadata_values,
    }
    
    connection = ApplicationRoleConnection.from_data(data)
    _assert_is_all_attribute_set(connection)
    
    vampytest.assert_eq(connection.platform_name, platform_name)
    vampytest.assert_eq(connection.platform_user_name, platform_user_name)
    vampytest.assert_eq(connection.metadata_values, metadata_values)



def test__ApplicationRoleConnection__to_data():
    """
    Tests whether ``ApplicationRoleConnection.to_data`` works as intended.
    
    Case: Include defaults
    """
    platform_name = 'buta'
    platform_user_name = 'otome'
    metadata_values = {'old': '1'}
    
    connection = ApplicationRoleConnection(
        platform_name = platform_name,
        platform_user_name = platform_user_name,
        metadata_values = metadata_values,
    )
    
    expected_data = {
        'platform_name': platform_name,
        'platform_username': platform_user_name,
        'metadata': metadata_values,
    }
    
    vampytest.assert_eq(
        connection.to_data(defaults = True),
        expected_data,
    )
