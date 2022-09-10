import vampytest

from .. import Channel, ChannelType


def test__Channel__thread_users__0():
    """
    Tests whether `channel.thread_users` works as intended.
    
    Only testing for a thread channel obviously.
    """
    channel = Channel.precreate(20220808, channel_type = ChannelType.guild_thread_public)
    
    vampytest.assert_is(channel.thread_users, None)
    
    value = {}
    channel.thread_users = value
    vampytest.assert_is(channel.thread_users, value)
    
    channel.thread_users = None
    vampytest.assert_is(channel.thread_users, None)
