import vampytest

from ....user import User

from ..reaction_mapping_line import ReactionMappingLine


def test__ReactionMappingLine__new__0():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: No parameter.
    """
    reaction_mapping_line = ReactionMappingLine()
    
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_eq(len(reaction_mapping_line), 0)
    vampytest.assert_eq(reaction_mapping_line.unknown, 0)


def test__ReactionMappingLine__new__1():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: users.
    """
    user_0 = User.precreate(202210010006)
    user_1 = User.precreate(202210010007)
    users = [user_0, user_1]
    
    reaction_mapping_line = ReactionMappingLine(users)
    
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_eq(len(reaction_mapping_line), len(users))
    vampytest.assert_in(user_0, reaction_mapping_line)
    vampytest.assert_in(user_1, reaction_mapping_line)
    vampytest.assert_eq(reaction_mapping_line.unknown, users.count(None))


def test__ReactionMappingLine__new__2():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: users with unknown.
    """
    user_0 = User.precreate(202210010008)
    user_1 = User.precreate(202210010009)
    users = [user_0, user_1, None]
    
    reaction_mapping_line = ReactionMappingLine(users)
    
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_eq(len(reaction_mapping_line), len(users))
    vampytest.assert_in(user_0, reaction_mapping_line)
    vampytest.assert_in(user_1, reaction_mapping_line)
    vampytest.assert_eq(reaction_mapping_line.unknown, users.count(None))


def test__ReactionMappingLine__new__3():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: Unknown.
    """
    unknown = 6
    
    reaction_mapping_line = ReactionMappingLine(unknown = unknown)
    
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_eq(len(reaction_mapping_line), unknown)
    vampytest.assert_eq(reaction_mapping_line.unknown, unknown)


def test__ReactionMappingLine__new__4():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: users with unknown.
    """
    user_0 = User.precreate(202210010010)
    user_1 = User.precreate(202210010011)
    users = [user_0, user_1, None]
    
    unknown = 6
    
    reaction_mapping_line = ReactionMappingLine(users, unknown = unknown)
    
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_eq(len(reaction_mapping_line), unknown + len(users))
    vampytest.assert_in(user_0, reaction_mapping_line)
    vampytest.assert_in(user_1, reaction_mapping_line)
    vampytest.assert_eq(reaction_mapping_line.unknown, unknown + users.count(None))


def test__ReactionMappingLine__new__5():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: `TypeError` from `initialize_with` parameter.
    """
    for input_value in (12.6, [12.6]):
        with vampytest.assert_raises(TypeError):
            ReactionMappingLine(input_value)


def test__ReactionMappingLine__new__6():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: `TypeError` from `unknown` parameter.
    """
    for input_value in (12.6, ):
        with vampytest.assert_raises(TypeError):
            ReactionMappingLine(unknown = input_value)


def test__ReactionMappingLine__new__7():
    """
    Tests whether ``ReactionMappingLine.__new__`` works as intended.
    
    Case: `ValueError` from `unknown` parameter.
    """
    for input_value in (-2, ):
        with vampytest.assert_raises(ValueError):
            ReactionMappingLine(unknown = input_value)


def test__ReactionMappingLine__create_empty():
    """
    Tests whether ``ReactionMapping._create_empty` works as intended.
    """
    unknown = 4
    reaction_mapping_line = ReactionMappingLine._create_empty(unknown)
    
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_eq(reaction_mapping_line.unknown, unknown)


def test__reactionMappingLine__create_full():
    """
    Tests whether ``ReactionMappingLine._create_full` works as intended.
    """
    user = User.precreate(202210010014)
    users = [user]
    
    reaction_mapping_line = ReactionMappingLine._create_full(users)
    
    vampytest.assert_instance(reaction_mapping_line, ReactionMappingLine)
    vampytest.assert_eq(len(reaction_mapping_line), len(users))
    vampytest.assert_in(user, reaction_mapping_line)
