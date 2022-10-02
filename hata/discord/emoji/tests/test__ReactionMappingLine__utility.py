import vampytest

from ...client import Client
from ...user import User

from ..reaction_mapping_line import ReactionMappingLine


def test__ReactionMappingLine__update():
    """
    Tests whether ``ReactionMappingLine.update`` works as intended.
    """
    user_1 = User.precreate(202210010015)
    user_2 = User.precreate(202210010016)
    user_3 = User.precreate(202210010017)
    
    reaction_mapping_line = ReactionMappingLine([user_1, user_2], unknown = 2)
    reaction_mapping_line.update([user_2, user_3])
    
    vampytest.assert_eq(len(reaction_mapping_line), 4)
    vampytest.assert_in(user_1, reaction_mapping_line)
    vampytest.assert_in(user_2, reaction_mapping_line)
    vampytest.assert_in(user_3, reaction_mapping_line)


def test__ReactionMappingLine__copy():
    """
    Tests whether ``ReactionMappingLine.update`` works as intended.
    """
    user_1 = User.precreate(202210010018)
    user_2 = User.precreate(202210010019)
    
    reaction_mapping_line = ReactionMappingLine([user_1, user_2], unknown = 2)
    copy = reaction_mapping_line.copy()
    
    vampytest.assert_instance(copy, ReactionMappingLine)
    vampytest.assert_eq(reaction_mapping_line, copy)
    vampytest.assert_is_not(reaction_mapping_line, copy)


def test__ReactionMappingLine__clear():
    """
    Tests whether ``ReactionMappingLine.clear`` works as intended.
    """
    client = Client('token_202210010000')
    
    try:
        user_1 = User.precreate(202210010020)
        user_2 = User.precreate(202210010021)
        users = [client, user_1, user_2]
        unknown = 4
        
        reaction_mapping_line = ReactionMappingLine(users, unknown = unknown)
        
        reaction_mapping_line.clear()
        
        vampytest.assert_eq(len(reaction_mapping_line), unknown + len(users))
        vampytest.assert_in(client, reaction_mapping_line)
        vampytest.assert_not_in(user_1, reaction_mapping_line)
        vampytest.assert_not_in(user_2, reaction_mapping_line)
    
    finally:
        client._delete()
        client = None


def test__ReactionMappingLine__filter_after():
    """
    Tests whether ``ReactionMappingLine.filter_after`` works as intended.
    """
    user_1 = User.precreate(202210010022)
    user_2 = User.precreate(202210010023)
    user_3 = User.precreate(202210010024)
    reaction_mapping_line = ReactionMappingLine([user_1, user_2, user_3])
    
    users = reaction_mapping_line.filter_after(1, user_1.id)
    
    vampytest.assert_instance(users, list)
    vampytest.assert_eq(users, [user_2])


def test__ReactionMappingLine__remove():
    """
    Tests whether ``ReactionMappingLine.remove`` works as intended.``
    """
    user_1 = User.precreate(202210010035)
    user_2 = User.precreate(202210010036)
    
    for initial_value, expected_value, expected_output, value_to_remove in (
        (ReactionMappingLine([user_1]), ReactionMappingLine(), True, user_1),
        (ReactionMappingLine([user_1]), ReactionMappingLine([user_1]), False, user_2),
        (ReactionMappingLine([None]), ReactionMappingLine(), True, user_1),
        (ReactionMappingLine(), ReactionMappingLine(), False, user_1),
    ):
        output = initial_value.remove(value_to_remove)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)
        vampytest.assert_eq(initial_value, expected_value)
