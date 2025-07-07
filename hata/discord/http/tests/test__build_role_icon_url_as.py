import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_role_icon_url_as


def _iter_options():
    role_id = 202504180003
    yield (
        role_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    role_id = 202504180004
    yield (
        role_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/role-icons/{role_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    role_id = 202504180005
    yield (
        role_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/role-icons/{role_id}/a_00000000000000000000000000000003.gif',
    )
    
    role_id = 202504180006
    yield (
        role_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/role-icons/{role_id}/a_00000000000000000000000000000003.png',
    )
    
    role_id = 202506210018
    yield (
        role_id,
        IconType.static,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/role-icons/{role_id}/00000000000000000000000000000004.webp',
    )
    
    role_id = 202506210019
    yield (
        role_id,
        IconType.animated,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/role-icons/{role_id}/a_00000000000000000000000000000004.webp?animated=true',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_role_icon_url_as(role_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_role_icon_url_as`` works as intended.
    
    Parameters
    ----------
    role_id : `int`
        Role identifier to test with.
    
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
    output = build_role_icon_url_as(role_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
