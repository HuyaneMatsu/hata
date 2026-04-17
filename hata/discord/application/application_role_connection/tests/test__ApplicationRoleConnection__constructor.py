import vampytest

from ..connection import ApplicationRoleConnection


def _assert_is_all_attribute_set(connection):
    """
    Asserts whether every attributes are set of the given connection.
    
    Parameters
    ----------
    connection : ``ApplicationRoleConnection``
        The connection to check.
    """
    vampytest.assert_instance(connection, ApplicationRoleConnection)
    vampytest.assert_instance(connection.platform_name, str, nullable = True)
    vampytest.assert_instance(connection.platform_user_name, str, nullable = True)
    vampytest.assert_instance(connection.metadata_values, dict, nullable = True)


def test__ApplicationRoleConnection__new__0():
    """
    Tests whether ``ApplicationRoleConnection.__new__`` works as intended.
    
    Case : No fields given.
    """
    connection = ApplicationRoleConnection()
    _assert_is_all_attribute_set(connection)

    
def test__ApplicationRoleConnection__new__1():
    """
    Tests whether ``ApplicationRoleConnection.__new__`` works as intended.
    
    Case : All fields given.
    """
    platform_name = 'buta'
    platform_user_name = 'otome'
    metadata_values = {'old': '1'}
    
    connection = ApplicationRoleConnection(
        platform_name = platform_name,
        platform_user_name = platform_user_name,
        metadata_values = metadata_values,
    )
    _assert_is_all_attribute_set(connection)
    
    vampytest.assert_eq(connection.platform_name, platform_name)
    vampytest.assert_eq(connection.platform_user_name, platform_user_name)
    vampytest.assert_eq(connection.metadata_values, metadata_values)
