import vampytest

from ..fields import validate_code


def _iter_options():
    yield None, ''
    yield '', ''
    yield 'a', 'a'
    yield 'aa', 'aa'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_code__passing(input_value):
    """
    Tests whether `validate_code` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `None`, `str`
        The value to validate.
    
    Returns
    -------
    output : `str`
    """
    return validate_code(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_code__type_error(input_value):
    """
    Tests whether `validate_code` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_code(input_value)
