from datetime import datetime as DateTime

import vampytest

from ....client import Client
from ....core import BUILTIN_EMOJIS, EMOJIS
from ....guild import Guild
from ....role import Role, RoleManagerType
from ....user import User

from ..emoji import Emoji

from .test__Emoji__constructor import _assert_fields_set


def _iter_options__is_premium():
    role_id_0 = 202212190005
    role_id_1 = 202212190006
    
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1, manager_type = RoleManagerType.subscription)
    
    yield 202212190007, None, False
    yield 202212190008, [role_0], False
    yield 202212190009, [role_1], True


@vampytest._(vampytest.call_from(_iter_options__is_premium()).returning_last())
def test__Emoji__is_premium(emoji_id, roles):
    """
    Tests whether ``Emoji.is_premium`` works as intended.
    
    Parameters
    ----------
    emoji_id : `int`
        Emoji identifier.
    
    roles : ``None | list<Role>``
        Roles to create the emoji with.
    
    Returns
    -------
    output : `bool`
    """
    if roles is None:
        role_ids = None
    else:
        role_ids = [role.id for role in roles]
    
    emoji = Emoji.precreate(emoji_id, role_ids = role_ids)
    
    output = emoji.is_premium()
    vampytest.assert_instance(output, bool)
    return output


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


def test__Emoji__copy_with__no_fields():
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


def test__Emoji__copy_with__all_fields():
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


def _iter_options__roles():
    role_id_0 = 202301010071
    role_id_1 = 202301010072
    role_0 = Role.precreate(role_id_0, position = 1)
    role_1 = Role.precreate(role_id_1, position = 0)
    
    yield None, None
    yield [role_id_0, role_id_1], (role_1, role_0)
    

@vampytest._(vampytest.call_from(_iter_options__roles()).returning_last())
def test__Emoji__roles(role_ids):
    """
    Tests whether ``Emoji.roles`` works as intended.
    
    Parameters
    ----------
    role_ids : `None | list<int>`
        Role identifiers to create emoji with.
    
    Returns
    -------
    output : ``tuple<Role>``
    """
    emoji = Emoji(role_ids = role_ids) 
    
    output = emoji.roles
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Role)
    
    return output


def _iter_options__iter_role_ids():
    role_id_0 = 202301010073
    role_id_1 = 202301010074
    
    yield None, []
    yield [role_id_0, role_id_1], [role_id_0, role_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_role_ids()).returning_last())
def test__Emoji__iter_role_ids(role_ids):
    """
    Tests whether ``Emoji.iter_role_ids`` works as intended.
    
    Parameters
    ----------
    role_ids : `None | list<int>`
        Role identifiers to create emoji with.
    
    Returns
    -------
    output : `list<int>`
    """
    emoji = Emoji(role_ids = role_ids)
    output = [*emoji.iter_role_ids()]
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output


def _iter_options__iter_roles():
    role_id_0 = 202301010075
    role_id_1 = 202301010076
    role_0 = Role.precreate(role_id_0, position = 1)
    role_1 = Role.precreate(role_id_1, position = 0)
    
    yield None, []
    yield [role_id_0, role_id_1], [role_0, role_1]



@vampytest._(vampytest.call_from(_iter_options__iter_roles()).returning_last())
def test__Emoji__iter_roles(role_ids):
    """
    Tests whether ``Emoji.iter_roles`` works as intended.
    
    Parameters
    ----------
    role_ids : `None | list<int>`
        Role identifiers to create emoji with.
    
    Returns
    -------
    output : ``list<Role>``
    """
    emoji = Emoji(role_ids = role_ids) 
    
    output = [*emoji.iter_roles()]
    
    for element in output:
        vampytest.assert_instance(element, Role)
    
    return output


def _iter_options__url():
    yield 202505310000, False, True
    yield 202505310001, True, True
    
    yield BUILTIN_EMOJIS['x'].id, False, False


@vampytest._(vampytest.call_from(_iter_options__url()).returning_last())
def test__Emoji__url(emoji_id, animated):
    """
    Tests whether ``Emoji.url`` works as intended.
    
    Parameters
    ----------
    emoji_id : `int`
        Identifier to create emoji with.
    
    animated : `bool`
        Whether the emoji is animated.
    
    Returns
    -------
    has_url : `bool`
    """
    if emoji_id < (1 << 22):
        emoji = EMOJIS[emoji_id]
    
    else:
        emoji = Emoji.precreate(
            emoji_id,
            animated = animated,
        )
    
    output = emoji.url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__url_as():
    yield 202505310002, False, {'ext': 'webp', 'size': 128}, True
    yield 202505310003, True, {'ext': 'webp', 'size': 128}, True
    
    yield BUILTIN_EMOJIS['x'].id, False, {'ext': 'webp', 'size': 128}, False


@vampytest._(vampytest.call_from(_iter_options__url_as()).returning_last())
def test__Emoji__url_as(emoji_id, animated, keyword_parameters):
    """
    Tests whether ``Emoji.url_as`` works as intended.
    
    Parameters
    ----------
    emoji_id : `int`
        Identifier to create emoji with.
    
    animated : `bool`
        Whether the emoji is animated.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_url : `bool`
    """
    if emoji_id < (1 << 22):
        emoji = EMOJIS[emoji_id]
    
    else:
        emoji = Emoji.precreate(
            emoji_id,
            animated = animated,
        )
    
    output = emoji.url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
