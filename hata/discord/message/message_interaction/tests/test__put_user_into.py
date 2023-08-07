import vampytest

from ....user import GuildProfile, User

from ..fields import put_user_into


def _iter_options():
    user_0 = User.precreate(202304230003, name = 'Yuuka')
    user_1 = User.precreate(202304230004, name = 'Yukari')
    guild_profile_0 = GuildProfile(nick = 'Yuuma')
    guild_id_0 = 202304230005
    user_1.guild_profiles[guild_id_0] = guild_profile_0
    
    yield user_0, False, 0, {'user': user_0.to_data(defaults = False, include_internals = True)}
    yield user_0, False, guild_id_0, {'user': user_0.to_data(defaults = False, include_internals = True)}
    yield user_1, False, 0, {'user': user_1.to_data(defaults = False, include_internals = True)}
    yield (
        user_1,
        False,
        guild_id_0,
        {
            'user': user_1.to_data(defaults = False, include_internals = True),
            'member': guild_profile_0.to_data(defaults = False, include_internals = True),
        },
    )

    yield user_0, True, 0, {'user': user_0.to_data(defaults = True, include_internals = True)}
    yield user_0, True, guild_id_0, {'user': user_0.to_data(defaults = True, include_internals = True)}
    yield user_1, True, 0, {'user': user_1.to_data(defaults = True, include_internals = True)}
    yield (
        user_1,
        True,
        guild_id_0,
        {
            'user': user_1.to_data(defaults = True, include_internals = True),
            'member': guild_profile_0.to_data(defaults = True, include_internals = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_into(input_value, defaults, guild_id):
    """
    Tests whether ``put_user_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``ClientUserBase``
        Input value to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    guild_id : `int`
        The respective guild identifier.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_user_into(input_value, {}, defaults, guild_id = guild_id)
