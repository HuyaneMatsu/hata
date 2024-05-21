import vampytest

from ..constants import TAG_LENGTH_MAX, TAG_LENGTH_MIN
from ..fields import validate_tag


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'aaaa', 'aaaa'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (TAG_LENGTH_MAX + 1)
    yield 'a' * (TAG_LENGTH_MIN - 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_tag(input_value):
    """
    Tests whether `validate_tag` works as intended.
    
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
    return validate_tag(input_value)
