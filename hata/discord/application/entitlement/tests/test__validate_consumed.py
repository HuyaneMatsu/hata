import vampytest

from ..fields import validate_consumed


def _iter_options():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_consumed__passing(input_value):
    """
    Tests whether `validate_consumed` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `bool`
    """
    return validate_consumed(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_consumed__type_error(input_value):
    """
    Tests whether `validate_consumed` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_consumed(input_value)
