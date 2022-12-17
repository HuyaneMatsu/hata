import vampytest

from ....core import BUILTIN_EMOJIS

from ..fields import put_unicode_emoji_into


def test__put_unicode_emoji_into():
    """
    Tests whether ``put_unicode_emoji_into`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'unicode_emoji': None}),
        (emoji, False, {'unicode_emoji': emoji.unicode}),
    ):
        output = put_unicode_emoji_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
