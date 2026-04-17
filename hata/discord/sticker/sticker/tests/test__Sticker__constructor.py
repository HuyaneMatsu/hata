import vampytest

from ....user import ClientUserBase, User

from ..preinstanced import StickerFormat, StickerType
from ..sticker import Sticker


def _assert_fields_set(sticker):
    """
    Asserts whether every fields are set of the given sticker.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The sticker to check out.
    """
    vampytest.assert_instance(sticker, Sticker)
    vampytest.assert_instance(sticker.available, bool)
    vampytest.assert_instance(sticker.description, str, nullable = True)
    vampytest.assert_instance(sticker.format, StickerFormat)
    vampytest.assert_instance(sticker.guild_id, int)
    vampytest.assert_instance(sticker.id, int)
    vampytest.assert_instance(sticker.name, str)
    vampytest.assert_instance(sticker.pack_id, int)
    vampytest.assert_instance(sticker.sort_value, int)
    vampytest.assert_instance(sticker.tags, frozenset, nullable = True)
    vampytest.assert_instance(sticker.type, StickerType)
    vampytest.assert_instance(sticker.user, ClientUserBase)


def test__Sticker__new__0():
    """
    Tests whether ``Sticker.__new__`` works as intended.
    
    Case: No fields given.
    """
    sticker = Sticker()
    _assert_fields_set(sticker)


def test__Sticker__new__1():
    """
    Tests whether ``Sticker.__new__`` works as intended.
    
    Case: All fields given.
    """
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070000
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070001)
        
    sticker = Sticker(
        available = available,
        description = description,
        name = name,
        pack_id = pack_id,
        sort_value = sort_value,
        sticker_format = sticker_format,
        sticker_type = sticker_type,
        tags = tags,
        user = user,
    )
    _assert_fields_set(sticker)
    
    vampytest.assert_eq(sticker.available, available)
    vampytest.assert_eq(sticker.description, description)
    vampytest.assert_is(sticker.format, sticker_format)
    vampytest.assert_eq(sticker.name, name)
    vampytest.assert_eq(sticker.pack_id, pack_id)
    vampytest.assert_eq(sticker.sort_value, sort_value)
    vampytest.assert_eq(sticker.tags, frozenset(tags))
    vampytest.assert_is(sticker.type, sticker_type)
    vampytest.assert_is(sticker.user, user)


def test__Sticker__create_empty():
    """
    Tests whether ``Sticker._create_empty˙˙ works as intended.
    """
    sticker_id = 202201070002
    
    sticker = Sticker._create_empty(sticker_id)
    _assert_fields_set(sticker)
    
    vampytest.assert_eq(sticker.id, sticker_id)


def test__Sticker__precreate__0():
    """
    Tests whether ``Sticker.precreate`` works as intended.
    
    Case: No fields given.
    """
    sticker_id = 202201070003
    
    sticker = Sticker.precreate(sticker_id)
    _assert_fields_set(sticker)
    
    vampytest.assert_eq(sticker.id, sticker_id)


def test__Sticker__precreate__1():
    """
    Tests whether ``Sticker.precreate`` works as intended.
    
    Case: All fields given.
    """
    sticker_id = 202201070004
    guild_id = 202201070005
    
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070006
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070007)
    
    sticker = Sticker.precreate(
        sticker_id,
        guild_id = guild_id,
        available = available,
        description = description,
        name = name,
        pack_id = pack_id,
        sort_value = sort_value,
        sticker_format = sticker_format,
        sticker_type = sticker_type,
        tags = tags,
        user = user,
    )
    _assert_fields_set(sticker)
    
    vampytest.assert_eq(sticker.available, available)
    vampytest.assert_eq(sticker.description, description)
    vampytest.assert_is(sticker.format, sticker_format)
    vampytest.assert_eq(sticker.name, name)
    vampytest.assert_eq(sticker.pack_id, pack_id)
    vampytest.assert_eq(sticker.sort_value, sort_value)
    vampytest.assert_eq(sticker.tags, frozenset(tags))
    vampytest.assert_is(sticker.type, sticker_type)
    vampytest.assert_is(sticker.user, user)
    
    vampytest.assert_eq(sticker.id, sticker_id)
    vampytest.assert_eq(sticker.guild_id, guild_id)


def test__Sticker__precreate__2():
    """
    Tests whether ``Sticker.precreate`` works as intended.
    
    Case: Caching.
    """
    sticker_id = 202201070008
    
    sticker = Sticker.precreate(sticker_id)
    test_sticker = Sticker.precreate(sticker_id)
    
    vampytest.assert_is(sticker, test_sticker)
