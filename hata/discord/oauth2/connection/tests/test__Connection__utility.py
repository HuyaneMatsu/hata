import vampytest

from ....integration import Integration

from ..connection import Connection
from ..preinstanced import ConnectionType, ConnectionVisibility

from .test__Connection__constructor import _assert_fields_set


def test__Connection__iter_integrations():
    """
    Tests whether ``Connection.iter_integrations` works as intended.
    """
    integration = Integration.precreate(202210080006)
    
    for input_integrations, expected_output in (
        (None, []),
        ([integration], [integration]),
    ):
        connection = Connection(integrations = input_integrations)
        vampytest.assert_eq([*connection.iter_integrations()], expected_output)


def test__Connection__copy():
    """
    Tests whether ``Connection.copy`` works as intended.
    """
    connection_type = ConnectionType.github
    friend_sync = True
    integrations = [Integration(name = 'majority')]
    metadata_visibility = ConnectionVisibility.everyone
    name = 'silenced'
    revoked = True
    show_activity = True
    two_way_link = True
    verified = True
    visibility = ConnectionVisibility.everyone
    
    connection = Connection(
        connection_type = connection_type,
        friend_sync = friend_sync,
        integrations = integrations,
        metadata_visibility = metadata_visibility,
        name = name,
        revoked = revoked,
        show_activity = show_activity,
        two_way_link = two_way_link,
        verified = verified,
        visibility = visibility,
    )
    
    copy = connection.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(connection, copy)
    
    vampytest.assert_eq(connection, copy)


def test__Connection__copy_with__0():
    """
    Tests whether ``Connection.copy_with`` works as intended.
    
    Case: No fields given.
    """
    connection_type = ConnectionType.github
    friend_sync = True
    integrations = [Integration(name = 'majority')]
    metadata_visibility = ConnectionVisibility.everyone
    name = 'silenced'
    revoked = True
    show_activity = True
    two_way_link = True
    verified = True
    visibility = ConnectionVisibility.everyone
    
    connection = Connection(
        connection_type = connection_type,
        friend_sync = friend_sync,
        integrations = integrations,
        metadata_visibility = metadata_visibility,
        name = name,
        revoked = revoked,
        show_activity = show_activity,
        two_way_link = two_way_link,
        verified = verified,
        visibility = visibility,
    )
    
    copy = connection.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(connection, copy)
    
    vampytest.assert_eq(connection, copy)


def test__Connection__copy_with__1():
    """
    Tests whether ``Connection.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_connection_type = ConnectionType.github
    old_friend_sync = True
    old_integrations = [Integration(name = 'majority')]
    old_metadata_visibility = ConnectionVisibility.everyone
    old_name = 'silenced'
    old_revoked = True
    old_show_activity = True
    old_two_way_link = True
    old_verified = True
    old_visibility = ConnectionVisibility.everyone
    
    new_connection_type = ConnectionType.youtube
    new_friend_sync = True
    new_integrations = [Integration(name = 'crimson')]
    new_metadata_visibility = ConnectionVisibility.user_only
    new_name = 'sky'
    new_revoked = False
    new_show_activity = False
    new_two_way_link = False
    new_verified = False
    new_visibility = ConnectionVisibility.user_only
    
    connection = Connection(
        connection_type = old_connection_type,
        friend_sync = old_friend_sync,
        integrations = old_integrations,
        metadata_visibility = old_metadata_visibility,
        name = old_name,
        revoked = old_revoked,
        show_activity = old_show_activity,
        two_way_link = old_two_way_link,
        verified = old_verified,
        visibility = old_visibility,
    )
    
    copy = connection.copy_with(
        connection_type = new_connection_type,
        friend_sync = new_friend_sync,
        integrations = new_integrations,
        metadata_visibility = new_metadata_visibility,
        name = new_name,
        revoked = new_revoked,
        show_activity = new_show_activity,
        two_way_link = new_two_way_link,
        verified = new_verified,
        visibility = new_visibility,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(connection, copy)
    

    vampytest.assert_is(copy.type, new_connection_type)
    vampytest.assert_eq(copy.friend_sync, new_friend_sync)
    vampytest.assert_eq(copy.integrations, tuple(new_integrations))
    vampytest.assert_is(copy.metadata_visibility, new_metadata_visibility)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.revoked, new_revoked)
    vampytest.assert_eq(copy.show_activity, new_show_activity)
    vampytest.assert_eq(copy.two_way_link, new_two_way_link)
    vampytest.assert_eq(copy.verified, new_verified)
    vampytest.assert_is(copy.visibility, new_visibility)
