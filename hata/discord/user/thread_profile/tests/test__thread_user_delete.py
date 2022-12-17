import vampytest

from ....channel import Channel, ChannelType
from ....user import User

from ..thread_profile import ThreadProfile
from ..utils import thread_user_create, thread_user_delete


def test__thread_user_delete():
    """
    Tests whether ``thread_user_delete`` works as intended.
    """
    thread_channel = Channel.precreate(202212150004, channel_type = ChannelType.guild_thread_public)
    user_1 = User.precreate(202212150005)
    user_2 = User.precreate(202212150006)
    thread_profile_1 = ThreadProfile(flags = 2)
    thread_profile_2 = ThreadProfile(flags = 4)
    
    thread_user_create(thread_channel, user_1, thread_profile_1.to_data(include_internals = True))
    thread_user_create(thread_channel, user_2, thread_profile_2.to_data(include_internals = True))
    
    thread_user_delete(thread_channel, user_1.id)
    vampytest.assert_eq(thread_channel.thread_users, {user_2.id: user_2})
    vampytest.assert_eq(user_1.thread_profiles, None)
    
    thread_user_delete(thread_channel, user_2.id)
    vampytest.assert_eq(thread_channel.thread_users, None)
    vampytest.assert_eq(user_1.thread_profiles, None)
