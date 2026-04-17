import vampytest

from ...sticker import Sticker

from ..sticker_pack import StickerPack


def test__StickerPack__repr():
    """
    Tests whether ``StickerPack.__repr__`` works as intended.
    """
    sticker_pack_id = 202201060032
    
    banner_id = 202201060033
    cover_sticker_id = 202201060034
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060035
    stickers = [Sticker.precreate(202201060036), Sticker.precreate(202201060037)]
    
    keyword_parameters = {
        'banner_id': banner_id,
        'cover_sticker_id': cover_sticker_id,
        'description': description,
        'name': name,
        'sku_id': sku_id,
        'stickers': stickers,
    }
    
    sticker_pack = StickerPack(**keyword_parameters)
    vampytest.assert_instance(repr(sticker_pack), str)
    
    sticker_pack = StickerPack.precreate(sticker_pack_id, **keyword_parameters)
    vampytest.assert_instance(repr(sticker_pack), str)


def test__StickerPack__hash():
    """
    Tests whether ``StickerPack.__hash__`` works as intended.
    """
    sticker_pack_id = 202201060038
    
    banner_id = 202201060039
    cover_sticker_id = 202201060040
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060041
    stickers = [Sticker.precreate(202201060042), Sticker.precreate(202201060043)]
    
    keyword_parameters = {
        'banner_id': banner_id,
        'cover_sticker_id': cover_sticker_id,
        'description': description,
        'name': name,
        'sku_id': sku_id,
        'stickers': stickers,
    }
    
    sticker_pack = StickerPack(**keyword_parameters)
    vampytest.assert_instance(hash(sticker_pack), int)
    
    sticker_pack = StickerPack.precreate(sticker_pack_id, **keyword_parameters)
    vampytest.assert_instance(hash(sticker_pack), int)


def test__StickerPack__eq():
    """
    Tests whether ``StickerPack.__eq__`` works as intended.
    """
    sticker_pack_id = 202201060044
    
    banner_id = 202201060045
    cover_sticker_id = 202201060046
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060047
    stickers = [Sticker.precreate(202201060048), Sticker.precreate(202201060049)]
    
    keyword_parameters = {
        'banner_id': banner_id,
        'cover_sticker_id': cover_sticker_id,
        'description': description,
        'name': name,
        'sku_id': sku_id,
        'stickers': stickers,
    }
    
    sticker_pack = StickerPack.precreate(sticker_pack_id, **keyword_parameters)
    vampytest.assert_eq(sticker_pack, sticker_pack)
    
    test_sticker_pack = StickerPack(**keyword_parameters)
    vampytest.assert_eq(sticker_pack, test_sticker_pack)
    
    for field_name, field_value in (
        ('banner_id', 202201060050),
        ('cover_sticker_id', 202201060051),
        ('description', 'koishi'),
        ('name', 'ara'),
        ('sku_id', 202201060052),
        ('stickers', None),
    ):
        test_sticker_pack = StickerPack(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(sticker_pack, test_sticker_pack)
