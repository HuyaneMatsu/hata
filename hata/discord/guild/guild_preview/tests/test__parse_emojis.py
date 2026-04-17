import vampytest

from ....emoji import Emoji

from ..fields import parse_emojis


def test__parse_emojis():
    """
    Tests whether ``parse_emojis`` works as intended.
    """
    emoji_0 = Emoji.precreate(202301080000, name = 'rose')
    emoji_1 = Emoji.precreate(202301080001, name = 'slayer')
    
    for input_data, input_entities, expected_output in (
        (
            {},
            {},
            {},
        ), (
            {'emojis': None},
            {},
            {},
        ), (
            {'emojis': []},
            {},
            {},
        ), (
            {'emojis': [emoji_0.to_data(defaults = True, include_internals = True)]},
            {},
            {emoji_0.id: emoji_0},
        ), (
            {'emojis': [emoji_1.to_data(defaults = True, include_internals = True)]},
            {emoji_0.id: emoji_0},
            {emoji_1.id: emoji_1},
        ),
    ):
        output = parse_emojis(input_data, input_entities, 0)
        vampytest.assert_eq(output, expected_output)
