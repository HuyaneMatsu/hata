import vampytest

from ...bases import Icon, IconType
from ...user import GuildProfile, User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_banner_url_at


def _iter_options():
    guild_id = 202407160056
    
    user_id = 202407160057
    user = User.precreate(user_id)
    
    yield (
        user,
        guild_id,
        None,
    )
    
    user_id = 202407160058
    user = User.precreate(user_id, banner = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/banners/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160059
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(banner = None)
    
    yield (
        user,
        guild_id,
        None,
    )
    
    user_id = 202407160060
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(banner = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160061
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(banner = Icon(IconType.animated, 3))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_banner_url_at(user, guild_id):
    """
    Tests whether ``user_banner_url_at`` works as intended.
    
    Parameters
    ----------
    user : ``User``
        User to get its banner url of.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | str`
    """
    output = user_banner_url_at(user, guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
