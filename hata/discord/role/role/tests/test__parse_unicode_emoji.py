import vampytest

from ....core import BUILTIN_EMOJIS

from ..fields import parse_unicode_emoji


def test__parse_unicode_emoji():
    """
    Tests whether ``parse_unicode_emoji`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    for input_value, expected_output in (
        ({}, None),
        ({'unicode_emoji': None}, None),
        ({'unicode_emoji': emoji.unicode}, emoji),
    ):
        output = parse_unicode_emoji(input_value)
        vampytest.assert_eq(output, expected_output)
