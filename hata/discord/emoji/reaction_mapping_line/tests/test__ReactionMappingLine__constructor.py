import vampytest

from ....user import User

from ..reaction_mapping_line import ReactionMappingLine


def _assert_fields_set(reaction_mapping_line):
    """
    Asserts whether every attributes are set of the given poll result.
    
    Parameters
    ----------
    reaction_mapping_line : ``ReactionMappingLine``
        The poll result to check.
    """
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_instance(reaction_mapping_line.count, int)
    vampytest.assert_instance(reaction_mapping_line.users, set, nullable = True)


def test__ReactionMappingLine__new__no_fields():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: No fields given.
    """
    reaction_mapping_line = ReactionMappingLine()
    _assert_fields_set(reaction_mapping_line)


def test__ReactionMappingLine__new__all_fields():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: all fields given.
    """
    count = 3
    users = [
        User.precreate(202405110002),
        User.precreate(202405110003),
    ]
    
    reaction_mapping_line = ReactionMappingLine(
        count = count,
        users = users,
    )
    
    _assert_fields_set(reaction_mapping_line)
    vampytest.assert_eq(reaction_mapping_line.count, count)
    vampytest.assert_eq(reaction_mapping_line.users, set(users))


def test__ReactionMappingLine__create_empty():
    """
    Tests whether ``ReactionMappingLine._create_empty`` works as intended.
    """
    reaction_mapping_line = ReactionMappingLine._create_empty()
    _assert_fields_set(reaction_mapping_line)
