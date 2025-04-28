import vampytest

from ...bases import Icon, IconType
from ...guild import Guild

from ..urls import CDN_ENDPOINT, guild_home_splash_url_as


def _iter_options():
    guild_id = 202504150001
    yield (
        guild_id,
        None,
        {},
        None,
    )
    
    guild_id = 202504150002
    yield (
        guild_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/home-headers/{guild_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    guild_id = 202504150003
    yield (
        guild_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/home-headers/{guild_id}/a_00000000000000000000000000000003.gif',
    )
    
    guild_id = 202504150004
    yield (
        guild_id,
        Icon(IconType.animated, 3),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/home-headers/{guild_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_home_splash_url_as(guild_id, icon, keyword_parameters):
    """
    Tests whether ``guild_home_splash_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create guild with.
    
    icon : `None | Icon`
        Icon to use as the guild's home splash.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    guild = Guild.precreate(guild_id, home_splash = icon)
    output = guild_home_splash_url_as(guild, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
