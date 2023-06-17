import vampytest

from ....activity import Activity
from ....user import User, GuildProfile

from ..fields import parse_users__cache_presence, parse_users__no_cache_presence
from ..guild import Guild


def iter_options__cache_presence():
    user_id = 202306150003
    
    user_name = 'Koishi'
    user_nick = 'Koi'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    
    yield {}, {}
    yield {'members': None}, {}
    yield {'members': []}, {}
    yield (
        {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),   
                    'user': user.to_data(defaults = True, include_internals = True),
                }
            ]
        },
        {user_id: user},
    )


@vampytest._(vampytest.call_from(iter_options__cache_presence()).returning_last())
def test__parse_users__cache_presence(input_data):
    """
    Tests whether ``parse_users__cache_presence`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to pass.
    
    Returns
    -------
    output : `dict<int, Channel>`
    """
    guild_id = 202306150004
    guild = Guild.precreate(guild_id)
    
    output = parse_users__cache_presence(input_data, guild.users, guild_id)
    
    for user in output.values():
        vampytest.assert_true(guild_id in user.guild_profiles.keys())
    
    return output


def iter_options__no_cache_presence():
    user_id = 202306160000
    
    user_name = 'Koishi'
    user_nick = 'Koi'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    
    yield {}, {}
    yield {'members': None}, {}
    yield {'members': []}, {}
    yield (
        {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),   
                    'user': user.to_data(defaults = True, include_internals = True),
                }
            ]
        },
        {},
    )


@vampytest._(vampytest.call_from(iter_options__no_cache_presence()).returning_last())
def test__parse_users__no_cache_presence(input_data):
    """
    Tests whether ``parse_users__no_cache_presence`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to pass.
    
    Returns
    -------
    output : `dict<int, Channel>`
    """
    guild_id = 202306160001
    guild = Guild.precreate(guild_id)
    
    return parse_users__no_cache_presence(input_data, guild.users, guild_id)


def test__parse_users__cache_presence__with_presence():
    """
    Tests whether ``parse_users__cache_presence`` works as intended.
    
    Case: presence given too.
    """
    activity = Activity(name = 'Loving eyes')
    user_id = 202306160008
    guild_id = 202306160009
    
    user_name = 'Satori'
    user_nick = 'Sato'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    
    data = {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),   
                    'user': user.to_data(defaults = True, include_internals = True),
                }
            ],
            'presences': [
                {
                    'user': {
                        'id': str(user_id)
                    },
                    'activities': [
                        activity.to_data(include_internals = True),
                    ],
                },
            ]
        }
    
    guild = Guild.precreate(guild_id)
    
    output = parse_users__cache_presence(data, guild.users, guild_id)
    
    vampytest.assert_is(output, guild.users)
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.get_guild_profile_for(guild_id), guild_profile)
    vampytest.assert_eq(user.activity, activity)
