import vampytest

from ....user import User, ZEROUSER

from ..preinstanced import StickerFormat, StickerType
from ..sticker import Sticker


def test__Sticker__repr():
    """
    Tests whether ``Sticker.__repr__`` works as intended.
    """
    sticker_id = 202201070026
    guild_id = 202201070027
    
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070028
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070029)
    
    keyword_parameters = {
        'available': available,
        'description': description,
        'name': name,
        'pack_id': pack_id,
        'sort_value': sort_value,
        'sticker_format': sticker_format,
        'sticker_type': sticker_type,
        'tags': tags,
        'user': user,
    }
    
    sticker = Sticker(**keyword_parameters)
    vampytest.assert_instance(repr(sticker), str)
    
    sticker = Sticker.precreate(sticker_id, guild_id = guild_id, **keyword_parameters)
    vampytest.assert_instance(repr(sticker), str)


def test__Sticker__hash():
    """
    Tests whether ``Sticker.__hash__`` works as intended.
    """
    sticker_id = 202201070030
    guild_id = 202201070031
    
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070032
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070033)
    
    keyword_parameters = {
        'available': available,
        'description': description,
        'name': name,
        'pack_id': pack_id,
        'sort_value': sort_value,
        'sticker_format': sticker_format,
        'sticker_type': sticker_type,
        'tags': tags,
        'user': user,
    }
    
    sticker = Sticker(**keyword_parameters)
    vampytest.assert_instance(hash(sticker), int)
    
    sticker = Sticker.precreate(sticker_id, guild_id = guild_id, **keyword_parameters)
    vampytest.assert_instance(hash(sticker), int)


def test__Sticker__eq():
    """
    Tests whether ``Sticker.__eq__`` works as intended.
    """
    sticker_id = 202201070034
    guild_id = 202201070035
    
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070036
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070037)
    
    keyword_parameters = {
        'available': available,
        'description': description,
        'name': name,
        'pack_id': pack_id,
        'sort_value': sort_value,
        'sticker_format': sticker_format,
        'sticker_type': sticker_type,
        'tags': tags,
        'user': user,
    }
    
    sticker = Sticker.precreate(sticker_id, guild_id = guild_id, **keyword_parameters)
    vampytest.assert_eq(sticker, sticker)
    vampytest.assert_ne(sticker, object())
    
    test_sticker = Sticker(**keyword_parameters)
    vampytest.assert_eq(sticker, test_sticker)
    
    
    for field_name, field_value in (
        ('available', False),
        ('description', None),
        ('name', 'holo'),
        ('pack_id', 0),
        ('sort_value', 0),
        ('sticker_format', StickerFormat.none),
        ('sticker_type', StickerType.none),
        ('tags', None),
        ('user', ZEROUSER),
    ):
        test_sticker = Sticker(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(sticker, test_sticker)
            

def test__Sticker__format():
    """
    Tests whether ``Sticker.__format__`` works as intended.
    """
    sticker = Sticker()
    
    vampytest.assert_instance(format(sticker, ''), str)
    vampytest.assert_instance(format(sticker, 'c'), str)


def test__Sticker__sort():
    """
    Tests whether sorting stickers works as intended.
    """
    sticker_0 = Sticker.precreate(202201070038, sort_value = 0)
    sticker_1 = Sticker.precreate(202201070039, sort_value = 4)
    sticker_2 = Sticker.precreate(202201070040, sort_value = 0)
    
    vampytest.assert_eq(
        sorted([
            sticker_0, sticker_1, sticker_2
        ]), [
            sticker_0, sticker_2, sticker_1
        ],
    )
