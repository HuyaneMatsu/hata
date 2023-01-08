from datetime import datetime as DateTime

import vampytest

from ....client import Client
from ....core import BUILTIN_EMOJIS
from ....guild import Guild
from ....role import Role, RoleManagerType
from ....user import User

from ..emoji import Emoji

from .test__Emoji__constructor import _assert_fields_set


def test__Emoji__is_premium():
    """
    Tests whether ``Emoji.is_premium`` works as intended.
    """
    role_id_0 = 202212190005
    role_id_1 = 202212190006
    
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1, manager_type = RoleManagerType.subscription)
    
    for emoji, expected_output in (
        (Emoji.precreate(202212190007, roles = None), False),
        (Emoji.precreate(202212190008, roles = [role_id_0]), False),
        (Emoji.precreate(202212190009, roles = [role_id_1]), True),
    ):
        vampytest.assert_eq(emoji.is_premium(), expected_output)


def test__Emoji__partial():
    """
    Tests whether ``Emoji.partial`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_false(emoji.partial)
    
    emoji = Emoji()
    vampytest.assert_true(emoji.partial)
    
    emoji_id = 202301010038
    guild_id = 202301010039
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    vampytest.assert_true(emoji.partial)
    
    
    emoji_id = 202301010040
    guild_id = 202301010041
    guild = Guild.precreate(guild_id)
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    guild.emojis[emoji_id] = emoji
    vampytest.assert_true(emoji.partial)
    
    
    client = Client(
        token = 'token_20230101_0000',
    )
    
    try:
        emoji_id = 202301010042
        guild_id = 202301010043
        guild = Guild.precreate(guild_id)
        guild.clients.append(client)
        emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
        guild.emojis[emoji_id] = emoji
        vampytest.assert_false(emoji.partial)
        
    # Cleanup
    finally:
        client._delete()
        client = None
        clients = None


def test__Emoji__is_custom_emoji():
    """
    Tests whether ``Emoji.is_custom_emoji`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_false(emoji.is_custom_emoji())
    
    emoji = Emoji()
    vampytest.assert_true(emoji.is_custom_emoji())


def test__Emoji__is_unicode_emoji():
    """
    Tests whether ``Emoji.is_unicode_emoji`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_true(emoji.is_unicode_emoji())
    
    emoji = Emoji()
    vampytest.assert_false(emoji.is_unicode_emoji())


def test__Emoji__as_reaction():
    """
    Tests whether ``Emoji.as_reaction`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_instance(emoji.as_reaction, str)
    
    emoji = Emoji()
    vampytest.assert_instance(emoji.as_reaction, str)


def test__Emoji__as_emoji():
    """
    Tests whether ``Emoji.as_emoji`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_instance(emoji.as_emoji, str)
    
    emoji = Emoji()
    vampytest.assert_instance(emoji.as_emoji, str)



def test__Emoji__created_at():
    """
    Tests whether ``Emoji.as_emoji`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_instance(emoji.created_at, DateTime)
    
    emoji = Emoji()
    vampytest.assert_instance(emoji.created_at, DateTime)
    
    emoji_id = 202301010044
    emoji = Emoji.precreate(emoji_id)
    vampytest.assert_instance(emoji.created_at, DateTime)


