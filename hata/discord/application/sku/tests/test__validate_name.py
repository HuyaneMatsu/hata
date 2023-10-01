import vampytest

from ..constants import NAME_LENGTH_MAX
from ..fields import validate_name


def _iter_options():
    yield None, ''
    yield '', ''
    yield 'aa', 'aa'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_name__passing(input_value):
    """
    Tests whether `validate_name` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `None`, `str`
        The value to validate.
    
    Returns
    -------
    output : `str`
    """
    return validate_name(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_name__type_error(input_value):
    """
    Tests whether `validate_name` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_name(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('a' * (NAME_LENGTH_MAX + 1))
def test__validate_name__value_error(input_value):
    """
    Tests whether `validate_name` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `None`, `str`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    return validate_name(input_value)
