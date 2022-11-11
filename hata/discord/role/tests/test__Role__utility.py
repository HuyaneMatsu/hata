import vampytest

from ...bases import Icon, IconType
from ...client import Client
from ...color import Color
from ...core import BUILTIN_EMOJIS
from ...guild import Guild
from ...integration import Integration
from ...permission import Permission
from ...user import ClientUserBase, GuildProfile, User
from ...utils import is_url

from ..role import Role
from ..preinstanced import RoleManagerType

from .test__Role__constructor import _assert_is_every_attribute_set


def test__Role__is_default():
    """
    Tests whether ``Role.is_default`` works as intended.
    """
    role = Role._create_empty(202211040027, 0)
    vampytest.assert_false(role.is_default())
    
    role = Role._create_empty(202211040028, 202211040028)
    vampytest.assert_true(role.is_default())


def test__Role__mention():
    """
    Tests whether ``Role.mention`` works as intended.
    """
    role_id = 202211040029
    
    role = Role._create_empty(role_id, 0)
    mention = role.mention
    vampytest.assert_instance(mention, str)
    vampytest.assert_in(str(role_id), mention)


def test__Role__users__0():
    """
    Tests whether ``Role.users`` works as intended.
    
    Case: Non default.
    """
    guild_id = 202211040031
    role_id = 202211040033
    
    guild = Guild.precreate(guild_id)
    role = Role.precreate(role_id, guild_id = guild_id)
    
    user_1 = User.precreate(202211040030)
    user_1.guild_profiles[guild_id] = GuildProfile()
    guild.users[user_1.id] = user_1
    
    user_2 = User.precreate(202211040032)
    user_2.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    guild.users[user_2.id] = user_2
    
    vampytest.assert_eq({*role.users}, {user_2})


def test__Role__users__1():
    """
    Tests whether ``Role.users`` works as intended.
    
    Case: Default.
    """
    guild_id = 202211040051
    role_id = guild_id
    
    guild = Guild.precreate(guild_id)
    role = Role.precreate(role_id, guild_id = guild_id)
    
    user_1 = User.precreate(202211040052)
    user_1.guild_profiles[guild_id] = GuildProfile()
    guild.users[user_1.id] = user_1
    
    user_2 = User.precreate(202211040053)
    user_2.guild_profiles[guild_id] = GuildProfile()
    guild.users[user_2.id] = user_2
    
    vampytest.assert_eq({*role.users}, {user_1, user_2})


def test__Role__managed():
    """
    Tests whether ``Role.managed`` works as intended.
    """
    role = Role(manager = (RoleManagerType.unknown, 0))
    vampytest.assert_true(role.managed)

    role = Role(manager = (RoleManagerType.none, 0))
    vampytest.assert_false(role.managed)


def test__Role__manager():
    """
    Tests whether ``Role.manager`` works as intended.
    """
    role = Role(manager = (RoleManagerType.bot, 2022110400335))
    vampytest.assert_instance(role.manager, ClientUserBase)

    role = Role(manager = (RoleManagerType.integration, 2022110400336))
    vampytest.assert_instance(role.manager, Integration)


def test__Role__guild():
    """
    Tests whether ``Role.guild`` works as intended.
    """
    guild_id = 202211040037
    role_id = 202211040038
    
    guild = Guild.precreate(guild_id)
    role = Role.precreate(role_id, guild_id = guild_id)
    
    vampytest.assert_is(role.guild, guild)


def test__Role__partial__0():
    """
    Tests whether ``Role.partial`` works as intended.
    
    Case: partial.
    """
    role_id = 202211040040
    
    role = Role.precreate(role_id)
    
    vampytest.assert_true(role.partial)
    
    
def test__Role__partial__1():
    """
    Tests whether ``Role.partial`` works as intended.
    
    Case: not partial.
    """
    client = Client(
        token = 'token_202211040000',
    )
    
    try:
        guild_id = 202211040049
        role_id = 202211040050
        
        guild = Guild.precreate(guild_id)
        guild.clients.append(client)
        role = Role.precreate(role_id, guild_id = guild_id)
        guild.roles[role_id] = role
        
        vampytest.assert_false(role.partial)
    
    finally:
        client._delete()
        client = None


