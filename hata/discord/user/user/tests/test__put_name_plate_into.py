import vampytest

from ...name_plate import NamePlate

from ..fields import put_name_plate


def _iter_options():
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030001,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'collectibles': {
                'nameplate': None,
            },
        },
    )
    
    yield (
        name_plate,
        False,
        {
            'collectibles': {
                'nameplate': name_plate.to_data(defaults = False),
            },
        },
    )
    
    yield (
        name_plate,
        True,
        {
            'collectibles': {
                'nameplate': name_plate.to_data(defaults = True),
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_name_plate(input_value, defaults):
    """
    Tests whether ``put_name_plate`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_name_plate(input_value, {}, defaults)
