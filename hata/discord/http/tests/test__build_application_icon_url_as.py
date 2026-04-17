import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_application_icon_url_as


def _iter_options():
    application_id = 202504170090
    yield (
        application_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    application_id = 202504170091
    yield (
        application_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/app-icons/{application_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    application_id = 202504170092
    yield (
        application_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/app-icons/{application_id}/a_00000000000000000000000000000003.gif',
    )
    
    application_id = 202504170093
    yield (
        application_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/app-icons/{application_id}/a_00000000000000000000000000000003.png',
    )
    
    application_id = 202506210002
    yield (
        application_id,
        IconType.static,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/app-icons/{application_id}/00000000000000000000000000000004.webp',
    )
    
    application_id = 202506210003
    yield (
        application_id,
        IconType.animated,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/app-icons/{application_id}/a_00000000000000000000000000000004.webp?animated=true',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_application_icon_url_as(application_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_application_icon_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create application for.
    
    icon_type : ``IconType``
        Icon type to use.
    
    icon_hash : `int`
        Icon hash to use (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_application_icon_url_as(application_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
