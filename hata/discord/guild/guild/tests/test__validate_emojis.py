import vampytest

from ....emoji import Emoji

from ..fields import validate_emojis


def _iter_options__passing():
    emoji_id_0 = 202306090003
    emoji_id_1 = 202306090050
    
    emoji_0 = Emoji.precreate(emoji_id_0, name = 'Koishi')
    emoji_1 = Emoji.precreate(emoji_id_1, name = 'Satori')
    
    yield None, {}
    yield [], {}
    yield {}, {}
    yield [emoji_0], {emoji_id_0: emoji_0}
    yield {emoji_id_0: emoji_0}, {emoji_id_0: emoji_0}
    yield [emoji_0, emoji_1], {emoji_id_0: emoji_0, emoji_id_1: emoji_1}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6: 12.6}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_emojis(input_value):
    """
    Tests whether ``validate_emojis`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `dict<int, Emoji>`
    
    Raises
    ------
    TypeError
    """
    output = validate_emojis(input_value)
    vampytest.assert_instance(output, dict)
    return output
