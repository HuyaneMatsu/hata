import vampytest

from ...bases import Icon, IconType
from ...user import GuildProfile, User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_avatar_url_for


def _iter_options():
    guild_id = 202407160019
    
    user_id = 202407160020
    yield (
        user_id,
        None,
        0,
        None,
        guild_id,
        None,
    )
    
    user_id = 202407160047
    yield (
        user_id,
        Icon(IconType.static, 2),
        0,
        None,
        guild_id,
        None,
    )
    
    user_id = 202407160021
    yield (
        user_id,
        None,
        guild_id,
        None,
        guild_id,
        None,
    )
    
    user_id = 202407160022
    yield (
        user_id,
        None,
        guild_id,
        Icon(IconType.static, 2),
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160023
    yield (
        user_id,
        None,
        guild_id,
        Icon(IconType.animated, 3),
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_avatar_url_for(user_id, icon, guild_profile_guild_id, guild_profile_icon, guild_id):
    """
    Tests whether ``user_avatar_url_for`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    icon : `None | Icon`
        Icon to use as the user's avatar.
    
    guild_profile_guild_id : `int`
        Guild identifier for the user's guild profile.
    
    guild_profile_icon : `None | Icon`
        Icon for the user's guild profile's avatar.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | str`
    """
    user = User.precreate(user_id, avatar = icon)
    if guild_profile_guild_id:
        user.guild_profiles[guild_profile_guild_id] = GuildProfile(avatar = guild_profile_icon)
    
    output = user_avatar_url_for(user, guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
