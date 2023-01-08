import vampytest

from ...sticker import Sticker

from ..sticker_pack import StickerPack

from .test__StickerPack__constructor import _assert_fields_set


def test__StickerPack__copy():
    """
    Tests whether ``StickerPack.copy`` works as intended.
    """
    banner_id = 202201060053
    cover_sticker_id = 202201060054
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060055
    stickers = [Sticker.precreate(202201060056), Sticker.precreate(202201060057)]
    
    sticker_pack = StickerPack(
        banner_id = banner_id,
        cover_sticker_id = cover_sticker_id,
        description = description,
        name = name,
        sku_id = sku_id,
        stickers = stickers,
    )
    
    copy = sticker_pack.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sticker_pack, copy)
    
    vampytest.assert_eq(sticker_pack, copy)


def test__StickerPack__copy_with__0():
    """
    Tests whether ``StickerPack.copy_with`` works as intended.
    
    Case: No fields given.
    """
    banner_id = 202201060058
    cover_sticker_id = 202201060059
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060060
    stickers = [Sticker.precreate(202201060061), Sticker.precreate(202201060062)]
    
    sticker_pack = StickerPack(
        banner_id = banner_id,
        cover_sticker_id = cover_sticker_id,
        description = description,
        name = name,
        sku_id = sku_id,
        stickers = stickers,
    )
    
    copy = sticker_pack.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sticker_pack, copy)
    
    vampytest.assert_eq(sticker_pack, copy)


def test__StickerPack__copy_with__1():
    """
    Tests whether ``StickerPack.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_banner_id = 202201060063
    old_cover_sticker_id = 202201060064
    old_description = 'Kodemari'
    old_name = 'Koruri'
    old_sku_id = 202201060065
    old_stickers = [Sticker.precreate(202201060066), Sticker.precreate(202201060067)]
    
    new_banner_id = 202201060068
    new_cover_sticker_id = 202201060069
    new_description = 'Komeiji'
    new_name = 'Koishi'
    new_sku_id = 202201060070
    new_stickers = [Sticker.precreate(202201060071)]
    
    sticker_pack = StickerPack(
        banner_id = old_banner_id,
        cover_sticker_id = old_cover_sticker_id,
        description = old_description,
        name = old_name,
        sku_id = old_sku_id,
        stickers = old_stickers,
    )
    
    copy = sticker_pack.copy_with(
        banner_id = new_banner_id,
        cover_sticker_id = new_cover_sticker_id,
        description = new_description,
        name = new_name,
        sku_id = new_sku_id,
        stickers = new_stickers
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(sticker_pack, copy)
    
    vampytest.assert_eq(copy.banner_id, new_banner_id)
    vampytest.assert_eq(copy.cover_sticker_id, new_cover_sticker_id)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.sku_id, new_sku_id)
    vampytest.assert_eq(copy.stickers, frozenset(new_stickers))


def test__StickerPack__partial():
    """
    Tests whether ``StickerPack.partial`` works as intended.
    """
    sticker_pack_id = 202201060072
    
    sticker_pack = StickerPack.precreate(sticker_pack_id)
    vampytest.assert_false(sticker_pack.partial)
    
    sticker_pack = StickerPack()
    vampytest.assert_true(sticker_pack.partial)


def test__StickerPack__iter_stickers():
    """
    Tests whether ``StickerPack.iter_stickers`` works as intended.
    """
    sticker_0 = Sticker.precreate(202201060073)
    sticker_1 = Sticker.precreate(202201060074)
    
    for input_value, expected_output in (
        (None, set()),
        ([sticker_0], {sticker_0}),
        ([sticker_0, sticker_1], {sticker_0, sticker_1}),
    ):
        sticker_pack = StickerPack(stickers = input_value)
        vampytest.assert_eq({*sticker_pack.iter_stickers()}, expected_output)


def test__StickerPack__has_sticker():
    """
    Tests whether ``StickerPack.has_sticker` works as intended.
    """
    sticker_0 = Sticker.precreate(202201060075)
    sticker_1 = Sticker.precreate(202201060076)
    
    for input_stickers, sticker, expected_output in (
        (None, sticker_0, False),
        ([sticker_0], sticker_0, True),
        ([sticker_1], sticker_0, False),
    ):
        sticker_pack = StickerPack(stickers = input_stickers)
        vampytest.assert_eq(sticker_pack.has_sticker(sticker), expected_output)


def test__StickerPack__banner_url():
    """
    Tests whether ``StickerPack.banner_url` works as intended.
    """
    sticker_pack = StickerPack()
    vampytest.assert_is(sticker_pack.banner_url, None)
    
    sticker_pack = StickerPack(banner_id = 202201060077)
    vampytest.assert_instance(sticker_pack.banner_url, str)
