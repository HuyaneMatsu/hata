import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_guild_badge_icon_url_as


def _iter_options():
    guild_id = 202405170020
    yield (
        guild_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    guild_id = 202405170021
    yield (
        guild_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    guild_id = 202405170022
    yield (
        guild_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/a_00000000000000000000000000000003.gif',
    )
    
    guild_id = 202405170023
    yield (
        guild_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/badge-icons/{guild_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_badge_icon_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_guild_badge_icon_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
    
    icon_type : ``IconType``
        Icon type to use.
    
    icon_hash : `int`
        Icon hash to use (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_guild_badge_icon_url_as(guild_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
