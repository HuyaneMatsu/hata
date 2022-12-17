import vampytest

from ....channel import Channel, ChannelType
from ....client import Client
from ....user import User

from ..thread_profile import ThreadProfile
from ..utils import thread_user_create, thread_user_pop


def test__thread_user_pop__0():
    """
    Tests whether ``thread_user_pop`` works as intended.
    
    Case: no client.
    """
    client = Client(
        token = 'token_20221215_0000',
    )
    
    try:
        thread_channel = Channel.precreate(202212150007, channel_type = ChannelType.guild_thread_public)
        user_1 = User.precreate(202212150008)
        user_2 = User.precreate(202212150009)
        thread_profile_1 = ThreadProfile(flags = 2)
        thread_profile_2 = ThreadProfile(flags = 4)
        
        thread_user_create(thread_channel, user_1, thread_profile_1.to_data(include_internals = True))
        thread_user_create(thread_channel, user_2, thread_profile_2.to_data(include_internals = True))
        
        thread_user_pop(thread_channel, user_1.id, client)
        vampytest.assert_eq(thread_channel.thread_users, {user_2.id: user_2})
        vampytest.assert_eq(user_1.thread_profiles, None)
        
        thread_user_pop(thread_channel, user_2.id, client)
        vampytest.assert_eq(thread_channel.thread_users, None)
        vampytest.assert_eq(user_1.thread_profiles, None)

    # Cleanup
    finally:
        client._delete()
        client = None


def test__thread_user_pop__1():
    """
    Tests whether ``thread_user_pop`` works as intended.
    
    Case: popping self.
    """
    client_id = 202212150010
    
    client = Client(
        token = 'token_20221215_0001',
        client_id = client_id,
    )
    
    try:
        thread_channel = Channel.precreate(202212150011, channel_type = ChannelType.guild_thread_public)
        thread_profile = ThreadProfile(flags = 2)
        
        thread_user_create(thread_channel, client, thread_profile.to_data(include_internals = True))
        
        thread_user_pop(thread_channel, client.id, client)
        vampytest.assert_eq(thread_channel.thread_users, None)
        vampytest.assert_eq(client.thread_profiles, None)

    # Cleanup
    finally:
        client._delete()
        client = None


def test__thread_user_pop__2():
    """
    Tests whether ``thread_user_pop`` works as intended.
    
    Case: popping by client.
    """
    client_id_0 = 202212150012
    client_id_1 = 202212150013
    
    client_0 = Client(
        token = 'token_20221215_0002',
        client_id = client_id_0,
    )
    
    client_1 = Client(
        token = 'token_20221215_0003',
        client_id = client_id_1,
    )
    
    try:
        thread_channel = Channel.precreate(202212150014, channel_type = ChannelType.guild_thread_public)
        thread_profile = ThreadProfile(flags = 4)
        
        thread_user_create(thread_channel, client_0, thread_profile.to_data(include_internals = True))
        
        thread_user_pop(thread_channel, client_id_0, client_1)
        vampytest.assert_eq(thread_channel.thread_users, {client_id_0: client_0})
        vampytest.assert_eq(client_0.thread_profiles, {thread_channel.id: thread_profile})

    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
