import vampytest

from ...bases import Icon, IconType
from ...color import Color
from ...core import BUILTIN_EMOJIS
from ...permission import Permission

from ..role import Role
from ..preinstanced import RoleManagerType


def test__Role__hash():
    """
    Tests whether ``Role.__hash__`` works as intended.
    """
    role_id = 202211040016
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_id = 202211040017
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    keyword_parameters = {
        'color': color,
        'icon': icon,
        'manager': (manager_type, manager_id),
        'mentionable': mentionable,
        'name': name,
        'permissions': permissions,
        'position': position,
        'separated': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role = Role(**keyword_parameters)
    vampytest.assert_instance(hash(role), int)
    
    role = Role.precreate(role_id, **keyword_parameters)
    vampytest.assert_instance(hash(role), int)


def test__Role__repr():
    """
    Tests whether ``Role.__repr__`` works as intended.
    """
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_id = 202211040019
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    role = Role(
        color = color,
        icon = icon,
        manager = (manager_type, manager_id),
        mentionable = mentionable,
        name = name,
        permissions = permissions,
        position = position,
        separated = separated,
        unicode_emoji = unicode_emoji,
    )
    
    vampytest.assert_instance(repr(role), str)


def test__Role__eq():
    """
    Tests whether ``Role.__eq__`` works as intended.
    """
    role_id = 202211040020
    
    color = Color(123)
    icon = None
    manager_id = 202211040021
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    keyword_parameters = {
        'color': color,
        'icon': icon,
        'manager': (manager_type, manager_id),
        'mentionable': mentionable,
        'name': name,
        'permissions': permissions,
        'position': position,
        'separated': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role = Role.precreate(role_id, **keyword_parameters)
    vampytest.assert_eq(role, role)
    vampytest.assert_ne(role, object())
    
    test_role = Role(**keyword_parameters)
    vampytest.assert_eq(role, test_role)
    
    for field_name, field_value in (
        ('color', Color(666)),
        ('icon', Icon(IconType.animated, 12)),
        ('manager', None),
        ('mentionable', False),
        ('name', 'alive'),
        ('permissions', Permission(554)),
        ('position', 7),
        ('separated', False),
        ('unicode_emoji', BUILTIN_EMOJIS['heart']),
    ):
        test_role = Role(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(role, test_role)


def test__Role__format():
    """
    Tests whether ``Role.__format__`` works as intended.
    """
    role_id = 202211040022
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_id = 202211040023
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    keyword_parameters = {
        'color': color,
        'icon': icon,
        'manager': (manager_type, manager_id),
        'mentionable': mentionable,
        'name': name,
        'permissions': permissions,
        'position': position,
        'separated': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role = Role.precreate(role_id, **keyword_parameters)
    
    vampytest.assert_eq(format(role, ''), role.name)
    vampytest.assert_eq(format(role, 'm'), role.mention)
    vampytest.assert_instance(format(role, 'c'), str)
    
    with vampytest.assert_raises(ValueError):
        format(role, 'owo')


def test__Role__sort():
    """
    Tests whether ``Role`` sorting works as intended.
    """
    role_1 = Role.precreate(202211040024, position = 6)
    role_2 = Role.precreate(202211040025, position = 12)
    role_3 = Role.precreate(202211040026, position = 6)
    
    for roles, expected_output in (
        ([role_1, role_2], [role_1, role_2]),
        ([role_2, role_3], [role_3, role_2]),
        ([role_3, role_1], [role_1, role_3]),
    ):
        vampytest.assert_eq(sorted(roles), expected_output)
