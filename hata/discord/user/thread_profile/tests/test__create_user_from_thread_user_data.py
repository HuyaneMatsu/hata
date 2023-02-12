import vampytest

from ....channel import ChannelType, create_partial_channel_from_id
from ....guild import Guild

from ...guild_profile import GuildProfile
from ...user import ClientUserBase, User

from ..utils import create_user_from_thread_user_data


def test__create_user_from_thread_user_data__0():
    """
    Tests whether ``create_user_from_thread_user_data`` works as intended.
    
    Case: only user id.
    """
    guild_id = 202302150000
    user_id = 202302150001
    channel_id = 202302150002
    
    channel = create_partial_channel_from_id(channel_id, ChannelType.guild_thread_public, guild_id)
    
    data = {
        'user_id': str(user_id),
    }
    
    user = create_user_from_thread_user_data(channel, data)
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    
    # test cache
    test_user = create_user_from_thread_user_data(channel, data)
    vampytest.assert_is(user, test_user)



def test__create_user_from_thread_user_data__1():
    """
    Tests whether ``create_user_from_thread_user_data`` works as intended.
    
    Case: with guild profile data.
    """
    guild_id = 202302150003
    user_id = 202302150004
    channel_id = 202302150005
    
    name = 'suika'
    nick = 'ibuki'
    
    guild = Guild.precreate(guild_id)
    channel = create_partial_channel_from_id(channel_id, ChannelType.guild_thread_public, guild_id)
    guild_profile = GuildProfile(nick = nick)
    
    data = {
        'user_id': str(user_id),
        'member': {
            **guild_profile.to_data(defaults = True),
            'user': {
                'id': str(user_id),
                **User(name = 'suika').to_data(defaults = True),
            }
        }
    }
    
    user = create_user_from_thread_user_data(channel, data)
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    
    # Extra data checks
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})
    vampytest.assert_eq(guild.users, {user_id: user})
    
    # test cache
    test_user = create_user_from_thread_user_data(channel, data)
    vampytest.assert_is(user, test_user)
