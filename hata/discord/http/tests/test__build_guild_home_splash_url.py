import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_guild_home_splash_url


def _iter_options():
    guild_id = 202504150000
    yield (
        guild_id,
        IconType.none,
        0,
        None,
    )
    
    guild_id = 202504150001
    yield (
        guild_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/home-headers/{guild_id}/00000000000000000000000000000002.png',
    )
    
    guild_id = 202504150002
    yield (
        guild_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/home-headers/{guild_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_home_splash_url(guild_id, icon_type, icon_hash):
    """
    Tests whether ``build_guild_home_splash_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_guild_home_splash_url(guild_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
