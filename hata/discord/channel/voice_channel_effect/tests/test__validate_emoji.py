import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import validate_emoji


def _iter_options__passing():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202309090002, name = 'met')
    
    yield None, None
    yield emoji_0, emoji_0
    yield emoji_1, emoji_1


def _iter_options__type_error():
    yield 'x'


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
