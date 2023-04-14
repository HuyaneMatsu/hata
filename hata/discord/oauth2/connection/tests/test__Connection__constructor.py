import vampytest

from ....integration import Integration

from ..connection import Connection
from ..preinstanced import ConnectionType, ConnectionVisibility


def _assert_fields_set(connection):
    """
    Tests whether every attribute of ``Connection`` is set.
    
    Parameters
    ----------
    connection : ``Connection``
        The connection to check.
    """
    vampytest.assert_instance(connection, Connection)
    
    vampytest.assert_instance(connection.id, int)
    vampytest.assert_instance(connection.friend_sync, bool)
    vampytest.assert_instance(connection.integrations, tuple, nullable = True)
    vampytest.assert_instance(connection.metadata_visibility, ConnectionVisibility)
    vampytest.assert_instance(connection.name, str)
    vampytest.assert_instance(connection.revoked, bool)
    vampytest.assert_instance(connection.show_activity, bool)
    vampytest.assert_instance(connection.two_way_link, bool)
    vampytest.assert_instance(connection.type, ConnectionType)
    vampytest.assert_instance(connection.verified, bool)
    vampytest.assert_instance(connection.visibility, ConnectionVisibility)


def test__Connection__new__0():
    """
    Tests whether ``Connection.__new__` works as intended.
    
    Case: No parameters.
    """
    connection = Connection()
    _assert_fields_set(connection)


def test__Connection__new__1():
    """
    Tests whether ``Connection.__new__`` works as intended.
    
    Case: All parameters.
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
    
    _assert_fields_set(connection)
    
    vampytest.assert_is(connection.type, connection_type)
    vampytest.assert_eq(connection.friend_sync, friend_sync)
    vampytest.assert_eq(connection.integrations, tuple(integrations))
    vampytest.assert_is(connection.metadata_visibility, metadata_visibility)
    vampytest.assert_eq(connection.name, name)
    vampytest.assert_eq(connection.revoked, revoked)
    vampytest.assert_eq(connection.show_activity, show_activity)
    vampytest.assert_eq(connection.two_way_link, two_way_link)
    vampytest.assert_eq(connection.verified, verified)
    vampytest.assert_is(connection.visibility, visibility)


def test__Connection__create_empty():
    """
    Tests whether ``Connection._create_empty` works as intended.
    """
    connection_id = 202210080000
    
    connection = Connection._create_empty(connection_id)
    _assert_fields_set(connection)
    vampytest.assert_eq(connection.id, connection_id)



def test__Connection__precreate__0():
    """
    Tests whether ``Connection.precreate` works as intended.
    
    Case: No parameters.
    """
    connection_id = 202210080001
    connection = Connection.precreate(connection_id)
    _assert_fields_set(connection)
    vampytest.assert_eq(connection.id, connection_id)


def test__Connection__precreate_1():
    """
    Tests whether ``Connection.__new__`` works as intended.
    
    Case: All parameters.
    """
    connection_id = 202210080002
    
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
    
    connection = Connection.precreate(
        connection_id,
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
    
    _assert_fields_set(connection)
    vampytest.assert_eq(connection.id, connection_id)
    
    vampytest.assert_is(connection.type, connection_type)
    vampytest.assert_eq(connection.friend_sync, friend_sync)
    vampytest.assert_eq(connection.integrations, tuple(integrations))
    vampytest.assert_is(connection.metadata_visibility, metadata_visibility)
    vampytest.assert_eq(connection.name, name)
    vampytest.assert_eq(connection.revoked, revoked)
    vampytest.assert_eq(connection.show_activity, show_activity)
    vampytest.assert_eq(connection.two_way_link, two_way_link)
    vampytest.assert_eq(connection.verified, verified)
    vampytest.assert_is(connection.visibility, visibility)
