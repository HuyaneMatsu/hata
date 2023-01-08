import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import Emoji

from ..utils import parse_reaction


def test__parse_reaction__0():
    """
    Tests whether ``parse_reaction`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['x']
    emoji_1 = Emoji.precreate(202301010090, name = 'replica', animated = True)
        
    for input_value, expected_output in (
        (emoji_0.as_reaction, emoji_0),
        (emoji_1.as_reaction, emoji_1),
    ):
        output = parse_reaction(input_value)
        vampytest.assert_eq(output, expected_output)
