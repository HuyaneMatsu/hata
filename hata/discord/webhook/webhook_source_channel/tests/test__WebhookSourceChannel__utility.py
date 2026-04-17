import vampytest

from ....channel import Channel

from ..channel import WebhookSourceChannel

from .test__WebhookSourceChannel__constructor import _assert_fields_set


def test__WebhookSourceChannel__copy():
    """
    Tests whether ``WebhookSourceChannel.copy`` works as intended.
    """
    channel_id = 202302010007
    name = 'senya'
    
    channel = WebhookSourceChannel(
        channel_id = channel_id,
        name = name,
    )
    copy = channel.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel)
    
    vampytest.assert_eq(copy, channel)


def test__WebhookSourceChannel__copy_with__0():
    """
    Tests whether ``WebhookSourceChannel.copy_with`` works as intended.
    
    Case: No fields given.
    """
    channel_id = 202302010008
    name = 'senya'
    
    channel = WebhookSourceChannel(
        channel_id = channel_id,
        name = name,
    )
    copy = channel.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel)
    
    vampytest.assert_eq(copy, channel)


def test__WebhookSourceChannel__copy_with__1():
    """
    Tests whether ``WebhookSourceChannel.copy_with`` works as intended.
    """
    old_channel_id = 202302010009
    old_name = 'senya'
    new_channel_id = 202302010010
    new_name = 'yuuka'
    
    channel = WebhookSourceChannel(
        channel_id = old_channel_id,
        name = old_name,
    )
    copy = channel.copy_with(
        channel_id = new_channel_id,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel)

    vampytest.assert_eq(copy.id, new_channel_id)
    vampytest.assert_eq(copy.name, new_name)


def test__WebhookSourceChannel__channel():
    """
    Tests whether ``WebhookSourceChannel.channel`` works as intended.
    """
    channel_id = 202302010011
    name = 'senya'
    
    channel = WebhookSourceChannel(
        channel_id = channel_id,
        name = name,
    )
    
    source_channel = channel.channel
    vampytest.assert_instance(source_channel, Channel)
    vampytest.assert_eq(source_channel.id, channel_id)
    vampytest.assert_eq(source_channel.name, name)
