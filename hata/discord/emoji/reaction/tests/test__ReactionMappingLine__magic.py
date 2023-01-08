import vampytest

from ....user import User

from ..reaction_mapping_line import ReactionMappingLine


def test__ReactionMappingLine__len():
    """
    Tests whether ``ReactionMappingLine.__len__`` works as intended.
    """
    user = User.precreate(202210010012)
    users = [user]
    unknown = 6
    
    reaction_mapping_line = ReactionMappingLine(users, unknown = unknown)
    
    length = len(reaction_mapping_line)
    
    vampytest.assert_instance(length, int)
    vampytest.assert_eq(length, len(users) + unknown)


def test__ReactionMappingLine__repr():
    """
    Tests whether ``ReactionMappingLine.__repr__`` works as intended.
    """
    user = User.precreate(202210010013)
    users = [user]
    unknown = 6
    
    reaction_mapping_line = ReactionMappingLine(users, unknown = unknown)
    
    vampytest.assert_instance(repr(reaction_mapping_line), str)


def test__ReactionMappingLine__eq():
    """
    Tests whether ``ReactionMappingLine.__eq__`` works as intended.
    """
    user_1 = User.precreate(202210010025)
    user_2 = User.precreate(202210010026)
    
    for input_1, input_2, expected_output in (
        (ReactionMappingLine(), ReactionMappingLine(), True),
        (ReactionMappingLine(unknown = 2), ReactionMappingLine(), False),
        (ReactionMappingLine(unknown = 2), ReactionMappingLine(unknown = 2), True),
        (ReactionMappingLine(unknown = 2), ReactionMappingLine(unknown = 2), True),
        (ReactionMappingLine([user_1]), ReactionMappingLine([user_1]), True),
        (ReactionMappingLine([user_1]), ReactionMappingLine([user_1, user_2]), False),
        (ReactionMappingLine([user_1]), ReactionMappingLine([user_1, None]), False),
        (ReactionMappingLine([user_1, None]), ReactionMappingLine([user_1, None]), True),
        (ReactionMappingLine([user_1, None]), 12, NotImplemented),
        (ReactionMappingLine(), [], True),
        (ReactionMappingLine(), [user_1], False),
        (ReactionMappingLine(), [12], NotImplemented),
        (ReactionMappingLine([None]), [None], True),
        (ReactionMappingLine([user_1]), [user_1], True),
        (ReactionMappingLine([user_1, None]), [user_1, None], True),
        (ReactionMappingLine([user_1, None]), [user_1, None, None], False),
    ):
        output = ReactionMappingLine.__eq__(input_1, input_2)
        vampytest.assert_eq(output, expected_output)


def test__ReactionMappingLine__bool():
    """
    Tests whether ``ReactionMappingLine.__bool__`` works as intended.
    """
    user_1 = User.precreate(202210010027)
    
    for reaction_mapping_line, expected_output in (
        (ReactionMappingLine(), False),
        (ReactionMappingLine([None]), True),
        (ReactionMappingLine([user_1]), True),
    ):
        vampytest.assert_eq(bool(reaction_mapping_line), expected_output)
