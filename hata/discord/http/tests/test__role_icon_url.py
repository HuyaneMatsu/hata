import vampytest

from ...bases import Icon, IconType
from ...role import Role

from ..urls import CDN_ENDPOINT, role_icon_url


def _iter_options():
    role_id = 202504180000
    yield (
        role_id,
        None,
        None,
    )
    
    role_id = 202504180001
    yield (
        role_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/role-icons/{role_id}/00000000000000000000000000000002.png',
    )
    
    role_id = 202504180002
    yield (
        role_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/role-icons/{role_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__role_icon_url(role_id, icon):
    """
    Tests whether ``role_icon_url`` works as intended.
    
    Parameters
    ----------
    role_id : `int`
        Role identifier to create role for.
    
    icon : `None | Icon`
        Icon to create the role with.
    
    Returns
    -------
    output : `None | str`
    """
    role = Role.precreate(role_id, icon = icon)
    output = role_icon_url(role)
    vampytest.assert_instance(output, str, nullable = True)
    return output
