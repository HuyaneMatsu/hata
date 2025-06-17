import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_guild_discovery_splash_url_as


def _iter_options():
    guild_id = 202405170070
    yield (
        guild_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    guild_id = 202405170071
    yield (
        guild_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/discovery-splashes/{guild_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    guild_id = 202405170072
    yield (
        guild_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/discovery-splashes/{guild_id}/a_00000000000000000000000000000003.gif',
    )
    
    guild_id = 202405170073
    yield (
        guild_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/discovery-splashes/{guild_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_discovery_splash_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_guild_discovery_splash_url_as`` works as intended.
    
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
    output = build_guild_discovery_splash_url_as(guild_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
