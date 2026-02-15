import vampytest

from ....user import GuildProfile, ClientUserBase

from ..fields import parse_user


def test__parse_user__user():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user.
    """
    user_id = 202602100010
    
    data = {
        'user': {
            'id': str(user_id),
        },
    }
    
    user = parse_user(data, 0)
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)


def test__parse_user__in_guild_user():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: in guild user.
    """
    user_id = 202602100011
    guild_id = 202602100012
    nick = 'Nomiya'
    
    data = {
        'user': {
            'id': str(user_id),
            'member': {
                'nick': nick,
            },
        },
    }
    
    
    user = parse_user(data, guild_id = guild_id)
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    
    guild_profile = user.get_guild_profile_for(guild_id)
    vampytest.assert_instance(guild_profile, GuildProfile)
    vampytest.assert_eq(guild_profile.nick, nick)
