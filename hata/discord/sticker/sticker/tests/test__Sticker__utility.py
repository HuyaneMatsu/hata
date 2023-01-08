import vampytest

from ....client import Client
from ....guild import Guild
from ....user import User

from ...sticker_pack import StickerPack

from ..preinstanced import StickerFormat, StickerType
from ..sticker import Sticker

from .test__Sticker__constructor import _assert_fields_set


def test__Sticker__copy():
    """
    Tests whether ``Sticker.copy`` works as intended.
    """
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070041
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070042)
    
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
    
    copy = sticker.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, sticker)
        
    vampytest.assert_eq(sticker, copy)


def test__Sticker__copy_with__0():
    """
    Tests whether ``Sticker.copy_with`` works as intended.
    
    Case: No fields given.
    """
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070043
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070044)
    
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
    
    copy = sticker.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, sticker)
        
    vampytest.assert_eq(sticker, copy)


def test__Sticker__copy_with__1():
    """
    Tests whether ``Sticker.copy_with`` works as intended.
    
    Case: No fields given.
    """
    old_available = True
    old_description = 'komeiji'
    old_name = 'koishi'
    old_pack_id = 202201070045
    old_sort_value = 4
    old_sticker_format = StickerFormat.png
    old_sticker_type = StickerType.guild
    old_tags = ['rin', 'okuu']
    old_user = User.precreate(202201070046)
    new_available = False
    new_description = 'Fujiwara no'
    new_name = 'Mokou'
    new_pack_id = 202201070046
    new_sort_value = 2
    new_sticker_format = StickerFormat.apng
    new_sticker_type = StickerType.standard
    new_tags = ['phoenix']
    new_user = User.precreate(202201070048)
    
    sticker = Sticker(
        available = old_available,
        description = old_description,
        name = old_name,
        pack_id = old_pack_id,
        sort_value = old_sort_value,
        sticker_format = old_sticker_format,
        sticker_type = old_sticker_type,
        tags = old_tags,
        user = old_user,
    )
    
    copy = sticker.copy_with(
        available = new_available,
        description = new_description,
        name = new_name,
        pack_id = new_pack_id,
        sort_value = new_sort_value,
        sticker_format = new_sticker_format,
        sticker_type = new_sticker_type,
        tags = new_tags,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, sticker)
    
    vampytest.assert_eq(copy.available, new_available)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_is(copy.format, new_sticker_format)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.pack_id, new_pack_id)
    vampytest.assert_eq(copy.sort_value, new_sort_value)
    vampytest.assert_eq(copy.tags, frozenset(new_tags))
    vampytest.assert_is(copy.type, new_sticker_type)
    vampytest.assert_is(copy.user, new_user)


def test__Sticker__partial():
    """
    Tests whether ``Sticker.partial`` works as intended.
    """
    sticker = Sticker()
    vampytest.assert_true(sticker.partial)
    
    sticker_id = 202301010049
    guild_id = 202301010050
    sticker = Sticker.precreate(sticker_id, guild_id = guild_id, sticker_type = StickerType.guild)
    vampytest.assert_true(sticker.partial)
    
    
    sticker_id = 202301010051
    guild_id = 202301010052
    guild = Guild.precreate(guild_id)
    sticker = Sticker.precreate(sticker_id, guild_id = guild_id, sticker_type = StickerType.guild)
    guild.stickers[sticker_id] = sticker
    vampytest.assert_true(sticker.partial)
    
    
    client = Client(
        token = 'token_20230107_0000',
    )
    
    try:
        sticker_id = 202301010053
        guild_id = 202301010054
        guild = Guild.precreate(guild_id)
        guild.clients.append(client)
        sticker = Sticker.precreate(sticker_id, guild_id = guild_id, sticker_type = StickerType.guild)
        guild.stickers[sticker_id] = sticker
        vampytest.assert_false(sticker.partial)
        
    # Cleanup
    finally:
        client._delete()
        client = None
        clients = None

    
    sticker_id = 202301010055
    sticker_pack_id = 202301010056
    sticker = Sticker.precreate(sticker_id, pack_id = sticker_pack_id, sticker_type = StickerType.standard)
    vampytest.assert_true(sticker.partial)
    

    sticker_id = 202301010057
    sticker_pack_id = 202301010058
    sticker = Sticker.precreate(sticker_id, pack_id = sticker_pack_id, sticker_type = StickerType.standard)
    sticker_pack = StickerPack.precreate(sticker_pack_id)
    vampytest.assert_true(sticker.partial)

    sticker_id = 202301010059
    sticker_pack_id = 202301010060
    sticker = Sticker.precreate(sticker_id, pack_id = sticker_pack_id, sticker_type = StickerType.standard)
    sticker_pack = StickerPack.precreate(sticker_pack_id, stickers = [sticker])
    vampytest.assert_false(sticker.partial)


def test__sticker__url():
    """
    Tests whether ``Sticker.url`` works as intended.
    """
    sticker = Sticker()
    vampytest.assert_is(sticker.url, None)

    sticker_id = 202301010066
    sticker_format = StickerFormat.png
    sticker = Sticker.precreate(sticker_id, sticker_format = sticker_format)
    vampytest.assert_instance(sticker.url, str)
    

def test__sticker__url_as():
    """
    Tests whether ``Sticker.url_as`` works as intended.
    """
    sticker = Sticker()
    vampytest.assert_is(sticker.url_as(), None)
    
    sticker_id = 202301010067
    sticker_format = StickerFormat.png
    sticker = Sticker.precreate(sticker_id, sticker_format = sticker_format)
    vampytest.assert_instance(sticker.url_as(), str)


def test__Sticker__guild():
    """
    Tests whether ``Sticker.guild`` works as intended.
    """
    sticker_id = 202301010061
    sticker = Sticker.precreate(sticker_id)
    vampytest.assert_is(sticker.guild, None)
    
    sticker_id = 202301010062
    guild_id = 202301010063
    sticker = Sticker.precreate(sticker_id, guild_id = guild_id)
    vampytest.assert_is(sticker.guild, None)
    
    sticker_id = 202301010064
    guild_id = 202301010065
    guild = Guild.precreate(guild_id)
    sticker = Sticker.precreate(sticker_id, guild_id = guild_id)
    vampytest.assert_is(sticker.guild, guild)


def test__Sticker__iter_tags():
    """
    Tests whether ``Sticker.iter_tags`` works as intended.
    """ 
    for input_value, expected_output in (
        (None, set()),
        (['howling'], {'howling'}),
        (['howling', 'moon'], {'howling', 'moon'}),
    ):
        sticker = Sticker(tags = input_value)
        vampytest.assert_eq({*sticker.iter_tags()}, expected_output)


def test__Sticker__has_tag():
    """
    Tests whether ``Sticker.has_tag` works as intended.
    """
    tag_0 = 'howling'
    tag_1 = 'moon'
    
    for input_tags, tag, expected_output in (
        (None, tag_0, False),
        ([tag_0], tag_0, True),
        ([tag_1], tag_0, False),
    ):
        tag_pack = Sticker(tags = input_tags)
        vampytest.assert_eq(tag_pack.has_tag(tag), expected_output)
