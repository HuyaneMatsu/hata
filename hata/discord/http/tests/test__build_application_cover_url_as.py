import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_application_cover_url_as


def _iter_options():
    application_id = 202504170110
    yield (
        application_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    application_id = 202504170111
    yield (
        application_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/00000000000000000000000000000002.png?size=1024',
    )
    
    application_id = 202504170112
    yield (
        application_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/a_00000000000000000000000000000003.gif',
    )
    
    application_id = 202504170113
    yield (
        application_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_application_cover_url_as(application_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_application_cover_url_as`` works as intended.
    
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
    output = build_application_cover_url_as(application_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
