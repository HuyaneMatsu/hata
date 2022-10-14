import vampytest

from ....integration import Integration

from ..connection import Connection
from ..preinstanced import ConnectionType, ConnectionVisibility


def _check_is_every_attribute_set(connection):
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
    _check_is_every_attribute_set(connection)


def test__Connection__new__1():
    """
    Tests whether ``Connection.__new__`` works as intended.
    
    Case: All parameters.
    """
    friend_sync = True
    integrations = [Integration(name = 'majority')]
    name = 'silenced'
    revoked = True
    show_activity = True
    two_way_link = True
    type_ = ConnectionType.github
    verified = True
    visibility = ConnectionVisibility.everyone
    
    connection = Connection(
        friend_sync = friend_sync,
        integrations = integrations,
        name = name,
        revoked = revoked,
        show_activity = show_activity,
        two_way_link = two_way_link,
        type_ = type_,
        verified = verified,
        visibility = visibility,
    )
    
    _check_is_every_attribute_set(connection)
    
    vampytest.assert_eq(connection.friend_sync, friend_sync)
    vampytest.assert_eq(connection.integrations, tuple(integrations))
    vampytest.assert_eq(connection.name, name)
    vampytest.assert_eq(connection.revoked, revoked)
    vampytest.assert_eq(connection.show_activity, show_activity)
    vampytest.assert_eq(connection.two_way_link, two_way_link)
    vampytest.assert_is(connection.type, type_)
    vampytest.assert_eq(connection.verified, verified)
    vampytest.assert_is(connection.visibility, visibility)


def test__Connection__create_empty():
    """
    Tests whether ``Connection._create_empty` works as intended.
    """
    connection_id = 202210080000
    
    connection = Connection._create_empty(connection_id)
    _check_is_every_attribute_set(connection)
    vampytest.assert_eq(connection.id, connection_id)



def test__Connection__precreate__0():
    """
    Tests whether ``Connection.precreate` works as intended.
    
    Case: No parameters.
    """
    connection_id = 202210080001
    connection = Connection.precreate(connection_id)
    _check_is_every_attribute_set(connection)
    vampytest.assert_eq(connection.id, connection_id)


def test__Connection__precreate_1():
    """
    Tests whether ``Connection.__new__`` works as intended.
    
    Case: All parameters.
    """
    connection_id = 202210080002
    
    friend_sync = True
    integrations = [Integration(name = 'majority')]
    name = 'silenced'
    revoked = True
    show_activity = True
    two_way_link = True
    type_ = ConnectionType.github
    verified = True
    visibility = ConnectionVisibility.everyone
    
    connection = Connection.precreate(
        connection_id,
        friend_sync = friend_sync,
        integrations = integrations,
        name = name,
        revoked = revoked,
        show_activity = show_activity,
        two_way_link = two_way_link,
        type_ = type_,
        verified = verified,
        visibility = visibility,
    )
    
    _check_is_every_attribute_set(connection)
    vampytest.assert_eq(connection.id, connection_id)
    
    vampytest.assert_eq(connection.friend_sync, friend_sync)
    vampytest.assert_eq(connection.integrations, tuple(integrations))
    vampytest.assert_eq(connection.name, name)
    vampytest.assert_eq(connection.revoked, revoked)
    vampytest.assert_eq(connection.show_activity, show_activity)
    vampytest.assert_eq(connection.two_way_link, two_way_link)
    vampytest.assert_is(connection.type, type_)
    vampytest.assert_eq(connection.verified, verified)
    vampytest.assert_is(connection.visibility, visibility)
