import vampytest

from ....core import BUILTIN_EMOJIS

from ..preinstanced import ReactionType
from ..reaction import Reaction

from .test__Reaction__constructor import _assert_fields_set


def test__Reaction__copy():
    """
    Tests whether ``Reaction.copy`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    reaction = Reaction(
        emoji,
        reaction_type = reaction_type,
    )
    
    copy = reaction.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, reaction)
    vampytest.assert_not_is(copy, reaction)


def test__Reaction__copy_with__0():
    """
    Tests whether ``Reaction.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    reaction = Reaction(
        emoji,
        reaction_type = reaction_type,
    )
    
    copy = reaction.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, reaction)
    vampytest.assert_not_is(copy, reaction)


def test__Reaction__copy_with__1():
    """
    Tests whether ``Reaction.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_emoji = BUILTIN_EMOJIS['x']
    old_reaction_type = ReactionType.burst
    
    new_emoji = BUILTIN_EMOJIS['heart']
    new_reaction_type = ReactionType.standard
    
    
    reaction = Reaction(
        emoji = old_emoji,
        reaction_type = old_reaction_type,
    )
    
    copy = reaction.copy_with(
        emoji = new_emoji,
        reaction_type = new_reaction_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_not_is(copy, reaction)
    
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_is(copy.type, new_reaction_type)
