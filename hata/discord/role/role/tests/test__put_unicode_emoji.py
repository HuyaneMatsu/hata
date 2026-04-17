import vampytest

from ....core import BUILTIN_EMOJIS

from ..fields import put_unicode_emoji


def test__put_unicode_emoji():
    """
    Tests whether ``put_unicode_emoji`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'unicode_emoji': None}),
        (emoji, False, {'unicode_emoji': emoji.unicode}),
    ):
        output = put_unicode_emoji(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
