import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_user_banner_url_as


def _iter_options():
    user_id = 202407160014
    yield (
        user_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    user_id = 202407160015
    yield (
        user_id,
        IconType.static,
        2,
        None,
        None,
        f'{CDN_ENDPOINT}/banners/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160016
    yield (
        user_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/banners/{user_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    user_id = 202407160017
    yield (
        user_id,
        IconType.static,
        2,
        'jpg',
        1024,
        f'{CDN_ENDPOINT}/banners/{user_id}/00000000000000000000000000000002.jpg?size=1024',
    )
    
    user_id = 202407160020
    yield (
        user_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/banners/{user_id}/a_00000000000000000000000000000003.gif',
    )
    
    user_id = 202506210026
    yield (
        user_id,
        IconType.static,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/banners/{user_id}/00000000000000000000000000000004.webp',
    )
    
    user_id = 202506210027
    yield (
        user_id,
        IconType.animated,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/banners/{user_id}/a_00000000000000000000000000000004.webp?animated=true',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_banner_url_as(user_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_user_banner_url_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        If the user has animated banner, it can be `'gif'` as well.
    
    size : `None | int`
        The preferred minimal size of the banner's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_user_banner_url_as(user_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
