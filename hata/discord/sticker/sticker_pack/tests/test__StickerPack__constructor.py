import vampytest

from ...sticker import Sticker

from ..sticker_pack import StickerPack


def _assert_fields_set(sticker_pack):
    """
    Asserts whether all fields are set of the given sticker pack.
    
    Parameters
    ----------
    sticker_pack : ``StickerPack``
        The sticker pack to check.
    """
    vampytest.assert_instance(sticker_pack, StickerPack)
    vampytest.assert_instance(sticker_pack.banner_id, int)
    vampytest.assert_instance(sticker_pack.cover_sticker_id, int)
    vampytest.assert_instance(sticker_pack.description, str, nullable = True)
    vampytest.assert_instance(sticker_pack.id, int)
    vampytest.assert_instance(sticker_pack.name, str)
    vampytest.assert_instance(sticker_pack.sku_id, int)
    vampytest.assert_instance(sticker_pack.stickers, frozenset, nullable = True)


def test__StickerPack__new__0():
    """
    Tests whether ``StickerPack.__new__`` works as intended.
    
    Case: No fields given.
    """
    sticker_pack = StickerPack()
    _assert_fields_set(sticker_pack)


def test__StickerPack__new__1():
    """
    Tests whether ``StickerPack.__new__`` works as intended.
    
    Case: All fields given.
    """
    banner_id = 202201060000
    cover_sticker_id = 202201060001
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060002
    stickers = [Sticker.precreate(202201060003), Sticker.precreate(202201060004)]
    
    sticker_pack = StickerPack(
        banner_id = banner_id,
        cover_sticker_id = cover_sticker_id,
        description = description,
        name = name,
        sku_id = sku_id,
        stickers = stickers,
    )
    _assert_fields_set(sticker_pack)
    
    vampytest.assert_eq(sticker_pack.banner_id, banner_id)
    vampytest.assert_eq(sticker_pack.cover_sticker_id, cover_sticker_id)
    vampytest.assert_eq(sticker_pack.description, description)
    vampytest.assert_eq(sticker_pack.name, name)
    vampytest.assert_eq(sticker_pack.sku_id, sku_id)
    vampytest.assert_eq(sticker_pack.stickers, frozenset(stickers))


def test__StickerPack__create_empty():
    """
    Tests whether ``StickerPack._create_empty`` works as intended.
    """
    sticker_pack_id = 202201060005
    
    sticker_pack = StickerPack._create_empty(sticker_pack_id)
    _assert_fields_set(sticker_pack)
    
    vampytest.assert_eq(sticker_pack.id, sticker_pack_id)


def test__StickerPack__precreate__0():
    """
    Tests whether ``StickerPack.precreate`` works as intended.
    
    Case: No fields given.
    """
    sticker_pack_id = 20220106006
    
    sticker_pack = StickerPack.precreate(sticker_pack_id)
    _assert_fields_set(sticker_pack)
    
    vampytest.assert_eq(sticker_pack.id, sticker_pack_id)


def test__StickerPack__precreate__1():
    """
    Tests whether ``StickerPack.precreate`` works as intended.
    
    Case: All fields given.
    """
    sticker_pack_id = 202201060007
    
    banner_id = 202201060008
    cover_sticker_id = 202201060009
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060010
    stickers = [Sticker.precreate(202201060011), Sticker.precreate(202201060012)]
    
    sticker_pack = StickerPack.precreate(
        sticker_pack_id,
        banner_id = banner_id,
        cover_sticker_id = cover_sticker_id,
        description = description,
        name = name,
        sku_id = sku_id,
        stickers = stickers,
    )
    _assert_fields_set(sticker_pack)
    
    vampytest.assert_eq(sticker_pack.id, sticker_pack_id)
    
    vampytest.assert_eq(sticker_pack.banner_id, banner_id)
    vampytest.assert_eq(sticker_pack.cover_sticker_id, cover_sticker_id)
    vampytest.assert_eq(sticker_pack.description, description)
    vampytest.assert_eq(sticker_pack.name, name)
    vampytest.assert_eq(sticker_pack.sku_id, sku_id)
    vampytest.assert_eq(sticker_pack.stickers, frozenset(stickers))

def test__StickerPack__precreate_2():
    """
    Tests whether ``StickerPack.precreate`` works as intended.
    
    Case: Caching
    """
    sticker_pack_id = 202201060013
    
    sticker_pack = StickerPack.precreate(sticker_pack_id)
    test_sticker_pack = StickerPack.precreate(sticker_pack_id)
    
    vampytest.assert_is(sticker_pack, test_sticker_pack)
