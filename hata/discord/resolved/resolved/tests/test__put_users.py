import vampytest

from ....user import User, GuildProfile

from ..fields import put_users


def _iter_options():
    user_id = 202211050023
    guild_id = 202211050024
    user_name = 'Faker'
    user_nick = 'COLORS'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    user.guild_profiles[guild_id] = guild_profile
    
    
    yield (
        None,
        False,
        0,
        {},
    )
    
    yield (
        None,
        True,
        0,
        {
            'users': {},
            'members': {},
        },
    )
    
    yield (
        {
            user_id: user,
        },
            False,
            0,
        {
            'users': {
                str(user_id): user.to_data(defaults = False, include_internals = True),
            },
            'members': {},
        },
    )
    
    yield (
        {
            user_id: user,
        },
            False,
            guild_id,
        {
            'users': {
                str(user_id): user.to_data(defaults = False, include_internals = True),
            },
            'members': {
                str(user_id): guild_profile.to_data(defaults = False, include_internals = True),
            },
        },
    )
    
    yield (
        {
            user_id: user,
        },
            True,
            0,
        {
            'users': {
                str(user_id): user.to_data(defaults = True, include_internals = True),
            },
            'members': {},
        },
    )
    
    yield (
        {
            user_id: user,
        },
            True,
            guild_id,
        {
            'users': {
                str(user_id): user.to_data(defaults = True, include_internals = True),
            },
            'members': {
                str(user_id): guild_profile.to_data(defaults = True, include_internals = True),
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_users(input_value, defaults, guild_id):
    """
    Tests whether ``put_users`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, ClientUserBase>`
        Value to serialise.
    defaults : `bool`
        Whether default values should be serialised as well.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_users(input_value, {}, defaults, guild_id = guild_id)
