import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import create_partial_emoji_data

from ..reaction_mapping import ReactionMapping


def test__ReactionMapping__from_data():
    """
    Tests whether ``ReactionMapping.from_data`` works as intended.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['x']
    
    data = [
        {
            'emoji': create_partial_emoji_data(emoji_1),
            'count': 2,
            'me': False,
        }, {
            'emoji': create_partial_emoji_data(emoji_2),
            'me': False,
        }
    ]
    
    expected = ReactionMapping({
        emoji_1: [None, None],
        emoji_2: [None]
    })
    
    reaction_mapping = ReactionMapping.from_data(data)
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_instance(reaction_mapping.fully_loaded, bool)
    
    vampytest.assert_eq(reaction_mapping, expected)


def test__ReactionMapping__to_data():
    """
    Tests whether ``ReactionMapping.to_data`` works as intended.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['eye']
    
    expected_data = [
        {
            'emoji': create_partial_emoji_data(emoji_1),
            'count': 2,
            'me': False,
        }, {
            'emoji': create_partial_emoji_data(emoji_2),
            'count': 1,
            'me': False,
        }
    ]
    
    reaction_mapping = ReactionMapping({
        emoji_1: [None, None],
        emoji_2: [None],
    })
    
    vampytest.assert_eq(expected_data, reaction_mapping.to_data())
