import vampytest

from ..constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN
from ..fields import validate_name


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'aa', 'aa'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (NAME_LENGTH_MAX + 1)
    yield 'a' * (NAME_LENGTH_MIN - 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_name(input_value):
    """
    Tests whether `validate_name` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_name(input_value)
