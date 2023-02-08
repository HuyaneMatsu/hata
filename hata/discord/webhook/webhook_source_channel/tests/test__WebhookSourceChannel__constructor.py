import vampytest

from ....channel import Channel, ChannelType

from ..channel import WebhookSourceChannel


def _assert_fields_set(channel):
    """
    Asserts whether every fields are set of the given webhook source channel.
    
    Parameters
    ----------
    channel : ``WebhookSourceChannel``
        The webhook source channel to check.
    """
    vampytest.assert_instance(channel, WebhookSourceChannel)
    vampytest.assert_instance(channel.id, int)
    vampytest.assert_instance(channel.name, str)


def test__WebhookSourceChannel__new__0():
    """
    Tests whether ``WebhookSourceChannel.__new__`` works as intended.
    
    Case: No fields given.
    """
    channel = WebhookSourceChannel()
    _assert_fields_set(channel)


def test__WebhookSourceChannel__new__1():
    """
    Tests whether ``WebhookSourceChannel.__new__`` works as intended.
    
    Case: All fields given.
    """
    channel_id = 202302010000
    name = 'senya'
    
    channel = WebhookSourceChannel(
        channel_id = channel_id,
        name = name,
    )
    _assert_fields_set(channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.name, name)


def test__WebhookSourceChannel__from_channel():
    """
    Tests whether ``WebhookSourceChannel.from_channel`` works as intended.
    """
    channel_id = 202302010001
    name = 'senya'
    
    source_channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = name,
    )
    
    channel = WebhookSourceChannel.from_channel(source_channel)
    _assert_fields_set(channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.name, name)
