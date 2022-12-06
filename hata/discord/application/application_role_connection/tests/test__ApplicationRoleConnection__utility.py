import vampytest

from ...application_role_connection_metadata import (
    ApplicationRoleConnectionMetadata, ApplicationRoleConnectionMetadataType
)

from ..connection import ApplicationRoleConnection

from .test__ApplicationRoleConnection__constructor import _assert_is_all_attribute_set


def test__ApplicationRoleConnection__copy():
    """
    Tests whether ``ApplicationRoleConnection.copy`` works as intended.
    """
    platform_name = 'buta'
    platform_user_name = 'otome'
    metadata_values = {'old': '1'}
    
    connection = ApplicationRoleConnection(
        platform_name = platform_name,
        platform_user_name = platform_user_name,
        metadata_values = metadata_values,
    )
    copy = connection.copy()
    _assert_is_all_attribute_set(copy)
    vampytest.assert_is_not(copy, connection)
    vampytest.assert_eq(copy, connection)


def test__ApplicationRoleConnection__copy_with__0():
    """
    Tests whether ``ApplicationRoleConnection.copy_with`` works as intended.
    
    Case: No parameters.
    """
    platform_name = 'buta'
    platform_user_name = 'otome'
    metadata_values = {'old': '1'}
    
    connection = ApplicationRoleConnection(
        platform_name = platform_name,
        platform_user_name = platform_user_name,
        metadata_values = metadata_values,
    )
    copy = connection.copy_with()
    _assert_is_all_attribute_set(copy)
    vampytest.assert_is_not(copy, connection)
    vampytest.assert_eq(copy, connection)


def test__ApplicationRoleConnection__copy_with__1():
    """
    Tests whether ``ApplicationRoleConnection.copy_with`` works as intended.
    
    Case: All parameters.
    """
    old_platform_name = 'buta'
    new_platform_name = 'left'
    old_platform_user_name = 'otome'
    new_platform_user_name = 'behind'
    old_metadata_values = {'old': '1'}
    new_metadata_values = {'new': '1'}
    
    connection = ApplicationRoleConnection(
        platform_name = old_platform_name,
        platform_user_name = old_platform_user_name,
        metadata_values = old_metadata_values,
    )
    copy = connection.copy_with(
        platform_name = new_platform_name,
        platform_user_name = new_platform_user_name,
        metadata_values = new_metadata_values,
    )
    _assert_is_all_attribute_set(copy)
    vampytest.assert_is_not(copy, connection)
    
    vampytest.assert_eq(copy.platform_name, new_platform_name)
    vampytest.assert_eq(copy.platform_user_name, new_platform_user_name)
    vampytest.assert_eq(copy.metadata_values, new_metadata_values)



def test__ApplicationRoleConnection__translate_value():
    """
    Tests whether ``ApplicationRoleConnection.translate_value`` works as intended.
    """
    metadata_0 = ApplicationRoleConnectionMetadata(
        'koishi', ApplicationRoleConnectionMetadataType.integer_greater_or_equal
    )
    
    for input_metadata_values, input_metadata, expected_output in (
        (
            None,
            metadata_0,
            None,
        ), (
            {'satori': '56'},
            metadata_0,
            None,
        ), (
            {'koishi': '56'},
            metadata_0,
            56,
        ),(
            {'koishi': 'hallo'},
            metadata_0,
            None,
        ),
    ):
        connection = ApplicationRoleConnection(metadata_values = input_metadata_values)
        output = connection.translate_value(input_metadata)
        vampytest.assert_eq(output, expected_output)


def test__ApplicationRoleConnection__translate_values():
    """
    Tests whether ``ApplicationRoleConnection.translate_values`` works as intended.
    """
    metadata_0 = ApplicationRoleConnectionMetadata(
        'koishi', ApplicationRoleConnectionMetadataType.integer_greater_or_equal
    )
    metadata_1 = ApplicationRoleConnectionMetadata(
        'satori', ApplicationRoleConnectionMetadataType.boolean_equal
    )
    
    for input_metadata_values, input_metadatas, expected_output in (
        (
            None,
            [metadata_0, metadata_1],
            {},
        ), (
            {'satori': '56'},
            [metadata_0, metadata_1],
            {},
        ), (
            {'koishi': '56'},
            [metadata_0, metadata_1],
            {metadata_0: 56},
        ), (
            {'koishi': 'hallo', 'satori': '1'},
            [metadata_0, metadata_1],
            {metadata_1: True},
        ), (
            {'koishi': 'hallo', 'satori': '1'},
            [],
            {},
        ),
    ):
        connection = ApplicationRoleConnection(metadata_values = input_metadata_values)
        output = connection.translate_values(input_metadatas)
        vampytest.assert_eq(output, expected_output)
