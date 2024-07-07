import vampytest

from ..constants import DURATION_DEFAULT
from ..fields import validate_duration


def _iter_options__passing():
    yield None, DURATION_DEFAULT
    yield 3600, 3600


def _iter_options__value_error():
    # under min
    yield -3600
    yield 0
    
    # over max
    yield 3600 * 24 * 32 + 3600
    
    # not % 3600 = 0
    yield 1


def _iter_options__type_error():
    yield 'senya'


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
