from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..name_plate import NamePlate
from ..preinstanced import Palette

from .test__NamePlate__constructor import _check_is_all_fields_set


def test__NamePlate__copy():
    """
    Tests whether ``NamePlate.copy`` works as intended.
    """
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270016
    
    
    name_plate = NamePlate(
        asset_path = asset_path,
        expires_at = expires_at,
        name = name,
        palette = palette,
        sku_id = sku_id,
    )
    copy = name_plate.copy()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(name_plate, copy)
    vampytest.assert_eq(name_plate, copy)


def test__NamePlate__copy_with__no_fields():
    """
    Tests whether ``NamePlate.copy_with`` works as intended.
    
    Case: No fields given.
    """
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270017
    
    
    name_plate = NamePlate(
        asset_path = asset_path,
        expires_at = expires_at,
        name = name,
        palette = palette,
        sku_id = sku_id,
    )
    copy = name_plate.copy_with()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(name_plate, copy)
    vampytest.assert_eq(name_plate, copy)


def test__NamePlate__copy_with__all_fields():
    """
    Tests whether ``NamePlate.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_asset_path = 'koishi/koishi/hat/'
    old_expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_name = 'KOISHI_KOISHI_HAT'
    old_palette = Palette.violet
    old_sku_id = 202505270018
    
    new_asset_path = 'koishi/koishi/eye/'
    new_expires_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_name = 'KOISHI_KOISHI_EYE'
    new_palette = Palette.green
    new_sku_id = 202505270019
    
    name_plate = NamePlate(
        asset_path = old_asset_path,
        expires_at = old_expires_at,
        name = old_name,
        palette = old_palette,
        sku_id = old_sku_id,
    )
    copy = name_plate.copy_with(
        asset_path = new_asset_path,
        expires_at = new_expires_at,
        name = new_name,
        palette = new_palette,
        sku_id = new_sku_id,
    )
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(name_plate, copy)

    vampytest.assert_eq(copy.asset_path, new_asset_path)
    vampytest.assert_eq(copy.expires_at, new_expires_at)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.palette, new_palette)
    vampytest.assert_eq(copy.sku_id, new_sku_id)


def _iter_options__url():
    yield 'koishi/koishi/hat/', True


@vampytest._(vampytest.call_from(_iter_options__url()).returning_last())
def test__NamePlate__url(asset_path):
    """
    Tests whether ``NamePlate.url`` works as intended.
    
    Parameters
    ----------
    asset_path : `str`
        Path to the name plate's asset.
    
    Returns
    -------
    has_url : `bool`
    """
    name_plate = NamePlate(asset_path = asset_path)
    output = name_plate.url
    vampytest.assert_instance(output, str)
    return (output is not None)
