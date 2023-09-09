import vampytest

from ...core import BUILTIN_EMOJIS
from ...emoji import Emoji

from ..shared_fields import validate_emoji


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202309090000, name = 'met')
    
    yield None, None
    yield emoji_0, emoji_0
    yield emoji_1, emoji_1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_emoji__passing(input_value):
    """
    Tests whether ``validate_emoji`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``Emoji``
    """
    return validate_emoji(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('x')
def test__validate_emoji__type_error(input_value):
    """
    Tests whether ``validate_emoji`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_emoji(input_value)
