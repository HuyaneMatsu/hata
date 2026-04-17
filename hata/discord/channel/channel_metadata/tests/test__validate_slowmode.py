import vampytest

from ..fields import validate_slowmode


def _iter_options__passing():
    yield None, 0
    yield 0, 0
    yield 1, 1


def _iter_options__type_error():
    yield ''

def _iter_option__value_error():
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_option__value_error()).raising(ValueError))
def test__validate_slowmode(input_value):
    """
    Validates whether ``validate_slowmode`` works as intended.
    
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
    output = validate_slowmode(input_value)
    vampytest.assert_instance(output, int)
    return output
