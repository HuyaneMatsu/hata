import vampytest

from ...bases import Icon, IconType
from ...guild import GuildActivityOverview

from ..urls import CDN_ENDPOINT, guild_activity_overview_badge_icon_url


def _iter_options():
    guild_id = 202504240000
    yield (
        guild_id,
        None,
        None,
    )
    
    guild_id = 202504240001
    yield (
        guild_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/00000000000000000000000000000002.png',
    )
    
    guild_id = 202504240002
    yield (
        guild_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_activity_overview_badge_icon_url(guild_id, icon):
    """
    Tests whether ``guild_activity_overview_badge_icon_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create guild activity overview for.
    
    icon : `None | Icon`
        Clan icon to create the guild activity overview with.
    
    Returns
    -------
    output : `None | str`
    """
    guild_activity_overview = GuildActivityOverview.precreate(guild_id, badge_icon = icon)
    output = guild_activity_overview_badge_icon_url(guild_activity_overview)
    vampytest.assert_instance(output, str, nullable = True)
    return output
