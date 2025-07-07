import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_guild_invite_splash_url_as


def _iter_options():
    guild_id = 202405170050
    yield (
        guild_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    guild_id = 202405170051
    yield (
        guild_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/splashes/{guild_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    guild_id = 202405170052
    yield (
        guild_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/splashes/{guild_id}/a_00000000000000000000000000000003.gif',
    )
    
    guild_id = 202405170053
    yield (
        guild_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/splashes/{guild_id}/a_00000000000000000000000000000003.png',
    )
    
    guild_id = 202506210016
    yield (
        guild_id,
        IconType.static,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/splashes/{guild_id}/00000000000000000000000000000004.webp',
    )
    
    guild_id = 202506210017
    yield (
        guild_id,
        IconType.animated,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/splashes/{guild_id}/a_00000000000000000000000000000004.webp?animated=true',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_invite_splash_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_guild_invite_splash_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_guild_invite_splash_url_as(guild_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
