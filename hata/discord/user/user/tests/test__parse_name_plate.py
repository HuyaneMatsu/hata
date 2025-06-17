import vampytest

from ...name_plate import NamePlate

from ..fields import parse_name_plate


def _iter_options():
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030000,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'collectibles': None,
        },
        None,
    )
    
    yield (
        {
            'collectibles': {},
        },
        None,
    )
    
    yield (
        {
            'collectibles': {
                'nameplate': None,
            },
        },
        None,
    )
    
    yield (
        {
            'collectibles': {
                'nameplate': name_plate.to_data(),
            },
        },
        name_plate,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_name_plate(data):
    """
    Tests whether ``parse_name_plate`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | NamePlate``
    """
    output = parse_name_plate(data)
    vampytest.assert_instance(output, NamePlate, nullable = True)
    return output
