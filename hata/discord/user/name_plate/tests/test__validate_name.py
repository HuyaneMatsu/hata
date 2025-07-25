import vampytest

from ..fields import validate_name


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'COLLECTIBLES_NAMEPLATES_CITYSCAPE_A11Y', 'COLLECTIBLES_NAMEPLATES_CITYSCAPE_A11Y'


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
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
