import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_avatar_decoration_url_as


def _iter_options():
    yield (
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    yield (
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/avatar-decoration-presets/00000000000000000000000000000002.png?size=1024',
    )
    
    yield (
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/avatar-decoration-presets/a_00000000000000000000000000000003.gif',
    )
    
    yield (
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/avatar-decoration-presets/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_avatar_decoration_url_as(icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_avatar_decoration_url_as`` works as intended.
    
    Parameters
    ----------
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `png`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_avatar_decoration_url_as(icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
