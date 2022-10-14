import vampytest

from ....integration import Integration

from ..connection import Connection
from ..preinstanced import ConnectionType, ConnectionVisibility


def test__Connection__repr():
    """
    Tests whether ``Connection.__repr__` works as intended.
    """
    connection_id = 202210080003
    
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
    
    vampytest.assert_instance(repr(connection), str)


def test__Connection__repr():
    """
    Tests whether ``Connection.__repr__` works as intended.
    """
    connection_id_1 = 202210080004
    connection_id_2 = 202210080005
    
    friend_sync = True
    integrations = [Integration(name = 'majority')]
    name = 'silenced'
    revoked = True
    show_activity = True
    two_way_link = True
    type_ = ConnectionType.github
    verified = True
    visibility = ConnectionVisibility.everyone
    
    keyword_parameters = {
        'friend_sync': friend_sync,
        'integrations': integrations,
        'name': name,
        'revoked': revoked,
        'show_activity': show_activity,
        'two_way_link': two_way_link,
        'type_': type_,
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
        ('friend_sync', False),
        ('integrations', None),
        ('name', 'ichigo'),
        ('revoked', False),
        ('show_activity', False),
        ('two_way_link', False),
        ('type_', ConnectionType.youtube),
        ('verified', False),
        ('visibility', ConnectionVisibility.user_only),
    ):
        test_connection = Connection(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(connection, test_connection)
