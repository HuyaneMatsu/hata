import vampytest


from ....integration import Integration

from ..connection import Connection
from ..preinstanced import ConnectionType, ConnectionVisibility

from .test__Connection__constructor import _check_is_every_attribute_set


def test__Connection__from_data():
    """
    Tests whether ``Connection.from_data`` works as intended.
    """
    connection_id = 202210080007
    
    friend_sync = True
    integrations = [Integration.precreate(202210140043, name = 'majority')]
    name = 'silenced'
    revoked = True
    show_activity = True
    two_way_link = True
    type_ = ConnectionType.github
    verified = True
    visibility = ConnectionVisibility.everyone
    
    data = {
        'id': str(connection_id),
        'friend_sync': friend_sync,
        'integrations': [integration.to_data(include_internals = True) for integration in integrations],
        'name': name,
        'revoked': revoked,
        'show_activity': show_activity,
        'two_way_link': two_way_link,
        'type': type_.value,
        'verified': verified,
        'visibility': visibility.value,
    }
    
    connection = Connection.from_data(data)
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


def test__Connection__to_data():
    """
    Tests whether ``Connection.to_data` works as intended.
    
    Case : defaults & include internals.
    """
    connection_id = 202210080008
    
    friend_sync = True
    integrations = [Integration.precreate(202210140043, name = 'majority')]
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
    
    expected_data = {
        'id': str(connection_id),
        'friend_sync': friend_sync,
        'integrations': [
            integration.to_data(defaults = True, include_internals = True) for integration in integrations
        ],
        'name': name,
        'revoked': revoked,
        'show_activity': show_activity,
        'two_way_link': two_way_link,
        'type': type_.value,
        'verified': verified,
        'visibility': visibility.value,
    }
    
    vampytest.assert_eq(
        connection.to_data(
            defaults = True,
            include_internals = True,
        ),
        expected_data,
    )
