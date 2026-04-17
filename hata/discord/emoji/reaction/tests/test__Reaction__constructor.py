import vampytest

from ....core import BUILTIN_EMOJIS

from ...emoji import Emoji

from ..preinstanced import ReactionType
from ..reaction import Reaction


def _assert_fields_set(reaction):
    """
    Asserts whether every attributes of the given are set.
    
    Parameters
    ----------
    reaction : ``Reaction``
        The audit log reaction to check.
    """
    vampytest.assert_instance(reaction, Reaction)
    vampytest.assert_instance(reaction.emoji, Emoji)
    vampytest.assert_instance(reaction.type, ReactionType)


def test__Reaction__new__no_fields():
    """
    Tests whether ``Reaction.__new__`` works as intended.
    
    Case: No parameters given.
    """
    emoji = BUILTIN_EMOJIS['x']
    
    reaction = Reaction(emoji)
    _assert_fields_set(reaction)
    
    vampytest.assert_is(reaction.emoji, emoji)
    vampytest.assert_is(reaction.type, ReactionType.standard)


def test__Reaction__new__all_fields():
    """
    Tests whether ``Reaction.__new__`` works as intended.
    
    Case: All parameters given.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    reaction = Reaction(
        emoji,
        reaction_type = reaction_type,
    )
    _assert_fields_set(reaction)
    
    vampytest.assert_is(reaction.emoji, emoji)
    vampytest.assert_is(reaction.type, reaction_type)



def test__Reaction__new__all_fields():
    """
    Tests whether ``Reaction.__new__`` works as intended.
    
    Case: All parameters given.
    """
    emoji = BUILTIN_EMOJIS['x']
    reaction_type = ReactionType.burst
    
    reaction = Reaction.from_fields(
        emoji,
        reaction_type,
    )
    _assert_fields_set(reaction)
    
    vampytest.assert_is(reaction.emoji, emoji)
    vampytest.assert_is(reaction.type, reaction_type)
