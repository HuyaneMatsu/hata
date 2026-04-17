import vampytest

from ....core import BUILTIN_EMOJIS

from ..preinstanced import ReactionType
from ..reaction import Reaction


def test__Reaction__repr():
    """
    Tests whether ``Reaction.__repr__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    reaction = Reaction(
        emoji,
        reaction_type = reaction_type,
    )
    
    vampytest.assert_instance(repr(reaction), str)


def test__Reaction__hash():
    """
    Tests whether ``Reaction.__hash__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    reaction = Reaction(
        emoji,
        reaction_type = reaction_type,
    )
    
    vampytest.assert_instance(hash(reaction), int)


def test__Reaction__hash__emoji():
    """
    Tests whether ``Reaction.__eq__`` works as intended.
    
    Case: Matching emoji hash.
    """
    emoji = BUILTIN_EMOJIS['x']
    
    vampytest.assert_eq(
        hash(emoji),
        hash(Reaction(emoji, reaction_type = ReactionType.standard)),
    )
    
    vampytest.assert_ne(
        hash(emoji),
        hash(Reaction(emoji, reaction_type = ReactionType.burst)),
    )


def test__Reaction__eq():
    """
    Tests whether ``Reaction.__eq__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    keyword_parameters = {
        'emoji': emoji,
        'reaction_type': reaction_type,
    }
    
    reaction = Reaction(**keyword_parameters)
    
    vampytest.assert_eq(reaction, reaction)
    vampytest.assert_ne(reaction, object())
    
    for field_emoji, field_value in (
        ('emoji', BUILTIN_EMOJIS['heart']),
        ('reaction_type', ReactionType.standard),
    ):
        test_reaction = Reaction(**{**keyword_parameters, field_emoji: field_value})
        vampytest.assert_ne(reaction, test_reaction)


def test__Reaction__eq__emoji():
    """
    Tests whether ``Reaction.__eq__`` works as intended.
    
    Case: Match emoji.
    """
    emoji = BUILTIN_EMOJIS['x']
    
    vampytest.assert_eq(
        emoji,
        Reaction(emoji, reaction_type = ReactionType.standard),
    )
    
    vampytest.assert_ne(
        emoji,
        Reaction(emoji, reaction_type = ReactionType.burst),
    )
