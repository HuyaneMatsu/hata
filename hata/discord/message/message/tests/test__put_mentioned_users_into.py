import vampytest

from ....user import GuildProfile, User

from ..fields import put_mentioned_users_into


def _iter_options():
    user_id_0 = 202407200007
    user_id_1 = 202407200008
    guild_id = 202407200009
    name_0 = 'Orin'
    name_1 = 'Okuu'
    nick_0 = 'Dancing cat'
    
    user_0 = User.precreate(user_id_0, name = name_0)
    guild_profile_0 = GuildProfile(nick = nick_0)
    user_0.guild_profiles[guild_id] = guild_profile_0
    user_1 = User.precreate(user_id_1, name = name_1)

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
        {'mentions': []},
    )
    
    yield (
        (user_0, user_1),
        False,
        0,
        {
            'mentions': [
                user_0.to_data(defaults = False, include_internals = True),
                user_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        (user_0, user_1),
        True,
        0,
        {
            'mentions': [
                user_0.to_data(defaults = True, include_internals = True),
                user_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )
    
    yield (
        (user_0, user_1),
        False,
        guild_id,
        {
            'mentions': [
                {
                    **user_0.to_data(defaults = False, include_internals = True),
                    'member': guild_profile_0.to_data(defaults = False, include_internals = True),
                },
                user_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        (user_0, user_1),
        True,
        guild_id,
        {
            'mentions': [
                {
                    **user_0.to_data(defaults = True, include_internals = True),
                    'member': guild_profile_0.to_data(defaults = True, include_internals = True),
                },
                user_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mentioned_users_into(input_value, defaults, guild_id):
    """
    Tests whether ``put_mentioned_users_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<ClientUserBase>`
        Value to serialize.
    defaults : `bool`
        Whether to serialize default values as well.
    guild_id : `int`
        Guild identifier.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_mentioned_users_into(input_value, {}, defaults, guild_id = guild_id)
