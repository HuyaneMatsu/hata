import vampytest

from ...bases import Icon, IconType
from ...user import UserClan

from ..urls import CDN_ENDPOINT, clan_icon_url_as


def _iter_options():
    guild_id = 202405170020
    yield (
        UserClan(guild_id = guild_id),
        {},
        None,
    )
    
    guild_id = 202405170021
    yield (
        UserClan(guild_id = guild_id, icon = Icon(IconType.static, 2)),
        {'size': 1024},
        f'{CDN_ENDPOINT}/clan-badges/{guild_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    guild_id = 202405170022
    yield (
        UserClan(guild_id = guild_id, icon = Icon(IconType.animated, 3)),
        {},
        f'{CDN_ENDPOINT}/clan-badges/{guild_id}/a_00000000000000000000000000000003.gif',
    )
    
    guild_id = 202405170023
    yield (
        UserClan(guild_id = guild_id, icon = Icon(IconType.animated, 3)),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/clan-badges/{guild_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__clan_icon_url_as(user_clan, keyword_parameters):
    """
    Tests whether ``clan_icon_url_as`` works as intended.
    
    Parameters
    ----------
    user_clan : ``UserClan``
        User clan to get its url of.
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    output = clan_icon_url_as(user_clan, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
