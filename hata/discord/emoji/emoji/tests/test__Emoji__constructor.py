import vampytest

from ....core import BUILTIN_EMOJIS
from ....user import ClientUserBase, User

from ...unicode.unicode_type import Unicode

from ..emoji import Emoji


def _assert_fields_set(emoji):
    """
    Asserts whether all the fields if the given emoji are set.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji to check.
    """
    vampytest.assert_instance(emoji, Emoji)
    vampytest.assert_instance(emoji.animated, bool)
    vampytest.assert_instance(emoji.available, bool)
    vampytest.assert_instance(emoji.guild_id, int)
    vampytest.assert_instance(emoji.id, int)
    vampytest.assert_instance(emoji.managed, bool)
    vampytest.assert_instance(emoji.name, str)
    vampytest.assert_instance(emoji.require_colons, bool)
    vampytest.assert_instance(emoji.role_ids, tuple, nullable = True)
    vampytest.assert_instance(emoji.unicode, str, nullable = True)
    vampytest.assert_instance(emoji.user, ClientUserBase)


def test__Emoji__new__0():
    """
    Checks whether ``Emoji.__new__`` works as intended.
    
    Case: No fields given.
    """
    emoji = Emoji()
    _assert_fields_set(emoji)


def test__Emoji__new__1():
    """
    Checks whether ``Emoji.__new__`` works as intended.
    
    Case: All fields given.
    """
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010000, 202301010001]
    user = User.precreate(202301010002)
    
    emoji = Emoji(
        animated = animated,
        available = available,
        managed = managed,
        name = name,
        require_colons = require_colons,
        role_ids = role_ids,
        user = user,
    )
    _assert_fields_set(emoji)
    
    vampytest.assert_eq(emoji.animated, animated)
    vampytest.assert_eq(emoji.available, available)
    vampytest.assert_eq(emoji.managed, managed)
    vampytest.assert_eq(emoji.name, name)
    vampytest.assert_eq(emoji.require_colons, require_colons)
    vampytest.assert_eq(emoji.role_ids, tuple(role_ids))
    vampytest.assert_is(emoji.user, user)


def test__Emoji__precreate__0():
    """
    Tests whether ``Emoji.precreate`` works as intended.
    
    Case: No fields given.
    """
    emoji_id = 202301010003
    
    emoji = Emoji.precreate(emoji_id)
    _assert_fields_set(emoji)
    
    vampytest.assert_eq(emoji.id, emoji_id)


def test__Emoji__precreate__1():
    """
    Tests whether ``Emoji.precreate`` works as intended.
    
    Case: All fields given.
    """
    emoji_id = 202301010004
    guild_id = 202301010005
    
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010006, 202301010007]
    user = User.precreate(202301010008)
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        animated = animated,
        available = available,
        managed = managed,
        name = name,
        require_colons = require_colons,
        role_ids = role_ids,
        user = user,
    )
    _assert_fields_set(emoji)

    vampytest.assert_eq(emoji.id, emoji_id)
    vampytest.assert_eq(emoji.guild_id, guild_id)
    
    vampytest.assert_eq(emoji.animated, animated)
    vampytest.assert_eq(emoji.available, available)
    vampytest.assert_eq(emoji.managed, managed)
    vampytest.assert_eq(emoji.name, name)
    vampytest.assert_eq(emoji.require_colons, require_colons)
    vampytest.assert_eq(emoji.role_ids, tuple(role_ids))
    vampytest.assert_is(emoji.user, user)


def test__Emoji__precreate__2():
    """
    Tests whether ``Emoji.precreate`` works as intended.
    
    Case: Caching.
    """
    emoji_id = 202301010009
    
    emoji = Emoji.precreate(emoji_id)   
    test_emoji = Emoji.precreate(emoji_id)
    vampytest.assert_is(emoji, test_emoji)


def test__Emoji__create_unicode__0():
    """
    Tests whether ``Emoji._create_unicode`` registers the emoji by name when `register_by_name` parameter is 
    passed as `True`.
    """
    name = '20220811_0000'
    emoticon = '20220811_0001'
    alias = '20220811_0002'
    
    unicode = Unicode(name, b'abs', False, (emoticon, ), (alias, ))
    
    emoji = Emoji._create_unicode(unicode, True)
    _assert_fields_set(emoji)
    
    for alternative_name in (name, emoticon, alias):
        vampytest.assert_in(alternative_name, BUILTIN_EMOJIS)
        vampytest.assert_is(BUILTIN_EMOJIS[alternative_name], emoji)


def test__Emoji__create_unicode__1():
    """
    Tests whether ``Emoji._create_unicode`` will not register the emoji by name when `register_by_name` parameter is
    passed as `False`.
    """
    name = '20220811_0003'
    emoticon = '20220811_0004'
    alias = '20220811_0005'
    
    unicode = Unicode(name, b'abs', False, (emoticon, ), (alias, ))
    
    emoji = Emoji._create_unicode(unicode, False)
    _assert_fields_set(emoji)
    
    for alternative_name in (name, emoticon, alias):
        vampytest.assert_not_in(alternative_name, BUILTIN_EMOJIS)


def test__Emoji___create_partial__0():
    """
    Tests whether ``Emoji._create_partial`` works as intended.
    
    Case: Fields.
    """
    emoji_id = 202301010057
    name = 'abs'
    animated = True
    
    emoji = Emoji._create_partial(emoji_id, name, animated)
    _assert_fields_set(emoji)
    
    vampytest.assert_eq(emoji.id, emoji_id)
    vampytest.assert_eq(emoji.name, name)
    vampytest.assert_eq(emoji.animated, animated)


def test__Emoji__create_partial__1():
    """
    Tests whether ``Emoji._create_partial`` works as intended.
    
    Case: Caching.
    """
    emoji_id = 202301010057
    name = 'abs'
    animated = True
    
    emoji = Emoji._create_partial(emoji_id, name, animated)
    test_emoji = Emoji._create_partial(emoji_id, name, animated)
    
    vampytest.assert_is(emoji, test_emoji)


def test__Emoji__create_empty():
    """
    Tests whether ``Emoji._create_empty`` works as intended.
    """
    emoji_id = 202301010058
    
    emoji = Emoji._create_empty(emoji_id)
    _assert_fields_set(emoji)
    vampytest.assert_eq(emoji.id, emoji_id)
