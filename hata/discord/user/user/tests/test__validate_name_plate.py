import vampytest

from ...name_plate import NamePlate

from ..fields import validate_name_plate


def _iter_options__passing():
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030002,
    )
    
    yield None, None
    yield name_plate, name_plate


def _iter_options__type_error():
    yield 12.6



@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_name_plate(input_value):
    """
    Tests whether `validate_name_plate` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | NamePlate``
    
    Raises
    ------
    TypeError
    """
    output = validate_name_plate(input_value)
    vampytest.assert_instance(output, NamePlate, nullable = True)
    return output
