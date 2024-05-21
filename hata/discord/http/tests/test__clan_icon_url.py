import vampytest

from ...bases import Icon, IconType
from ...user import UserClan

from ..urls import CDN_ENDPOINT, clan_icon_url


def _iter_options():
    guild_id = 202405170017
    yield (
        UserClan(guild_id = guild_id),
        None,
    )
    
    guild_id = 202405170018
    yield (
        UserClan(guild_id = guild_id, icon = Icon(IconType.static, 2)),
        f'{CDN_ENDPOINT}/clan-badges/{guild_id}/00000000000000000000000000000002.png',
    )
    
    guild_id = 202405170019
    yield (
        UserClan(guild_id = guild_id, icon = Icon(IconType.animated, 3)),
        f'{CDN_ENDPOINT}/clan-badges/{guild_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__clan_icon_url(user_clan):
    """
    Tests whether ``clan_icon_url`` works as intended.
    
    Parameters
    ----------
    user_clan : ``UserClan``
        User clan to get its url of.
    
    Returns
    -------
    output : `None | str`
    """
    output = clan_icon_url(user_clan)
    vampytest.assert_instance(output, str, nullable = True)
    return output
