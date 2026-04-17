import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji
from ....permission import Permission

from ...role_color_configuration import RoleColorConfiguration
from ...role_manager_metadata import RoleManagerMetadataBase, RoleManagerMetadataBooster

from ..flags import RoleFlag
from ..role import Role
from ..preinstanced import RoleManagerType


def _assert_fields_set(role):
    """
    Asserts whether every attributes of the given role is set.
    
    Parameters
    ----------
    role : ``Role``
        The role to check.
    """
    vampytest.assert_instance(role, Role)
    vampytest.assert_instance(role.color, Color)
    vampytest.assert_instance(role.color_configuration, RoleColorConfiguration)
    vampytest.assert_instance(role.flags, RoleFlag)
    vampytest.assert_instance(role.icon, Icon)
    vampytest.assert_instance(role.guild_id, int)
    vampytest.assert_instance(role.id, int)
    vampytest.assert_instance(role.manager_metadata, RoleManagerMetadataBase)
    vampytest.assert_instance(role.manager_type, RoleManagerType)
    vampytest.assert_instance(role.mentionable, bool)
    vampytest.assert_instance(role.name, str)
    vampytest.assert_instance(role.permissions, Permission)
    vampytest.assert_instance(role.position, int)
    vampytest.assert_instance(role.separated, bool)
    vampytest.assert_instance(role.unicode_emoji, Emoji, nullable = True)


def test__Role__new__no_fields_given():
    """
    Tests whether ``Role.__new__`` works as intended.
    
    Case: No fields given.
    """
    role = Role()
    _assert_fields_set(role)


def test__Role__new_all_fields_given():
    """
    Tests whether ``Role.__new__`` works as intended.
    
    Case: All fields given.
    """
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    flags = RoleFlag(12)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBooster()
    manager_type = RoleManagerType.booster
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    role = Role(
        color = color,
        color_configuration = color_configuration,
        flags = flags,
        icon = icon,
        manager = (manager_type, manager_metadata),
        mentionable = mentionable,
        name = name,
        permissions = permissions,
        position = position,
        separated = separated,
        unicode_emoji = unicode_emoji,
    )
    _assert_fields_set(role)
    
    vampytest.assert_eq(role.color, color)
    vampytest.assert_eq(role.color_configuration, color_configuration)
    vampytest.assert_eq(role.flags, flags)
    vampytest.assert_eq(role.icon, icon)
    vampytest.assert_eq(role.manager_metadata, manager_metadata)
    vampytest.assert_is(role.manager_type, manager_type)
    vampytest.assert_eq(role.mentionable, mentionable)
    vampytest.assert_eq(role.name, name)
    vampytest.assert_eq(role.permissions, permissions)
    vampytest.assert_eq(role.position, position)
    vampytest.assert_eq(role.separated, separated)
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)


def test__Role__new__unicode_emoji():
    """
    Tests whether ``Role.__new__`` works as intended.
    
    Case: Test unicode emoji.
    """
    unicode_emoji = BUILTIN_EMOJIS['heart']
    
    role = Role(
        unicode_emoji = unicode_emoji,
    )
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)


def test__Role__new__icon_and_unicode_emoji():
    """
    Tests whether ``Role.__new__`` works as intended.
    
    Case: Icon & unicode emoji are mutually exclusive.
    """
    icon = Icon(IconType.static, 2)
    unicode_emoji = BUILTIN_EMOJIS['heart']
    
    with vampytest.assert_raises(ValueError):
        Role(
            icon = icon,
            unicode_emoji = unicode_emoji,
        )


def test__Role__create_empty():
    """
    Tests whether ``Role._create_empty`` works as intended.
    
    Case: No fields given.
    """
    role_id = 202211040000
    guild_id = 202211040001
    
    role = Role._create_empty(role_id, guild_id)
    _assert_fields_set(role)
    
    vampytest.assert_eq(role.id, role_id)
    vampytest.assert_eq(role.guild_id, guild_id)


def test__Role__precreate__no_fields():
    """
    Tests whether ``Role.precreate`` works as intended.
    
    Case: No fields given.
    """
    role_id = 202211040002
    
    role = Role.precreate(role_id)
    _assert_fields_set(role)
    
    vampytest.assert_eq(role.id, role_id)


def test__Role__precreate__all_fields():
    """
    Tests whether ``Role.precreate`` works as intended.
    
    Case: All fields given.
    """
    role_id = 202211040003
    guild_id = 202211040034
    
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    flags = RoleFlag(12)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBooster()
    manager_type = RoleManagerType.booster
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    role = Role.precreate(
        role_id,
        guild_id = guild_id,
        color = color,
        color_configuration = color_configuration,
        flags = flags,
        icon = icon,
        manager = (manager_type, manager_metadata),
        mentionable = mentionable,
        name = name,
        permissions = permissions,
        position = position,
        separated = separated,
        unicode_emoji = unicode_emoji,
    )
    
    _assert_fields_set(role)
    
    vampytest.assert_eq(role.id, role_id)
    vampytest.assert_eq(role.guild_id, guild_id)
    
    vampytest.assert_eq(role.color, color)
    vampytest.assert_eq(role.color_configuration, color_configuration)
    vampytest.assert_eq(role.flags, flags)
    vampytest.assert_eq(role.icon, icon)
    vampytest.assert_eq(role.manager_metadata, manager_metadata)
    vampytest.assert_is(role.manager_type, manager_type)
    vampytest.assert_eq(role.mentionable, mentionable)
    vampytest.assert_eq(role.name, name)
    vampytest.assert_eq(role.permissions, permissions)
    vampytest.assert_eq(role.position, position)
    vampytest.assert_eq(role.separated, separated)
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)


def test__Role__precreate__unicode_emoji():
    """
    Tests whether ``Role.precreate`` works as intended.
    
    Case: Unicode emoji.
    """
    role_id = 202211040004
    
    unicode_emoji = BUILTIN_EMOJIS['heart']
    
    role = Role.precreate(
        role_id,
        unicode_emoji = unicode_emoji,
    )
    
    _assert_fields_set(role)
    
    vampytest.assert_eq(role.id, role_id)
    
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)



def test__Role__precreate__icon_and_unicode_emoji():
    """
    Tests whether ``Role.precreate`` works as intended.
    
    Case: icon & unicode_emoji are mutually exclusive.
    """
    role_id = 202211040005
    
    icon = Icon(IconType.static, 2)
    unicode_emoji = BUILTIN_EMOJIS['heart']
    
    with vampytest.assert_raises(ValueError):
        Role.precreate(
            role_id,
            icon = icon,
            unicode_emoji = unicode_emoji,
        )


def test__Role__precreate__cache():
    """
    Tests whether ``Role.precreate`` works as intended.
    
    Case: test cache.
    """
    role_id = 202211040006
    
    role_1 = Role.precreate(role_id)
    role_2 = Role.precreate(role_id)
    
    vampytest.assert_is(role_1, role_2)
