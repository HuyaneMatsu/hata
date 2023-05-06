import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import ReactionMapping

from ..fields import put_reactions_into


def test__put_reactions_into():
    """
    Tests whether ``put_reactions_into`` works as intended.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['x']
    
    reaction_mapping = ReactionMapping({
        emoji_1: [None, None],
        emoji_2: [None]
    })
    
    for input_value, defaults, expected_output in (
        (None, True, {'reactions': []}),
        (None, False, {}),
        (reaction_mapping, False, {'reactions': reaction_mapping.to_data()}),
    ):
        output = put_reactions_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
