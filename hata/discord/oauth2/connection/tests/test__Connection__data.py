import vampytest


from ....integration import Integration

from ..connection import Connection
from ..preinstanced import ConnectionType, ConnectionVisibility

from .test__Connection__constructor import _assert_fields_set


def test__Connection__from_data():
    """
    Tests whether ``Connection.from_data`` works as intended.
    """
    connection_id = 202210080007
    
    connection_type = ConnectionType.github
    friend_sync = True
    integrations = [Integration.precreate(202210140043, name = 'majority')]
    metadata_visibility = ConnectionVisibility.everyone
    name = 'silenced'
    revoked = True
    show_activity = True
    two_way_link = True
    verified = True
    visibility = ConnectionVisibility.everyone
    
    data = {
        'id': str(connection_id),
        'type': connection_type.value,
        'friend_sync': friend_sync,
        'integrations': [integration.to_data(include_internals = True) for integration in integrations],
        'metadata_visibility': metadata_visibility.value,
        'name': name,
        'revoked': revoked,
        'show_activity': show_activity,
        'two_way_link': two_way_link,
        'verified': verified,
        'visibility': visibility.value,
    }
    
    connection = Connection.from_data(data)
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


def test__Connection__to_data():
    """
    Tests whether ``Connection.to_data` works as intended.
    
    Case : defaults & include internals.
    """
    connection_id = 202210080008
    
    connection_type = ConnectionType.github
    friend_sync = True
    integrations = [Integration.precreate(202210140043, name = 'majority')]
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
    
    expected_data = {
        'id': str(connection_id),
        'friend_sync': friend_sync,
        'integrations': [
            integration.to_data(defaults = True, include_internals = True) for integration in integrations
        ],
        'metadata_visibility': metadata_visibility.value,
        'name': name,
        'revoked': revoked,
        'show_activity': show_activity,
        'two_way_link': two_way_link,
        'type': connection_type.value,
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
