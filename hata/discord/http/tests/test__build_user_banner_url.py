import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_user_banner_url


def _iter_options():
    user_id = 202407160005
    yield (
        user_id,
        IconType.none,
        0,
        None,
    )
    
    user_id = 202407160004
    yield (
        user_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/banners/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160003
    yield (
        user_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/banners/{user_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_banner_url(user_id, icon_type, icon_hash):
    """
    Tests whether ``build_user_banner_url`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_user_banner_url(user_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
