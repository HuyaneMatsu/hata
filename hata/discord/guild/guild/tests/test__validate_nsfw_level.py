import vampytest

from ..fields import validate_nsfw_level
from ..preinstanced import NsfwLevel


def _iter_options__passing():
    yield None, NsfwLevel.none
    yield NsfwLevel.safe, NsfwLevel.safe
    yield NsfwLevel.safe.value, NsfwLevel.safe


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_nsfw_level(input_value):
    """
    Tests whether `validate_nsfw_level` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``NsfwLevel``
    
    Raises
    ------
    TypeError
    """
    output = validate_nsfw_level(input_value)
    vampytest.assert_instance(output, NsfwLevel)
    return output
