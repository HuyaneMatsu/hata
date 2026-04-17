import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_guild_badge_icon_url


def _iter_options():
    guild_id = 202405170017
    yield (
        guild_id,
        IconType.none,
        0,
        None,
    )
    
    guild_id = 202405170018
    yield (
        guild_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/00000000000000000000000000000002.png',
    )
    
    guild_id = 202405170019
    yield (
        guild_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_badge_icon_url(guild_id, icon_type, icon_hash):
    """
    Tests whether ``build_guild_badge_icon_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
    
    icon_type : ``IconType``
        Icon type to use.
    
    icon_hash : `int`
        Icon hash to use (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_guild_badge_icon_url(guild_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
