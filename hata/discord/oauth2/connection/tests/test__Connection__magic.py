import vampytest

from ....integration import Integration

from ..connection import Connection
from ..preinstanced import ConnectionType, ConnectionVisibility


def test__Connection__repr():
    """
    Tests whether ``Connection.__repr__` works as intended.
    """
    connection_id = 202210080003
    
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
    
    vampytest.assert_instance(repr(connection), str)


def test__Connection__hash():
    """
    Tests whether ``Connection.__hash__` works as intended.
    """
    connection_id = 202302160003
    
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
    
    keyword_parameters = {
        'connection_type': connection_type,
        'friend_sync': friend_sync,
        'integrations': integrations,
        'metadata_visibility': metadata_visibility,
        'name': name,
        'revoked': revoked,
        'show_activity': show_activity,
        'two_way_link': two_way_link,
        'verified': verified,
        'visibility': visibility,
    }
    
    connection = Connection.precreate(connection_id, **keyword_parameters)
    vampytest.assert_instance(hash(connection), int)

    connection = Connection(**keyword_parameters)
    vampytest.assert_instance(hash(connection), int)


def test__Connection__eq():
    """
    Tests whether ``Connection.__repr__` works as intended.
    """
    connection_id_1 = 202210080004
    connection_id_2 = 202210080005
    
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
    
    keyword_parameters = {
        'connection_type': connection_type,
        'friend_sync': friend_sync,
        'integrations': integrations,
        'metadata_visibility': metadata_visibility,
        'name': name,
        'revoked': revoked,
        'show_activity': show_activity,
        'two_way_link': two_way_link,
        'verified': verified,
        'visibility': visibility,
    }
    
    connection = Connection.precreate(
        connection_id_1,
        **keyword_parameters
    )
    
    vampytest.assert_eq(connection, connection)
    vampytest.assert_ne(connection, object())
    
    test_connection = Connection.precreate(
        connection_id_2,
        **keyword_parameters
    )
    
    vampytest.assert_ne(connection, test_connection)
    
    test_connection = Connection(
        **keyword_parameters
    )
    
    vampytest.assert_eq(connection, test_connection)
    
    for field_name, field_value in (
        ('connection_type', ConnectionType.youtube),
        ('friend_sync', False),
        ('integrations', None),
        ('metadata_visibility', ConnectionVisibility.user_only),
        ('name', 'ichigo'),
        ('revoked', False),
        ('show_activity', False),
        ('two_way_link', False),
        ('verified', False),
        ('visibility', ConnectionVisibility.user_only),
    ):
        test_connection = Connection(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(connection, test_connection)
