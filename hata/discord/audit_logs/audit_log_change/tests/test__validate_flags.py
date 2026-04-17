import vampytest

from ..fields import validate_flags


def _iter_options__passing():
    yield None, 0
    yield 0, 0
    yield 1, 1


def _iter_options__type_error():
    yield 'a'
    yield 12.6


def _iter_options__value_error():
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_flags(input_value):
    """
    Tests whether `validate_flags` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    value : `int`
    
    Raises
    ------
    TypeError
    """
    output = validate_flags(input_value)
    vampytest.assert_instance(output, int)
    return output
