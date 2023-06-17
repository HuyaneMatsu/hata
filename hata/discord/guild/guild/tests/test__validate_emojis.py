import vampytest

from ....emoji import Emoji

from ..fields import validate_emojis


def test__validate_emojis__0():
    """
    Tests whether ``validate_emojis`` works as intended.
    
    Case: passing.
    """
    emoji_id = 202306090003
    emoji_name = 'Koishi'
    
    emoji = Emoji.precreate(
        emoji_id,
        name = emoji_name,
    )
    
    for input_value, expected_output in (
        (None, {}),
        ([], {}),
        ({}, {}),
        ([emoji], {emoji_id: emoji}),
        ({emoji_id: emoji}, {emoji_id: emoji}),
    ):
        output = validate_emojis(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_emojis__1():
    """
    Tests whether ``validate_emojis`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_emojis(input_value)
