import vampytest

from ....user import User, GuildProfile

from ..fields import parse_client_guild_profile__cache_presence, parse_client_guild_profile__no_cache_presence
from ..guild import Guild


def _iter_options__cache_presence():
    user_id_0 = 202306160002
    user_id_1 = 202306160007
    
    user_name = 'Koishi'
    user_nick = 'Koi'
    
    user_0 = User.precreate(
        user_id_0,
        name = user_name,
    )
    
    user_1 = User.precreate(
        user_id_1,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    
    yield {}, None, {}
    yield {'members': None}, None, {}
    yield {'members': []}, None, {}
    
    yield (
        {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),   
                    'user': user_0.to_data(defaults = True, include_internals = True),
                }
            ]
        },
        user_0,
        {},
    )
    
    yield (
        {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),   
                    'user': user_1.to_data(defaults = True, include_internals = True),
                }
            ]
        },
        user_1,
        {},
    )


@vampytest._(vampytest.call_from(_iter_options__cache_presence()).returning_last())
def test__parse_client_guild_profile__cache_presence(input_data, user_in_cache):
    """
    Tests whether ``parse_client_guild_profile__cache_presence`` works as intended.
    
    If presence caching is enabled it should do nothing.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to pass.
    user_in_cache : `None`, ``ClientUserBase``
        Additional parameter just to make sure that the user is kept cache.
    
    Returns
    -------
    output : `dict<int, Channel>`
    """
    guild_id = 202306160003
    guild = Guild.precreate(guild_id)
    
    return parse_client_guild_profile__cache_presence(input_data, guild.users, guild_id)


def _iter_options__no_cache_presence():
    user_id_0 = 202306160004
    user_id_1 = 202306160006
    
    user_name = 'Koishi'
    user_nick = 'Koi'
    
    user_0 = User.precreate(
        user_id_0,
        name = user_name,
    )
    
    user_1 = User.precreate(
        user_id_1,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    
    yield {}, None, {}
    yield {'members': None}, None, {}
    yield {'members': []}, None, {}
    
    yield (
        {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),   
                    'user': user_0.to_data(defaults = True, include_internals = True),
                }
            ]
        },
        user_0,
        {user_id_0: user_0},
    )
    
    yield (
        {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),   
                    'user': user_1.to_data(defaults = True, include_internals = True),
                }
            ]
        },
        None,
        {},
    )


@vampytest._(vampytest.call_from(_iter_options__no_cache_presence()).returning_last())
def test__parse_client_guild_profile__no_cache_presence(input_data, user_in_cache):
    """
    Tests whether ``parse_client_guild_profile__no_cache_presence`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to pass.
    user_in_cache : `None`, ``ClientUserBase``
        Additional parameter just to make sure that the user is kept cache.
    
    Returns
    -------
    output : `dict<int, Channel>`
    """
    guild_id = 202306160005
    guild = Guild.precreate(guild_id)
    
    return parse_client_guild_profile__no_cache_presence(input_data, guild.users, guild_id)
