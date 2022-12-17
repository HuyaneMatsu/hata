import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....permission import Permission

from ...role_manager_metadata import RoleManagerMetadataBot

from ..role import Role
from ..preinstanced import RoleManagerType

from .test__Role__constructor import _assert_is_every_attribute_set


def test__Role__from_data__0():
    """
    Tests whether ``Role.from_data`` works as intended.
    """
    role_id = 202211040007
    guild_id = 202211040008
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBot(bot_id = 202211040009)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    data = {
        'id': str(role_id),
        'color': int(color),
        'icon': icon.as_base_16_hash,
        'managed': True,
        'tags': manager_metadata.to_data(),
        'mentionable': mentionable,
        'name': name,
        'permissions': format(permissions, 'd'),
        'position': position,
        'hoist': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role = Role.from_data(data, guild_id)
    _assert_is_every_attribute_set(role)
    
    vampytest.assert_eq(role.id, role_id)
    vampytest.assert_eq(role.guild_id, guild_id)
    
    vampytest.assert_eq(role.color, color)
    vampytest.assert_eq(role.icon, icon)
    vampytest.assert_eq(role.manager_metadata, manager_metadata)
    vampytest.assert_is(role.manager_type, manager_type)
    vampytest.assert_eq(role.mentionable, mentionable)
    vampytest.assert_eq(role.name, name)
    vampytest.assert_eq(role.permissions, permissions)
    vampytest.assert_eq(role.position, position)
    vampytest.assert_eq(role.separated, separated)
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)


def test__Role__from_data__1():
    """
    Tests whether ``Role.from_data`` works as intended.
    
    Case: Check caching.
    """
    role_id = 202211040010
    guild_id = 202211040011
    
    role_1 = Role.precreate(role_id)
    
    data = {
        'id': str(role_id),
    }
    
    role_2 = Role.from_data(data, guild_id)
    
    vampytest.assert_is(role_1, role_2)


def test__Role__to_data__1():
    """
    Tests whether ``Role.to_data`` works as intended.
    
    Case: include internals & defaults.
    """
    role_id = 202211040012
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBot(bot_id = 202212170026)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    role = Role.precreate(
        role_id,
        color = color,
        icon = icon,
        manager = (manager_type, manager_metadata),
        mentionable = mentionable,
        name = name,
        permissions = permissions,
        position = position,
        separated = separated,
        unicode_emoji = unicode_emoji,
    )
    
    vampytest.assert_eq(
        role.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'id': str(role_id),
            'color': int(color),
            'icon': icon.as_base_16_hash,
            'managed': True,
            'tags': manager_metadata.to_data(),
            'mentionable': mentionable,
            'name': name,
            'permissions': format(permissions, 'd'),
            'position': position,
            'hoist': separated,
            'unicode_emoji': unicode_emoji,
        },
    )


def test__Role__set_attributes():
    """
    Tests whether ``Role._set_attributes`` works as intended.
    """
    role_id = 202211040013
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBot(bot_id = 202212170027)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    role = Role.precreate(
        role_id,
    )
    
    data = {
        'color': int(color),
        'icon': icon.as_base_16_hash,
        'managed': True,
        'tags': manager_metadata.to_data(),
        'mentionable': mentionable,
        'name': name,
        'permissions': format(permissions, 'd'),
        'position': position,
        'hoist': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role._set_attributes(data)
    
    vampytest.assert_eq(role.color, color)
    vampytest.assert_eq(role.icon, icon)
    vampytest.assert_eq(role.manager_metadata, manager_metadata)
    vampytest.assert_is(role.manager_type, manager_type)
    vampytest.assert_eq(role.mentionable, mentionable)
    vampytest.assert_eq(role.name, name)
    vampytest.assert_eq(role.permissions, permissions)
    vampytest.assert_eq(role.position, position)
    vampytest.assert_eq(role.separated, separated)
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)


def test__Role__update_attributes():
    """
    Tests whether ``Role._update_attributes`` works as intended.
    """
    role_id = 202211040014
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBot(bot_id = 202212170028)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    role = Role.precreate(
        role_id,
        manager_type = RoleManagerType.unset,
    )
    
    data = {
        'color': int(color),
        'icon': icon.as_base_16_hash,
        'managed': True,
        'tags': manager_metadata.to_data(),
        'mentionable': mentionable,
        'name': name,
        'permissions': format(permissions, 'd'),
        'position': position,
        'hoist': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role._update_attributes(data)
    
    vampytest.assert_eq(role.color, color)
    vampytest.assert_eq(role.icon, icon)
    vampytest.assert_eq(role.manager_metadata, manager_metadata)
    vampytest.assert_is(role.manager_type, manager_type)
    vampytest.assert_eq(role.mentionable, mentionable)
    vampytest.assert_eq(role.name, name)
    vampytest.assert_eq(role.permissions, permissions)
    vampytest.assert_eq(role.position, position)
    vampytest.assert_eq(role.separated, separated)
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)


def test__Role__difference_update_attributes():
    """
    Tests whether ``Role._difference_update_attributes`` works as intended.
    """
    role_id = 202211040015
    
    old_color = Color(123)
    new_color = Color(999)
    old_icon = Icon(IconType.static, 2)
    new_icon = None
    old_mentionable = True
    new_mentionable = False
    old_name = 'holo'
    new_name = 'kokoro'
    old_permissions = Permission(555)
    new_permissions = Permission(6666)
    old_position = 6
    new_position = 4
    old_separated = True
    new_separated = False
    old_unicode_emoji = None
    new_unicode_emoji = BUILTIN_EMOJIS['heart']
    
    role = Role.precreate(
        role_id,
        color = old_color,
        icon = old_icon,
        mentionable = old_mentionable,
        name = old_name,
        permissions = old_permissions,
        position = old_position,
        separated = old_separated,
        unicode_emoji = old_unicode_emoji,
    )
    
    data = {
        'id': str(role_id),
        'color': int(new_color),
        'icon': new_icon,
        'mentionable': new_mentionable,
        'name': new_name,
        'permissions': format(new_permissions, 'd'),
        'position': new_position,
        'hoist': new_separated,
        'unicode_emoji': new_unicode_emoji.unicode,
    }
    
    old_attributes = role._difference_update_attributes(data)
    
    vampytest.assert_eq(role.color, new_color)
    vampytest.assert_eq(role.icon, new_icon)
    vampytest.assert_eq(role.mentionable, new_mentionable)
    vampytest.assert_eq(role.name, new_name)
    vampytest.assert_eq(role.permissions, new_permissions)
    vampytest.assert_eq(role.position, new_position)
    vampytest.assert_eq(role.separated, new_separated)
    vampytest.assert_is(role.unicode_emoji, new_unicode_emoji)
    
    vampytest.assert_in('color', old_attributes)
    vampytest.assert_in('icon', old_attributes)
    vampytest.assert_in('mentionable', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permissions', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('separated', old_attributes)
    vampytest.assert_in('unicode_emoji', old_attributes)
    
    vampytest.assert_eq(old_attributes['color'], old_color)
    vampytest.assert_eq(old_attributes['icon'], old_icon)
    vampytest.assert_eq(old_attributes['mentionable'], old_mentionable)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(old_attributes['permissions'], old_permissions)
    vampytest.assert_eq(old_attributes['position'], old_position)
    vampytest.assert_eq(old_attributes['separated'], old_separated)
    vampytest.assert_is(old_attributes['unicode_emoji'], old_unicode_emoji)
