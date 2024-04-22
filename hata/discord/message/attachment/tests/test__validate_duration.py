import vampytest

from ..constants import DURATION_DEFAULT
from ..fields import validate_duration


def _iter_options__passing():
    yield None, DURATION_DEFAULT
    yield 1.0, 1.0


def _iter_options__value_error():
    yield -1.0


def _iter_options__type_error():
    yield 'senya'
    yield 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_duration(input_value):
    """
    Tests whether `validate_duration` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `float`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_duration(input_value)
