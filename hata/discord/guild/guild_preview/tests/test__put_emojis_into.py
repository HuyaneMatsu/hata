import vampytest

from ....emoji import Emoji

from ..fields import put_emojis_into


def test__put_emojis_into():
    """
    Tests whether ``put_emojis_into`` works as intended.
    """
    emoji_0 = Emoji.precreate(202301080002, name = 'rose')
    
    for input_value, expected_output in (
        (
            {},
            {'emojis': []},
        ), (
            {emoji_0.id: emoji_0},
            {'emojis': [emoji_0.to_data(defaults = True, include_internals = True)]},
        ),
    ):
        output = put_emojis_into(input_value, {}, True)
        vampytest.assert_eq(output, expected_output)
