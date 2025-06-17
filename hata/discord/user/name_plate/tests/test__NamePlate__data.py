from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_unix_time

from ..name_plate import NamePlate
from ..preinstanced import Palette

from .test__NamePlate__constructor import _check_is_all_fields_set


def test__NamePlate__from_data():
    """
    Tests whether ``NamePlate.from_data`` works as intended.
    """
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270011
    
    data = {
        'asset': asset_path,
        'expires_at': datetime_to_unix_time(expires_at),
        'label': name,
        'palette': palette.value,
        'sku_id': str(sku_id),
    }
    
    name_plate = NamePlate.from_data(data)
    _check_is_all_fields_set(name_plate)
    
    vampytest.assert_eq(name_plate.asset_path, asset_path)
    vampytest.assert_eq(name_plate.expires_at, expires_at)
    vampytest.assert_eq(name_plate.name, name)
    vampytest.assert_is(name_plate.palette, palette)
    vampytest.assert_eq(name_plate.sku_id, sku_id)


def test__NamePlate__to_data():
    """
    Tests whether ``NamePlate.to_data`` works as intended.
    
    Case: Include defaults.
    """
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270012
    
    name_plate = NamePlate(
        asset_path = asset_path,
        expires_at = expires_at,
        name = name,
        palette = palette,
        sku_id = sku_id,
    )
    
    vampytest.assert_eq(
        name_plate.to_data(
            defaults = True,
        ),
        {
            'asset': asset_path,
            'expires_at': datetime_to_unix_time(expires_at),
            'label': name,
            'palette': palette.value,
            'sku_id': str(sku_id),
        },
    )
