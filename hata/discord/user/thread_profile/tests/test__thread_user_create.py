import vampytest

from ....channel import Channel, ChannelType
from ....user import User

from ..thread_profile import ThreadProfile
from ..utils import thread_user_create


def test__thread_user_create():
    """
    Tests whether ``thread_user_create`` works as intended.
    """
    thread_channel = Channel.precreate(202212150000, channel_type = ChannelType.guild_thread_public)
    user = User.precreate(202212150001)
    thread_profile = ThreadProfile(flags = 2)
    
    thread_profile_data = thread_profile.to_data(include_internals = True)
    
    created = thread_user_create(thread_channel, user, thread_profile_data)
    vampytest.assert_true(created)
    
    vampytest.assert_eq(thread_channel.thread_users, {user.id: user})
    vampytest.assert_eq(user.thread_profiles, {thread_channel.id: thread_profile})
    
    created = thread_user_create(thread_channel, user, thread_profile_data)
    vampytest.assert_false(created)
