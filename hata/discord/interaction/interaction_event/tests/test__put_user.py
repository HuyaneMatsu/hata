import vampytest

from ....user import User, GuildProfile

from ..fields import put_user


def _iter_options():
    user = User.precreate(202210280009)
    guild_profile = GuildProfile()
    serialize_guild_id = 202210280010
    user.guild_profiles[serialize_guild_id] = guild_profile
    
    
    yield (
        user,
        False,
        0,
        {
            'user': user.to_data(
                defaults = False,
                include_internals = True,
            )
        },
    )
    
    yield (
        user,
        True,
        0,
        {
            'user': user.to_data(
                defaults = True,
                include_internals = True,
            )
        },
    )
    
    yield (
        user,
        False,
        serialize_guild_id,
        {
            'member': {
                **guild_profile.to_data(
                    defaults = False,
                    include_internals = True,
                ),
                'user': user.to_data(
                    defaults = False,
                    include_internals = True,
                )
            }
        },
    )
    
    yield (
        user,
        True,
        serialize_guild_id,
        {
            'member': {
                **guild_profile.to_data(
                    defaults = True,
                    include_internals = True,
                ),
                'user': user.to_data(
                    defaults = True,
                    include_internals = True,
                )
            }
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user(input_value, defaults, guild_id):
    """
    Tests whether ``put_user`` works as intended.
    
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
    return put_user(input_value, {}, defaults, guild_id = guild_id)
