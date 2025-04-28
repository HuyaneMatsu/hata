import vampytest

from ...bases import Icon, IconType
from ...guild import GuildBadge

from ..urls import CDN_ENDPOINT, guild_badge_icon_url


def _iter_options():
    guild_id = 202405170017
    yield (
        guild_id,
        None,
        None,
    )
    
    guild_id = 202405170018
    yield (
        guild_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/00000000000000000000000000000002.png',
    )
    
    guild_id = 202405170019
    yield (
        guild_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_badge_icon_url(guild_id, icon):
    """
    Tests whether ``guild_badge_icon_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create badge for.
    
    icon : `None | Icon`
        Icon to create the guild badge with.
    
    Returns
    -------
    output : `None | str`
    """
    guild_badge = GuildBadge(guild_id = guild_id, icon = icon)
    output = guild_badge_icon_url(guild_badge)
    vampytest.assert_instance(output, str, nullable = True)
    return output
