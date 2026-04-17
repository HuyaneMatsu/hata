import vampytest

from ....bases import Icon, IconType
from ....color import Color

from ...role_color_configuration import RoleColorConfiguration

from ..role import Role
from ..utils import create_partial_role_data


def test__create_partial_role_data():
    """
    Tests whether ``create_partial_role_data`` works as intended.
    """
    role_id = 202604050004
    guild_id = 202604050005
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    name = 'Eirin'
    position = 5
    icon = Icon(IconType.static, 2)
    
    expected_output = {
        'id': str(role_id),
        'colors': color_configuration.to_data(defaults = True),
        'name': name,
        'position': position,
        'icon': icon.as_base_16_hash,
        
        'unicode_emoji': None,
        'color': 0,
    }
    
    role = Role.precreate(
        role_id = role_id,
        guild_id = guild_id,
        color_configuration = color_configuration,
        name = name,
        position = position,
        icon = icon,
    )
    
    output = create_partial_role_data(role)
    
    vampytest.assert_eq(output, expected_output)
