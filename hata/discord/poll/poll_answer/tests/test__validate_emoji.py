import vampytest

from ....emoji import Emoji

from ..fields import validate_emoji


def _iter_options__passing():
    emoji = Emoji.precreate(202404120002)
    
    yield None, None
    yield emoji, emoji


def _iter_options__type_error():
    yield 12.56


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_emoji(input_value):
    """
    Tests whether ``validate_emoji`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | Emoji`
    
    Raises
    ------
    TypeError
    """
    output = validate_emoji(input_value)
    vampytest.assert_instance(output, Emoji, nullable = True)
    return output
