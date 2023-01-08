import vampytest

from ...sticker import Sticker

from ..sticker_pack import StickerPack

from .test__StickerPack__constructor import _assert_fields_set


@vampytest.skip_if((not hasattr(Sticker, 'to_data')) or (not hasattr(Sticker, 'from_data')))
def test__StickerPack__from_data__0():
    """
    Tests whether ``StickerPack.from_data`` works as intended.
    
    Case: Generic.
    """
    sticker_pack_id = 202201060014
    
    banner_id = 202201060015
    cover_sticker_id = 202201060016
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060017
    stickers = [Sticker.precreate(202201060018), Sticker.precreate(202201060019)]
    
    data = {
        'id': str(sticker_pack_id),
        'banner_asset_id': str(banner_id),
        'cover_sticker_id': str(cover_sticker_id),
        'description': description,
        'name': name,
        'sku_id': str(sku_id),
        'stickers': [sticker.to_data(defaults = True, include_internals = True) for sticker in stickers],
    }
    
    sticker_pack = StickerPack.from_data(data)
    _assert_fields_set(sticker_pack)
    
    vampytest.assert_eq(sticker_pack.id, sticker_pack_id)
    
    vampytest.assert_eq(sticker_pack.banner_id, banner_id)
    vampytest.assert_eq(sticker_pack.cover_sticker_id, cover_sticker_id)
    vampytest.assert_eq(sticker_pack.description, description)
    vampytest.assert_eq(sticker_pack.name, name)
    vampytest.assert_eq(sticker_pack.sku_id, sku_id)
    vampytest.assert_eq(sticker_pack.stickers, frozenset(stickers))


def test__StickerPack__from_data__1():
    """
    Tests whether ``StickerPack.from_data`` works as intended.
    
    Case: Caching.
    """
    sticker_pack_id = 202201060020
    
    data = {
        'id':str(sticker_pack_id),
    }
    
    sticker_pack = StickerPack.from_data(data)
    test_sticker_pack = StickerPack.from_data(data)
    
    vampytest.assert_is(sticker_pack, test_sticker_pack)



@vampytest.skip_if((not hasattr(Sticker, 'to_data')))
def test__StickerPack__to_data():
    """
    Tests whether ``StickerPack.to_data`` works as intended.
    
    Case: include defaults.
    """
    sticker_pack_id = 202201060021
    
    banner_id = 202201060022
    cover_sticker_id = 202201060023
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060024
    stickers = [Sticker.precreate(202201060025), Sticker.precreate(202201060026)]
    
    sticker_pack = StickerPack.precreate(
        sticker_pack_id,
        banner_id = banner_id,
        cover_sticker_id = cover_sticker_id,
        description = description,
        name = name,
        sku_id = sku_id,
        stickers = stickers,
    )
    
    expected_output = {
        'id': str(sticker_pack_id),
        'banner_asset_id': str(banner_id),
        'cover_sticker_id': str(cover_sticker_id),
        'description': description,
        'name': name,
        'sku_id': str(sku_id),
        'stickers': [sticker.to_data(defaults = True, include_internals = True) for sticker in stickers],
    }
    
    vampytest.assert_eq(
        sticker_pack.to_data(defaults = True),
        expected_output,
    )


@vampytest.skip_if((not hasattr(Sticker, 'to_data')) or (not hasattr(Sticker, 'from_data')))
def test__StickerPack__set_attributes():
    """
    Tests whether ``StickerPack._set_attributes`` works as intended.
    
    Case: Generic.
    """
    banner_id = 202201060027
    cover_sticker_id = 202201060028
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060029
    stickers = [Sticker.precreate(202201060030), Sticker.precreate(202201060031)]
    
    data = {
        'banner_asset_id': str(banner_id),
        'cover_sticker_id': str(cover_sticker_id),
        'description': description,
        'name': name,
        'sku_id': str(sku_id),
        'stickers': [sticker.to_data(defaults = True, include_internals = True) for sticker in stickers],
    }
    
    sticker_pack = StickerPack()
    sticker_pack._set_attributes(data)
    
    vampytest.assert_eq(sticker_pack.banner_id, banner_id)
    vampytest.assert_eq(sticker_pack.cover_sticker_id, cover_sticker_id)
    vampytest.assert_eq(sticker_pack.description, description)
    vampytest.assert_eq(sticker_pack.name, name)
    vampytest.assert_eq(sticker_pack.sku_id, sku_id)
    vampytest.assert_eq(sticker_pack.stickers, frozenset(stickers))
