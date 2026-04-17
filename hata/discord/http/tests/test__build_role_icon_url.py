import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_role_icon_url


def _iter_options():
    role_id = 202504180000
    yield (
        role_id,
        IconType.none,
        0,
        None,
    )
    
    role_id = 202504180001
    yield (
        role_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/role-icons/{role_id}/00000000000000000000000000000002.png',
    )
    
    role_id = 202504180002
    yield (
        role_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/role-icons/{role_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_role_icon_url(role_id, icon_type, icon_hash):
    """
    Tests whether ``build_role_icon_url`` works as intended.
    
    Parameters
    ----------
    role_id : `int`
        Role identifier to test with.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_role_icon_url(role_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
