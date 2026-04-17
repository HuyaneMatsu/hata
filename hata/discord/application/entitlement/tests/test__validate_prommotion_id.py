import vampytest

from ..fields import validate_promotion_id


def _iter_options__passing():
    promotion_id = 202507010002
    
    yield 0, 0
    yield promotion_id, promotion_id
    yield str(promotion_id), promotion_id


def _iter_options__type_error():
    yield None
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_promotion_id(input_value):
    """
    Tests whether `validate_promotion_id` works as intended.
    
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
    output = validate_promotion_id(input_value)
    vampytest.assert_instance(output, int)
    return output
