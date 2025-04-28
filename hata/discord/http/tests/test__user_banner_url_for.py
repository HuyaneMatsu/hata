import vampytest

from ...bases import Icon, IconType
from ...user import GuildProfile, User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_banner_url_for


def _iter_options():
    guild_id = 202407160024
    
    user_id = 202407160025
    yield (
        user_id,
        None,
        0,
        None,
        guild_id,
        None,
    )
    
    user_id = 202407160049
    yield (
        user_id,
        Icon(IconType.static, 2),
        0,
        None,
        guild_id,
        None,
    )
    
    user_id = 202407160026
    yield (
        user_id,
        None,
        guild_id,
        None,
        guild_id,
        None,
    )
    
    user_id = 202407160027
    yield (
        user_id,
        None,
        guild_id,
        Icon(IconType.static, 2),
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160028
    yield (
        user_id,
        None,
        guild_id,
        Icon(IconType.animated, 3),
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_banner_url_for(
    user_id, icon, guild_profile_guild_id, guild_profile_icon, guild_id
):
    """
    Tests whether ``user_banner_url_for`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    icon : `None | Icon`
        Icon to use as the user's banner.
    
    guild_profile_guild_id : `int`
        Guild identifier for the user's guild profile.
    
    guild_profile_icon : `None | Icon`
        Icon for the user's guild profile's banner.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | str`
    """
    user = User.precreate(user_id, banner = icon)
    if guild_profile_guild_id:
        user.guild_profiles[guild_profile_guild_id] = GuildProfile(banner = guild_profile_icon)
    
    output = user_banner_url_for(user, guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
