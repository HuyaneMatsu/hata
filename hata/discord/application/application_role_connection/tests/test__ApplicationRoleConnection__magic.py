import vampytest

from ..connection import ApplicationRoleConnection


def test__ApplicationRoleConnection__repr():
    """
    Tests whether ``ApplicationRoleConnection.__repr__`` works as intended.
    
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
    
    vampytest.assert_instance(repr(connection), str)


def test__ApplicationRoleConnection__hash():
    """
    Tests whether ``ApplicationRoleConnection.__hash__`` works as intended.
    
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
    
    vampytest.assert_instance(hash(connection), int)


def test__ApplicationRoleConnection__eq():
    """
    Tests whether ``ApplicationRoleConnection.__eq__`` works as intended.
    
    Case: Include defaults
    """
    platform_name = 'buta'
    platform_user_name = 'otome'
    metadata_values = {'old': '1'}
    
    keyword_parameters = {
        'platform_name': platform_name,
        'platform_user_name': platform_user_name,
        'metadata_values': metadata_values,
    }
    
    connection = ApplicationRoleConnection(**keyword_parameters)
    
    vampytest.assert_eq(connection, connection)
    vampytest.assert_ne(connection, object())
    
    for field_name, field_value in (
        ('platform_name', None),
        ('platform_user_name', None),
        ('metadata_values', None),
    ):
        test_connection = ApplicationRoleConnection(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(connection, test_connection)
