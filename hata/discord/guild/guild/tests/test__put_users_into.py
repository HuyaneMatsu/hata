import vampytest

from ....user import User, GuildProfile

from ..fields import put_users_into


def _iter_options():
    user_id = 202306150005
    guild_id = 202306150006
    
    user_name = 'Koishi'
    user_nick = 'Koi'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    user.guild_profiles[guild_id] = guild_profile

    yield None, False, 0, {'members': []}
    yield None, True, 0, {'members': []}
    yield (
            {
                user_id: user,
            },
            True,
            None,
            {
                'members': [],
            },
        )
    yield (
        {
            user_id: user,
        },
        True,
        guild_id,
        {
            'members': [
                {
                    **guild_profile.to_data(defaults = True, include_internals = True),
                    'user': user.to_data(defaults = True, include_internals = True),
                },
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_users_into(users, defaults, guild_id):
    """
    Tests whether ``put_users_into`` works as intended.
    
    Parameters
    ----------
    users : `dict` of (`int`, ``ClientUserBase``) items
        Users to pass.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    guild_id : `int`
        Guild identifier to pass.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_users_into(users, {}, defaults, guild_id = guild_id)
