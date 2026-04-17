import vampytest

from ..constants import STATUS_LENGTH_MAX
from ..fields import validate_status


def _iter_options():
    yield None, None
    yield '', None
    yield 'a', 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_status__passing(input_value):
    """
    Tests whether `validate_status` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None`, `str`
    """
    return validate_status(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_status__type_error(input_value):
    """
    Tests whether `validate_status` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_status(input_value)



@vampytest.raising(ValueError)
@vampytest.call_with('a' * (STATUS_LENGTH_MAX + 1))
def test__validate_status__value_error(input_value):
    """
    Tests whether `validate_status` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    ValueError
    """
    validate_status(input_value)
