import vampytest

from ...emoji import Emoji

from ..request_helpers import get_emoji_id


def _iter_options__passing():
    emoji_id = 202407290000
    
    yield (
        emoji_id,
        emoji_id,
    )
    
    
    emoji_id = 202407290001
    
    yield (
        str(emoji_id),
        emoji_id,
    )
    
    
    emoji_id = 202407290002
    
    yield (
        Emoji.precreate(emoji_id),
        emoji_id,
    )
    
    
def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_emoji_id(input_value):
    """
    Tests whether ``get_emoji_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    return get_emoji_id(input_value)
