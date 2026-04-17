import vampytest

from ..channel import WebhookSourceChannel

from .test__WebhookSourceChannel__constructor import _assert_fields_set


def test__WebhookSourceChannel__from_data():
    """
    Tests whether ``WebhookSourceChannel.from_data`` works as intended.
    """
    channel_id = 202302010002
    name = 'senya'
    
    data = {
        'id': str(channel_id),
        'name': name,
    }
    
    channel = WebhookSourceChannel.from_data(data)
    _assert_fields_set(channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.name, name)


def test__WebhookSourceChannel__to_data():
    """
    Tests whether ``WebhookSourceChannel.to_data`` works as intended.
    
    Case: Include defaults.
    """
    channel_id = 202302010025
    name = 'senya'
    
    channel = WebhookSourceChannel(
        channel_id = channel_id,
        name = name,
    )
    
    expected_output = {
        'id': str(channel_id),
        'name': name,
    }
    
    vampytest.assert_eq(
        channel.to_data(defaults = True),
        expected_output,
    )
