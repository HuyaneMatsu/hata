import vampytest

from ...sku import SKU

from ..fields import validate_sku_id


def _iter_options__passing():
    sku_id = 202310020006
    
    yield 0, 0
    yield sku_id, sku_id
    yield str(sku_id), sku_id
    yield None, 0
    yield SKU.precreate(sku_id), sku_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_sku_id__passing(input_value):
    """
    Tests whether `validate_sku_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    """
    return validate_sku_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_sku_id__type_error(input_value):
    """
    Tests whether `validate_sku_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_sku_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_sku_id__value_error(input_value):
    """
    Tests whether `validate_sku_id` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_sku_id(input_value)
