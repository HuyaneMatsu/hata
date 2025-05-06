import vampytest

from ...bases import Icon, IconType
from ...guild import GuildActivityOverview

from ..urls import CDN_ENDPOINT, guild_activity_overview_badge_icon_url_as


def _iter_options():
    guild_id = 202504240003
    yield (
        guild_id,
        None,
        {},
        None,
    )
    
    guild_id = 202504240004
    yield (
        guild_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    guild_id = 202504240005
    yield (
        guild_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/a_00000000000000000000000000000003.gif',
    )
    
    guild_id = 202504240006
    yield (
        guild_id,
        Icon(IconType.animated, 3),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_activity_overview_badge_icon_url_as(guild_id, icon, keyword_parameters):
    """
    Tests whether ``guild_activity_overview_badge_icon_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create guild activity overview for.
    
    icon : `None | Icon`
        Clan icon to create the guild activity overview with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    guild_activity_overview = GuildActivityOverview.precreate(guild_id, badge_icon = icon)
    output = guild_activity_overview_badge_icon_url_as(guild_activity_overview, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
