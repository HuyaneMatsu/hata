import vampytest

from ..channel import WebhookSourceChannel


def test__WebhookSourceChannel__repr():
    """
    Tests whether ``WebhookSourceChannel.__repr__`` works as intended.
    """
    channel_id = 202302010003
    name = 'senya'
    
    channel = WebhookSourceChannel(
        channel_id = channel_id,
        name = name,
    )
    vampytest.assert_instance(repr(channel), str)


def test__WebhookSourceChannel__hash():
    """
    Tests whether ``WebhookSourceChannel.__hash__`` works as intended.
    """
    channel_id = 202302010004
    name = 'senya'
    
    channel = WebhookSourceChannel(
        channel_id = channel_id,
        name = name,
    )
    vampytest.assert_instance(hash(channel), int)


def test__WebhookSourceChannel__eq():
    """
    Tests whether ``WebhookSourceChannel.__eq__`` works as intended.
    """
    channel_id = 202302010005
    name = 'senya'
    
    keyword_parameters = {
        'channel_id': channel_id,
        'name': name,
    }
    
    channel = WebhookSourceChannel(**keyword_parameters)
    vampytest.assert_eq(channel, channel)
    vampytest.assert_ne(channel, object())
    
    for field_name, field_value in (
        ('channel_id', 202302010006),
        ('name', 'yuuka'),
    ):
        test_channel = WebhookSourceChannel(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(channel, test_channel)