def test__Role__copy():
    """
    Tests whether ``Role.copy`` works as intended.
    """
    role_id = 202211040041
    guild_id = 202211040042
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_id = 0
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
        icon = icon,
        manager = (manager_type, manager_id),
        mentionable = mentionable,
        name = name,
        permissions = permissions,
        position = position,
        separated = separated,
        unicode_emoji = unicode_emoji,
    )
    
    copy = role.copy()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(role, copy)
    vampytest.assert_eq(role, copy)
    
    vampytest.assert_eq(copy.id, 0)
    vampytest.assert_eq(copy.guild_id, 0)


def test__Role__copy_with__0():
    """
    Tests whether ``Role.copy_with`` works as intended.
    
    Case: No fields given.
    """
    role_id = 202211040043
    guild_id = 202211040044
    
    color = Color(123)
    icon = Icon(IconType.static, 2)
    manager_id = 0
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
        icon = icon,
        manager = (manager_type, manager_id),
        mentionable = mentionable,
        name = name,
        permissions = permissions,
        position = position,
        separated = separated,
        unicode_emoji = unicode_emoji,
    )
    
    copy = role.copy_with()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(role, copy)
    vampytest.assert_eq(role, copy)
    
    vampytest.assert_eq(copy.id, 0)
    vampytest.assert_eq(copy.guild_id, 0)


def test__Role__copy_with__1():
    """
    Tests whether ``Role.copy_with`` works as intended.
    
    Case: No fields given.
    """
    old_color = Color(123)
    new_color = Color(999)
    old_icon = Icon(IconType.static, 2)
    new_icon = None
    old_manager_id = 202211040045
    new_manager_id = 202211040046
    old_manager_type = RoleManagerType.bot
    new_manager_type = RoleManagerType.integration
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
    
    role = Role(
        color = old_color,
        icon = old_icon,
        manager = (old_manager_type, old_manager_id),
        mentionable = old_mentionable,
        name = old_name,
        permissions = old_permissions,
        position = old_position,
        separated = old_separated,
        unicode_emoji = old_unicode_emoji,
    )
    
    copy = role.copy_with(
        color = new_color,
        icon = new_icon,
        manager = (new_manager_type, new_manager_id),
        mentionable = new_mentionable,
        name = new_name,
        permissions = new_permissions,
        position = new_position,
        separated = new_separated,
        unicode_emoji = new_unicode_emoji,
    )
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(role, copy)
    
    vampytest.assert_eq(copy.color, new_color)
    vampytest.assert_eq(copy.icon, (IconType.none, 0))
    vampytest.assert_eq(copy.manager_id, new_manager_id)
    vampytest.assert_is(copy.manager_type, new_manager_type)
    vampytest.assert_eq(copy.mentionable, new_mentionable)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.permissions, new_permissions)
    vampytest.assert_eq(copy.position, new_position)
    vampytest.assert_eq(copy.separated, new_separated)
    vampytest.assert_is(copy.unicode_emoji, new_unicode_emoji)


def test__Role__copy_with__2():
    """
    Tests whether ``Role.copy_with`` works as intended.
    
    Case: icon and unicode_emoji are mutually exclusive.
    """
    role = Role()
    
    with vampytest.assert_raises(ValueError):
        role.copy_with(
            icon = Icon(IconType.static, 56),
            unicode_emoji = BUILTIN_EMOJIS['heart'],
        )


def test__Role__copy_with__3():
    """
    Tests whether ``Role.copy_with`` works as intended.
    
    Case: overwriting existing icon and unicode_emoji.
    """
    icon = Icon(IconType.static, 56)
    unicode_emoji = BUILTIN_EMOJIS['heart']
    
    role = Role(icon = icon).copy_with(unicode_emoji = unicode_emoji)
    vampytest.assert_eq(role.icon, None)
    vampytest.assert_is(role.unicode_emoji, unicode_emoji)

    role = Role(unicode_emoji = unicode_emoji).copy_with(icon = icon)
    vampytest.assert_eq(role.icon, icon)
    vampytest.assert_is(role.unicode_emoji, None)


def test__Role__icon_url__0():
    """
    Tests whether ``Role.icon_url`` works as intended.
    
    Case: has icon.
    """
    role_id = 202211040047
    
    role = Role.precreate(role_id, icon = Icon(IconType.static, 56))
    
    icon_url = role.icon_url
    vampytest.assert_instance(icon_url, str)
    vampytest.assert_true(is_url(icon_url))


def test__Role__icon_url__1():
    """
    Tests whether ``Role.icon_url`` works as intended.
    
    Case: no icon.
    """
    role_id = 202211040048
    
    role = Role.precreate(role_id, icon = None)
    
    icon_url = role.icon_url
    vampytest.assert_is(icon_url, None)
