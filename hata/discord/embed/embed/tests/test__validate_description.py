import vampytest

from ..constants import EMBED_DESCRIPTION_LENGTH_MAX
from ..fields import validate_description


def _iter_options():
    yield None, None
    yield '', None
    yield 'a', 'a'
    yield 1, '1'


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


@vampytest.raising(ValueError)
@vampytest.call_with('a' * (EMBED_DESCRIPTION_LENGTH_MAX + 1))
def test__validate_description__value_error(input_value):
    """
    Tests whether `validate_description` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    ValueError
    """
    validate_description(input_value)
