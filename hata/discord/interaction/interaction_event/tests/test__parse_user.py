import vampytest

from ....user import GuildProfile, ClientUserBase

from ..fields import parse_user


def test__parse_user__0():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user.
    """
    user_id = 202210280011
    
    data = {
        'user': {
            'id': str(user_id),
        }
    }
    
    user = parse_user(data, 0)
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)


def test__parse_user__1():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user.
    """
    user_id = 202210280012
    guild_id = 202210280013
    nick = 'Nomiya'
    
    data = {
        'member': {
            'nick': nick,
            'user': {
                'id': str(user_id),
            }
        }
    }
    
    
    user = parse_user(data, guild_id = guild_id)
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    
    guild_profile = user.get_guild_profile_for(guild_id)
    vampytest.assert_instance(guild_profile, GuildProfile)
    vampytest.assert_eq(guild_profile.nick, nick)
