import vampytest

from ...bases import Icon, IconType
from ...role import Role

from ..urls import CDN_ENDPOINT, role_icon_url_as


def _iter_options():
    role_id = 202504180003
    yield (
        role_id,
        None,
        {},
        None,
    )
    
    role_id = 202504180004
    yield (
        role_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/role-icons/{role_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    role_id = 202504180005
    yield (
        role_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/role-icons/{role_id}/a_00000000000000000000000000000003.gif',
    )
    
    role_id = 202504180006
    yield (
        role_id,
        Icon(IconType.animated, 3),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/role-icons/{role_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__role_icon_url_as(role_id, icon, keyword_parameters):
    """
    Tests whether ``role_icon_url_as`` works as intended.
    
    Parameters
    ----------
    role_id : `int`
        Role identifier to create role for.
    
    icon : `None | Icon`
        Icon to create the role with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    role = Role.precreate(role_id, icon = icon)
    output = role_icon_url_as(role, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
