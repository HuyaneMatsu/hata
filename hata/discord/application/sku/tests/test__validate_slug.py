import vampytest

from ..fields import validate_slug


def _iter_options():
    yield None, None
    yield '', None
    yield 'https://orindance.party/', 'https://orindance.party/'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_slug__passing(input_value):
    """
    Tests whether `validate_slug` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | str`
    """
    return validate_slug(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_slug__type_error(input_value):
    """
    Tests whether `validate_slug` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_slug(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('a')
def test__validate_slug__value_error(input_value):
    """
    Tests whether `validate_slug` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    ValueError
    """
    validate_slug(input_value)
