import vampytest

from ..fields import validate_nsfw_level
from ..preinstanced import NsfwLevel


def _iter_options():
    yield NsfwLevel.safe, NsfwLevel.safe
    yield NsfwLevel.safe.value, NsfwLevel.safe
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_nsfw_level__passing(input_value):
    """
    Tests whether `validate_nsfw_level` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``NsfwLevel``
    """
    return validate_nsfw_level(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_nsfw_level__type_error(input_value):
    """
    Tests whether `validate_nsfw_level` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_nsfw_level(input_value)
