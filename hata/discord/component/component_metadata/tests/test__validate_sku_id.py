import vampytest

from ....application import SKU

from ..fields import validate_sku_id


def _iter_options__passing():
    sku_id = 202405180072
    
    yield 0, 0
    yield sku_id, sku_id
    yield str(sku_id), sku_id
    yield None, 0
    yield SKU.precreate(sku_id), sku_id


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield -1
    yield '1111111111111111111111'
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_sku_id(input_value):
    """
    Tests whether `validate_sku_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_sku_id(input_value)
