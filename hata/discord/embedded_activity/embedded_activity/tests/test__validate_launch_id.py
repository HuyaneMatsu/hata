import vampytest

from ..fields import validate_launch_id


def _iter_options__passing():
    launch_id = 202409010066
    
    yield 0, 0
    yield launch_id, launch_id
    yield str(launch_id), launch_id


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_launch_id(input_value):
    """
    Tests whether `validate_launch_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_launch_id(input_value)
    vampytest.assert_instance(output, int)
    return output