def test__emoji__url():
    """
    Tests whether ``Emoji.url`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_is(emoji.url, None)

    emoji = Emoji()
    vampytest.assert_instance(emoji.url, str)


def test__emoji__url_as():
    """
    Tests whether ``Emoji.url_as`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_is(emoji.url_as(), None)

    emoji = Emoji()
    vampytest.assert_instance(emoji.url_as(), str)


def test__Emoji__copy():
    """
    Tests whether ``Emoji.copy`` works as intended.
    """
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010057, 202301010058]
    user = User.precreate(202301010059)
    
    emoji = Emoji(
        animated = animated,
        available = available,
        managed = managed,
        name = name,
        require_colons = require_colons,
        role_ids = role_ids,
        user = user,
    )
    
    copy = emoji.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(emoji, copy)
    vampytest.assert_eq(emoji, copy)


def test__Emoji__copy_with__0():
    """
    Tests whether ``Emoji.copy_with`` works as intended.
    
    Case: No fields given.
    """
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010060, 202301010061]
    user = User.precreate(202301010062)
    
    emoji = Emoji(
        animated = animated,
        available = available,
        managed = managed,
        name = name,
        require_colons = require_colons,
        role_ids = role_ids,
        user = user,
    )
    
    copy = emoji.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(emoji, copy)
    vampytest.assert_eq(emoji, copy)


def test__Emoji__copy_with__1():
    """
    Tests whether ``Emoji.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_animated = True
    old_available = True
    old_managed = True
    old_name = 'eclipse'
    old_require_colons = True
    old_role_ids = [202301010063, 202301010064]
    old_user = User.precreate(202301010065)
    
    new_animated = True
    new_available = True
    new_managed = True
    new_name = 'eclipse'
    new_require_colons = True
    new_role_ids = [202301010066, 202301010067]
    new_user = User.precreate(202301010068)
    
    emoji = Emoji(
        animated = old_animated,
        available = old_available,
        managed = old_managed,
        name = old_name,
        require_colons = old_require_colons,
        role_ids = old_role_ids,
        user = old_user,
    )
    
    copy = emoji.copy_with(
        animated = new_animated,
        available = new_available,
        managed = new_managed,
        name = new_name,
        require_colons = new_require_colons,
        role_ids = new_role_ids,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(emoji, copy)
    
    vampytest.assert_eq(copy.animated, new_animated)
    vampytest.assert_eq(copy.available, new_available)
    vampytest.assert_eq(copy.managed, new_managed)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.require_colons, new_require_colons)
    vampytest.assert_eq(copy.role_ids, tuple(new_role_ids))
    vampytest.assert_is(copy.user, new_user)


def test__Emoji__guild():
    """
    Tests whether ``Emoji.guild`` works as intended
    """
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_is(emoji.guild, None)
    
    emoji = Emoji()
    vampytest.assert_is(emoji.guild, None)
    
    emoji_id = 202301010069
    guild_id = 202301010070
    guild = Guild.precreate(guild_id)
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
    )
    vampytest.assert_is(emoji.guild, guild)


def test__Emoji__roles():
    """
    Tests whether ``Emoji.roles`` works as intended.
    """
    role_id_0 = 202301010071
    role_id_1 = 202301010072
    role_0 = Role.precreate(role_id_0, position = 1)
    role_1 = Role.precreate(role_id_1, position = 0)
    
    for input_value, expected_output in (
        (None, None),
        ([role_id_0, role_id_1], (role_1, role_0)),
    ):
        emoji = Emoji(role_ids = input_value) 
        vampytest.assert_eq(emoji.roles, expected_output)


def test__Emoji__iter_role_ids():
    """
    Tests whether ``Emoji.iter_role_ids`` works as intended.
    """
    role_id_0 = 202301010073
    role_id_1 = 202301010074
    
    for input_value, expected_output in (
        (None, []),
        ([role_id_0, role_id_1], [role_id_0, role_id_1]),
    ):
        emoji = Emoji(role_ids = input_value) 
        vampytest.assert_eq([*emoji.iter_role_ids()], expected_output)


def test__Emoji__iter_roles():
    """
    Tests whether ``Emoji.iter_roles`` works as intended.
    """
    role_id_0 = 202301010075
    role_id_1 = 202301010076
    role_0 = Role.precreate(role_id_0, position = 1)
    role_1 = Role.precreate(role_id_1, position = 0)
    
    for input_value, expected_output in (
        (None, []),
        ([role_id_0, role_id_1], [role_0, role_1]),
    ):
        emoji = Emoji(role_ids = input_value) 
        vampytest.assert_eq([*emoji.iter_roles()], expected_output)
