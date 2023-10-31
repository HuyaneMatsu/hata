import vampytest

from ..fields import validate_flags


def iter_options__passing():
    yield 0, 0
    yield 1, 1


@vampytest._(vampytest.call_from(iter_options__passing()).returning_last())
def test__validate_flags__passing(input_value):
    """
    Tests whether `validate_flags` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The object to validate.
    
    Returns
    -------
    value : `int`
        The validated value.
    """
    return validate_flags(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with(-1)
def test__validate_flags__value_error(input_value):
    """
    Tests whether `validate_flags` works as intended.
    
    Case: value error.
    
    Parameters
    ----------
    input_value : `object`
        The object to validate.
    
    Raises
    ------
    ValueError
        The raises exception.
    """
    validate_flags(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('a')
def test__validate_flags__type_error(input_value):
    """
    Tests whether `validate_flags` works as intended.
    
    Case: type error
    
    Parameters
    ----------
    input_value : `object`
        The object to validate.
    
    Raises
    ------
    TypeError
        The raises exception.
    """
    validate_flags(input_value)
