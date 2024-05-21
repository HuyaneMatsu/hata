import vampytest

from ..constants import NAME_LENGTH_MAX
from ..fields import validate_name


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'
    yield 'aa', 'aa'
    yield 1, '1'
    yield 12.6, '12.6'


def _iter_options__value_error():
    yield 'a' * (NAME_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
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
    ValueError
    """
    return validate_name(input_value)
