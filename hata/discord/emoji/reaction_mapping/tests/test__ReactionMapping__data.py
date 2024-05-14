import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import create_partial_emoji_data
from ...reaction import Reaction, ReactionType
from ...reaction_mapping_line import ReactionMappingLine

from ..reaction_mapping import ReactionMapping

from .test__ReactionMapping__constructor import _assert_fields_set


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
    
    expected = ReactionMapping(
        lines = {
            Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
            Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1),
            Reaction.from_fields(emoji_1, ReactionType.burst): ReactionMappingLine(count = 2),
        }
    )
    
    reaction_mapping = ReactionMapping.from_data(data)
    _assert_fields_set(reaction_mapping)
    
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
    
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
            Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1),
            Reaction.from_fields(emoji_1, ReactionType.burst): ReactionMappingLine(count = 2),
        }
    )
    
    vampytest.assert_eq(expected_data, reaction_mapping.to_data())
