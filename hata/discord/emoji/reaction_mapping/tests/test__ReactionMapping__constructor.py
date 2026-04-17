import vampytest

from ....user import User

from ...emoji import Emoji
from ...reaction import Reaction, ReactionType
from ...reaction_mapping_line import ReactionMappingLine

from ..reaction_mapping import ReactionMapping


def _assert_fields_set(reaction_mapping):
    """
    Asserts whether every fields are set of the given reaction mapping.
    
    Parameters
    ----------
    reaction_mapping : ``ReactionMapping``
    """
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_instance(reaction_mapping.lines, dict, nullable = True)


def test__ReactionMapping__new__no_fields():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: No fields given.
    """
    reaction_mapping = ReactionMapping()
    _assert_fields_set(reaction_mapping)
    
    vampytest.assert_eq(len(reaction_mapping), 0)


def test__ReactionMapping__new__all_fields():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: All fields given.
    """
    reaction_0 = Reaction.from_fields(Emoji.precreate(202210010028), ReactionType.standard)
    user_0 = User.precreate(202210010029)
    line = ReactionMappingLine(count = 4, users = [user_0])
    
    reaction_mapping = ReactionMapping(lines = {reaction_0: line})
    _assert_fields_set(reaction_mapping)
    
    vampytest.assert_eq(
        reaction_mapping.lines,
        {reaction_0: line},
    )
