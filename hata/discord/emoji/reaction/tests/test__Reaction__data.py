import vampytest

from ....core import BUILTIN_EMOJIS

from ..preinstanced import ReactionType
from ..reaction import Reaction

from .test__Reaction__constructor import _assert_fields_set


def test__Reaction__from_data():
    """
    Tests whether ``Reaction.from_data`` works as intended.
    
    Case: Default.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    data = {
        'emoji': {'name': emoji.unicode},
        'burst': (reaction_type is ReactionType.burst),
    }
    
    reaction = Reaction.from_data(data)
    _assert_fields_set(reaction)
    
    vampytest.assert_eq(reaction.type, reaction_type)
    vampytest.assert_eq(reaction.emoji, emoji)


def test__Reaction__to_data():
    """
    Tests whether ``Reaction.to_data`` works as intended.
    
    Case: include defaults.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    expected_output = {
        'emoji': {'name': emoji.unicode},
        'burst': (reaction_type is ReactionType.burst),
    }
    
    reaction = Reaction(
        emoji,
        reaction_type = reaction_type,
    )
    
    vampytest.assert_eq(reaction.to_data(defaults = True), expected_output)
