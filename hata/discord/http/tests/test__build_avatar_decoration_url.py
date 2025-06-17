import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_avatar_decoration_url


def _iter_options():
    yield (
        IconType.none,
        0,
        None,
    )
    
    yield (
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/avatar-decoration-presets/00000000000000000000000000000002.png',
    )
    
    yield (
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/avatar-decoration-presets/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_avatar_decoration_url(icon_type, icon_hash):
    """ 
    Tests whether ``build_avatar_decoration_url`` works as intended.
    
    Parameters
    ----------
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_avatar_decoration_url(icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
