import vampytest

from ..fields import validate_description


def _iter_options():
    yield None, None
    yield '', None
    yield 'a', 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_description__passing(input_value):
    """
    Tests whether `validate_description` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | str`
    """
    return validate_description(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_description__type_error(input_value):
    """
    Tests whether `validate_description` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_description(input_value)
