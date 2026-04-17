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


def test__Sticker__copy_with__no_fields():
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


def test__Sticker__copy_with__all_fields():
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


def _iter_options__iter_tags():
    tag_0 = 'howling'
    tag_1 = 'moon'
    
    yield None, set()
    yield [tag_0], {tag_0}
    yield [tag_0, tag_1], {tag_0, tag_1}


@vampytest._(vampytest.call_from(_iter_options__iter_tags()).returning_last())
def test__Sticker__iter_tags(tags):
    """
    Tests whether ``Sticker.iter_tags`` works as intended.
    
    Parameters
    ----------
    tags : `None | list<str>`
        tag to create sticker with.
    
    Returns
    -------
    output : `set<str>`
    """ 
    sticker = Sticker(tags = tags)
    output = {*sticker.iter_tags()}
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output


def _iter_options__has_tag():
    tag_0 = 'howling'
    tag_1 = 'moon'
    
    yield None, tag_0, False
    yield [tag_0], tag_0, True
    yield [tag_1], tag_0, False


@vampytest._(vampytest.call_from(_iter_options__has_tag()).returning_last())
def test__Sticker__has_tag(tags, tag):
    """
    Tests whether ``Sticker.has_tag` works as intended.
    
    Parameters
    ----------
    tags : `None | list<str>`
        tag to create sticker with.
    
    tag : `str`
        Tag to test with.
    
    Returns
    -------
    output : `bool`
    """
    sticker = Sticker(tags = tags)
    output = sticker.has_tag(tag)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__url():
    yield 202506010020, StickerFormat.none, False
    yield 202506010021, StickerFormat.png, True
    yield 202506010022, StickerFormat.apng, True
    yield 202506010023, StickerFormat.lottie, True
    yield 202506010024, StickerFormat.gif, True


@vampytest._(vampytest.call_from(_iter_options__url()).returning_last())
def test__Sticker__url(sticker_id, sticker_format):
    """
    Tests whether ``Sticker.url`` works as intended.
    
    Parameters
    ----------
    sticker_id : `int`
        Identifier to create Sticker with.
    
    sticker_format : ``StickerFormat``
        The sticker's format.
    
    Returns
    -------
    has_url : `bool`
    """
    sticker = Sticker.precreate(
        sticker_id,
        sticker_format = sticker_format,
    )
    
    output = sticker.url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__url_as():
    yield 202506010025, StickerFormat.none, {'size': 128, 'preview': True}, False
    yield 202506010026, StickerFormat.png, {'size': 128, 'preview': True}, True
    yield 202506010027, StickerFormat.apng, {'size': 128, 'preview': True}, True
    yield 202506010028, StickerFormat.lottie, {'size': 128, 'preview': True}, True
    yield 202506010029, StickerFormat.gif, {'size': 128, 'preview': True}, True


@vampytest._(vampytest.call_from(_iter_options__url_as()).returning_last())
def test__Sticker__url_as(sticker_id, sticker_format, keyword_parameters):
    """
    Tests whether ``Sticker.url_as`` works as intended.
    
    Parameters
    ----------
    sticker_id : `int`
        Identifier to create Sticker with.
    
    sticker_format : ``StickerFormat``
        The sticker's format.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_url : `bool`
    """
    sticker = Sticker.precreate(
        sticker_id,
        sticker_format = sticker_format,
    )
    
    output = sticker.url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
