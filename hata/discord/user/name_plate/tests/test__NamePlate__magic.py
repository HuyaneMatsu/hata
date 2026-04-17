from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..name_plate import NamePlate
from ..preinstanced import Palette


def test__NamePlate__repr():
    """
    Tests whether ``NamePlate.__repr__`` works as intended.
    """
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270013
    
    name_plate = NamePlate(
        asset_path = asset_path,
        expires_at = expires_at,
        name = name,
        palette = palette,
        sku_id = sku_id,
    )
    
    output = repr(name_plate)
    vampytest.assert_instance(output, str)


def test__NamePlate__hash():
    """
    Tests whether ``NamePlate.__hash__`` works as intended.
    """
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270014
    
    name_plate = NamePlate(
        asset_path = asset_path,
        expires_at = expires_at,
        name = name,
        palette = palette,
        sku_id = sku_id,
    )
    
    output = hash(name_plate)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    asset_path = 'koishi/koishi/hat/'
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    name = 'KOISHI_KOISHI_HAT'
    palette = Palette.violet
    sku_id = 202505270015
    
    keyword_parameters = {
        'asset_path': asset_path,
        'expires_at': expires_at,
        'name': name,
        'palette': palette,
        'sku_id': sku_id,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'asset_path': 'koishi/koishi/eye/',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'expires_at': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sku_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'KOISHI_KOISHI_EYE',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'palette': Palette.green,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__NamePlate__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``NamePlate.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    name_plate_0 = NamePlate(**keyword_parameters_0)
    name_plate_1 = NamePlate(**keyword_parameters_1)
    
    output = name_plate_0 == name_plate_1
    vampytest.assert_instance(output, bool)
    return output
