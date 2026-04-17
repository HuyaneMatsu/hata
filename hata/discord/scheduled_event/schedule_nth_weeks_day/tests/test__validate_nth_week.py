import vampytest

from ..fields import validate_nth_week


def _iter_options__passing():
    yield None, 1
    yield 1, 1
    yield 2, 2


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield 0
    yield 6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_nth_week(input_value):
    """
    Tests whether `validate_nth_week` works as intended.
    
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
    return validate_nth_week(input_value)
