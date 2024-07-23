import vampytest

from ...bases import Icon, IconType
from ...user import GuildProfile, User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_banner_url_for


def _iter_options():
    guild_id = 202407160024
    
    user_id = 202407160025
    user = User.precreate(user_id)
    
    yield (
        user,
        guild_id,
        None,
    )
    
    user_id = 202407160049
    user = User.precreate(user_id, banner = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        None,
    )
    
    user_id = 202407160026
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(banner = None)
    
    yield (
        user,
        guild_id,
        None,
    )
    
    user_id = 202407160027
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(banner = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160028
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(banner = Icon(IconType.animated, 3))
    
    yield (
        user,
        guild_id,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_banner_url_for(user, guild_id):
    """
    Tests whether ``user_banner_url_for`` works as intended.
    
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
    output = user_banner_url_for(user, guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
