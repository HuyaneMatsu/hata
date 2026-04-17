import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import ROLES

from ...role_color_configuration import RoleColorConfiguration

from ..role import Role
from ..utils import create_partial_role_from_data


def test__create_partial_role_from_data__new():
    """
    Tests whether ``create_partial_role_from_data`` works as intended.
    
    Case: new.
    """
    role_id = 202604050000
    guild_id = 202604050001
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    name = 'Eirin'
    position = 5
    icon = Icon(IconType.static, 2)
    
    data = {
        'id': str(role_id),
        'colors': color_configuration.to_data(),
        'name': name,
        'position': position,
        'icon': icon.as_base_16_hash,
    }
    
    vampytest.assert_is(ROLES.get(role_id, None), None)
    output = create_partial_role_from_data(data, guild_id)
    vampytest.assert_instance(output, Role)
    
    vampytest.assert_is(ROLES.get(role_id, None), output)
    
    vampytest.assert_eq(output.id, role_id)
    vampytest.assert_eq(output.guild_id, guild_id)
    vampytest.assert_eq(output.color_configuration, color_configuration)
    vampytest.assert_eq(output.name, name)
    vampytest.assert_eq(output.position, position)
    vampytest.assert_eq(output.icon, icon)


def test__create_partial_role_from_data__existing():
    """
    Tests whether ``create_partial_role_from_data`` works as intended.
    
    Case: existing.
    """
    role_id = 202604050002
    guild_id = 202604050003
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    name = 'Eirin'
    position = 5
    icon = Icon(IconType.static, 2)
    
    data = {
        'id': str(role_id),
        'colors': color_configuration.to_data(),
        'name': name,
        'position': position,
        'icon': icon.as_base_16_hash,
    }
    
    role = Role.precreate(role_id)
    vampytest.assert_is(ROLES.get(role_id, None), role)
    output = create_partial_role_from_data(data, guild_id)
    vampytest.assert_instance(output, Role)
    
    vampytest.assert_is(ROLES.get(role_id, None), role)
    vampytest.assert_is(role, output)
    
    # We keep the existing attributes here.
    vampytest.assert_ne(output.color_configuration, color_configuration)
    vampytest.assert_ne(output.name, name)
    vampytest.assert_ne(output.position, position)
    vampytest.assert_ne(output.icon, icon)
