import vampytest

from ...bases import Icon, IconType
from ...user import GuildProfile, User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_avatar_url_at


def _iter_options():
    guild_id = 202407160050
    
    user_id = 202407160051
    user = User.precreate(user_id)
    
    yield (
        user,
        guild_id,
        'https://cdn.discordapp.com/embed/avatars/5.png',
    )
    
    user_id = 202407160052
    user = User.precreate(user_id, avatar = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/avatars/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160053
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = None)
    
    yield (
        user,
        guild_id,
        'https://cdn.discordapp.com/embed/avatars/5.png',
    )
    
    user_id = 202407160054
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160055
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.animated, 3))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_avatar_url_at(user, guild_id):
    """
    Tests whether ``user_avatar_url_at`` works as intended.
    
    Parameters
    ----------
    user : ``User``
        User to get its avatar url of.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | str`
    """
    output = user_avatar_url_at(user, guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
