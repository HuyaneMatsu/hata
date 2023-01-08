import vampytest

from ....emoji import Emoji

from ..fields import validate_emojis


def test__validate_emojis__0():
    """
    Tests whether ``validate_emojis`` works as intended.
    
    Case: Passing.
    """
    emoji_0 = Emoji.precreate(202301080003, name = 'rose')
    emoji_1 = Emoji.precreate(202301080004, name = 'slayer')
    
    for input_value, expected_output in (
        (
            None,
            {},
        ), (
            [],
            {},
        ), (
            [emoji_1],
            {emoji_1.id: emoji_1},
        ), (
            [emoji_0, emoji_1],
            {emoji_0.id: emoji_0, emoji_1.id: emoji_1},
        ),
    ):
        output = validate_emojis(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_emojis__1():
    """
    Tests whether ``validate_emojis`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.5],
    ):
        with vampytest.assert_raises(TypeError):
            validate_emojis(input_value)
