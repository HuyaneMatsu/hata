import vampytest

from ..fields import validate_uses


def _iter_options__passing():
    yield 0, 0
    yield 1, 1
    yield None, None


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_uses__passing(input_value):
    """
    Tests whether `validate_uses` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `None`, `int`
    """
    return validate_uses(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with('12')
def test__validate_uses__type_error(input_value):
    """
    Tests whether `validate_uses` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_uses(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with(-1)
def test__validate_uses__value_error(input_value):
    """
    Tests whether `validate_uses` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_uses(input_value)
