import vampytest

from .. import CHANNEL_TYPES, Channel


def test__Channel__thread_users_0():
    """
    Tests whether `channel.thread_users` works as intended.
    
    Only testing for a thread channel obviously.
    """
    channel = Channel.precreate(20220808, channel_type=CHANNEL_TYPES.guild_thread_public)
    
    vampytest.assert_is(channel.thread_users, None)
    
    value = {}
    channel.thread_users = value
    vampytest.assert_is(channel.thread_users, value)
    
    channel.thread_users = None
    vampytest.assert_is(channel.thread_users, None)
