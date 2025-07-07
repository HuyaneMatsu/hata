from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..name_plate import NamePlate
from ..preinstanced import Palette


def _assert_fields_set(name_plate):
    """
    Asserts whether all fields of the given name plate are set.
    
    Parameters
    ----------
    name_plate : ``NamePlate``
    """
    vampytest.assert_instance(name_plate, NamePlate)
    vampytest.assert_instance(name_plate.asset_path, str)
    vampytest.assert_instance(name_plate.expires_at, DateTime, nullable = True)
    vampytest.assert_instance(name_plate.name, str)
    vampytest.assert_instance(name_plate.palette, Palette)
    vampytest.assert_instance(name_plate.sku_id, int)


def test__NamePlate__new__no_fields():
    """
    Tests whether ``NamePlate.__new__`` works as intended.
    
    Case: No parameters.
    """
    name_plate = NamePlate()
    _assert_fields_set(name_plate)


def test__NamePlate__new__all_fields():
    """
    Tests whether ``NamePlate.__new__`` works as intended.
    
    Case: all fields.
    """
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270010
    
    
    name_plate = NamePlate(
        asset_path = asset_path,
        expires_at = expires_at,
        name = name,
        palette = palette,
        sku_id = sku_id,
    )
    _assert_fields_set(name_plate)
    
    vampytest.assert_eq(name_plate.asset_path, asset_path)
    vampytest.assert_eq(name_plate.expires_at, expires_at)
    vampytest.assert_eq(name_plate.name, name)
    vampytest.assert_is(name_plate.palette, palette)
    vampytest.assert_eq(name_plate.sku_id, sku_id)
