import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....guild import Guild
from ....permission import Permission

from ...role_color_configuration import RoleColorConfiguration
from ...role_manager_metadata import RoleManagerMetadataBot

from ..flags import RoleFlag
from ..role import Role
from ..preinstanced import RoleManagerType

from .test__Role__constructor import _assert_fields_set


def test__Role__from_data__default():
    """
    Tests whether ``Role.from_data`` works as intended.
    """
    role_id = 202211040007
    guild_id = 202211040008
    
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    flags = RoleFlag(12)
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
        'colors': color_configuration.to_data(),
        'flags': int(flags),
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


def test__Role__from_data__caching():
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


def test__Role__from_data__guild_caching():
    """
    Tests whether ``Role.from_data`` works as intended.
    
    Case: Check guild caching.
    """
    role_id = 202306130002
    guild_id = 202306130003
    
    data = {
        'id': str(role_id),
    }
    
    guild = Guild.precreate(guild_id)
    
    role = Role.from_data(data, guild_id)
    
    vampytest.assert_eq(guild.roles, {role_id: role})


def test__Role__from_data__string_cache_off():
    """
    Tests whether ``Role.from_data`` works as intended.
    
    Case: `strong_cache` given as `False`.
    """
    role_id = 202306130004
    guild_id = 202306130005
    
    data = {
        'id': str(role_id),
    }
    
    guild = Guild.precreate(guild_id)
    
    role = Role.from_data(data, guild_id, strong_cache = False)
    
    vampytest.assert_eq(guild.roles, {})


def test__Role__to_data__include_internals_and_defaults():
    """
    Tests whether ``Role.to_data`` works as intended.
    
    Case: include internals & defaults.
    """
    role_id = 202211040012
    
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    flags = RoleFlag(12)
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
    
    vampytest.assert_eq(
        role.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'id': str(role_id),
            'color': int(color),
            'colors': color_configuration.to_data(defaults = True),
            'flags': int(flags),
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
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    flags = RoleFlag(12)
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
        'colors': color_configuration.to_data(),
        'flags': int(flags),
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


def test__Role__update_attributes():
    """
    Tests whether ``Role._update_attributes`` works as intended.
    """
    role_id = 202211040014
    
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    flags = RoleFlag(12)
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
        'colors': color_configuration.to_data(),
        'flags': int(flags),
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


def test__Role__difference_update_attributes():
    """
    Tests whether ``Role._difference_update_attributes`` works as intended.
    """
    role_id = 202211040015
    
    old_color = Color(123)
    old_color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    old_flags = RoleFlag(12)
    old_icon = Icon(IconType.static, 2)
    old_permissions = Permission(555)
    old_name = 'holo'
    old_mentionable = True
    old_position = 6
    old_separated = True
    old_unicode_emoji = None
    
    new_color = Color(999)
    new_color_configuration = RoleColorConfiguration(
        color_primary = Color(333),
        color_secondary = Color(334),
        color_tertiary = Color(335),
    )
    new_flags = RoleFlag(11)
    new_icon = None
    new_mentionable = False
    new_name = 'kokoro'
    new_permissions = Permission(6666)
    new_position = 4
    new_separated = False
    new_unicode_emoji = BUILTIN_EMOJIS['heart']
    
    role = Role.precreate(
        role_id,
        color = old_color,
        color_configuration = old_color_configuration,
        flags = old_flags,
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
        'colors': new_color_configuration.to_data(),
        'flags': int(new_flags),
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
    vampytest.assert_eq(role.color_configuration, new_color_configuration)
    vampytest.assert_eq(role.flags, new_flags)
    vampytest.assert_eq(role.icon, new_icon)
    vampytest.assert_eq(role.mentionable, new_mentionable)
    vampytest.assert_eq(role.name, new_name)
    vampytest.assert_eq(role.permissions, new_permissions)
    vampytest.assert_eq(role.position, new_position)
    vampytest.assert_eq(role.separated, new_separated)
    vampytest.assert_is(role.unicode_emoji, new_unicode_emoji)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'color': old_color,
            'color_configuration': old_color_configuration,
            'flags': old_flags,
            'icon': old_icon,
            'mentionable': old_mentionable,
            'name': old_name,
            'permissions': old_permissions,
            'position': old_position,
            'separated': old_separated,
            'unicode_emoji': old_unicode_emoji,
        },
    )
