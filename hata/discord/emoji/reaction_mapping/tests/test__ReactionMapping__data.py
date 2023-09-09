import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import create_partial_emoji_data
from ...reaction import Reaction, ReactionType

from ..reaction_mapping import ReactionMapping


def test__ReactionMapping__from_data():
    """
    Tests whether ``ReactionMapping.from_data`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['x']
    
    data = [
        {
            'emoji': create_partial_emoji_data(emoji_0),
            'count_details': {
                'normal': 2,
                'burst': 1,
            }
        }, {
            'emoji': create_partial_emoji_data(emoji_1),
            'count_details': {
                'normal': 0,
                'burst': 2,
            }
        }
    ]
    
    expected = ReactionMapping({
        Reaction.from_fields(emoji_0, ReactionType.standard): [None, None],
        Reaction.from_fields(emoji_0, ReactionType.burst): [None],
        Reaction.from_fields(emoji_1, ReactionType.burst): [None, None],
    })
    
    reaction_mapping = ReactionMapping.from_data(data)
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_instance(reaction_mapping.fully_loaded, bool)
    
    vampytest.assert_eq(reaction_mapping, expected)


def test__ReactionMapping__to_data():
    """
    Tests whether ``ReactionMapping.to_data`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['eye']
    
    expected_data = [
        {
            'emoji': create_partial_emoji_data(emoji_0),
            'count_details': {
                'normal': 2,
                'burst': 1,
            }
        }, {
            'emoji': create_partial_emoji_data(emoji_1),
            'count_details': {
                'normal': 0,
                'burst': 2,
            }
        }
    ]
    
    reaction_mapping = ReactionMapping({
        Reaction.from_fields(emoji_0, ReactionType.standard): [None, None],
        Reaction.from_fields(emoji_0, ReactionType.burst): [None],
        Reaction.from_fields(emoji_1, ReactionType.burst): [None, None],
    })
    
    vampytest.assert_eq(expected_data, reaction_mapping.to_data())
