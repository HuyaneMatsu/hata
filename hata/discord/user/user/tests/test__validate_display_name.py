import vampytest

from ..constants import DISPLAY_NAME_LENGTH_MAX
from ..fields import validate_display_name


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'
    yield 'aa', 'aa'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (DISPLAY_NAME_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_display_name(input_value):
    """
    Tests whether `validate_display_name` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `None`, `str`
        The value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_display_name(input_value)
