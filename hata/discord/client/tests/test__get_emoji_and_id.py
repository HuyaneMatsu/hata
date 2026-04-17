import vampytest

from ...emoji import Emoji

from ..request_helpers import get_emoji_and_id


def _iter_options__passing():
    emoji_id = 202407290020
    
    yield (
        emoji_id,
        [],
        (None, emoji_id),
    )
    
    
    emoji_id = 202407290021
    
    yield (
        str(emoji_id),
        [],
        (None, emoji_id),
    )
    
    
    emoji_id = 202407290022
    emoji = Emoji.precreate(emoji_id) 
    
    yield (
        emoji,
        [emoji],
        (emoji, emoji_id),
    )
    
    
    emoji_id = 202407290023
    emoji = Emoji.precreate(emoji_id) 
    
    yield (
        emoji_id,
        [emoji],
        (emoji, emoji_id),
    )


def _iter_options__type_error():
    yield None, []
    yield 12.6, []


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_emoji_and_id(input_value, extra):
    """
    Tests whether ``get_emoji_and_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    extra : `list<object>`
        Extra objects to keep in cache.
    
    Returns
    -------
    output : `(None | Emoji, int)`
    
    Raises
    ------
    TypeError
    """
    return get_emoji_and_id(input_value)
