import vampytest

from ....channel import Channel, ChannelType
from ....user import User

from ..thread_profile import ThreadProfile
from ..utils import thread_user_create, thread_user_difference_update


def test__thread_user_difference_update():
    """
    Tests whether ``thread_user_difference_update`` works as intended.
    """
    thread_channel = Channel.precreate(202212150002, channel_type = ChannelType.guild_thread_public)
    user = User.precreate(202212150003)
    thread_profile_old = ThreadProfile(flags = 2)
    thread_profile_new = ThreadProfile(flags = 4)
    
    thread_profile_data = thread_profile_old.to_data(include_internals = True)
    thread_user_create(thread_channel, user, thread_profile_data)
    
    old_attributes = thread_user_difference_update(thread_channel, user, thread_profile_data)
    vampytest.assert_is(old_attributes, None)
    
    thread_profile_data = thread_profile_new.to_data(include_internals = True)
    
    old_attributes = thread_user_difference_update(thread_channel, user, thread_profile_data)
    vampytest.assert_eq(old_attributes, {'flags': thread_profile_old.flags})
