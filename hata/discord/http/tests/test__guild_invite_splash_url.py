import vampytest

from ...bases import Icon, IconType
from ...guild import Guild

from ..urls import CDN_ENDPOINT, guild_invite_splash_url


def _iter_options():
    guild_id = 202504160040
    yield (
        guild_id,
        None,
        None,
    )
    
    guild_id = 202504160041
    yield (
        guild_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/splashes/{guild_id}/00000000000000000000000000000002.png',
    )
    
    guild_id = 202504160042
    yield (
        guild_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/splashes/{guild_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_invite_splash_url(guild_id, icon):
    """
    Tests whether ``guild_invite_splash_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create guild for.
    
    icon : `None | Icon`
        Icon to use as the guild's invite splash.
    
    Returns
    -------
    output : `None | str`
    """
    guild = Guild.precreate(guild_id, invite_splash = icon)
    output = guild_invite_splash_url(guild)
    vampytest.assert_instance(output, str, nullable = True)
    return output
