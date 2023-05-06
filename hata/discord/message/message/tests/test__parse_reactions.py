import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import ReactionMapping
from ....user import User

from ..fields import parse_reactions


def test__parse_reactions__0():
    """
    Tests whether ``parse_reactions`` works as intended.
    
    Case: Nothing.
    """
    for input_data in (
        {},
        {'reactions': None},
        {'reactions': []},
    ):
        output = parse_reactions(input_data)
        vampytest.assert_is(output, None)


def test__parse_reactions__1():
    """
    tests whether ``parse_reactions` works as intended.
    
    Case: Old reactions, no new.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['x']
    
    old_reactions = ReactionMapping({
        emoji_1: [None, None],
        emoji_2: [None]
    })
    
    input_data = {}
    
    output = parse_reactions(input_data, old_reactions)
    vampytest.assert_is_not(output, None)
    vampytest.assert_is(output, old_reactions)
    vampytest.assert_instance(output, ReactionMapping)


def test__parse_reactions__2():
    """
    tests whether ``parse_reactions` works as intended.
    
    Case: New reactions, no old.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['x']
    
    reaction_mapping = ReactionMapping({
        emoji_1: [None, None],
        emoji_2: [None]
    })
    
    input_data = {
        'reactions': reaction_mapping.to_data()
    }
    
    output = parse_reactions(input_data, None)
    vampytest.assert_is_not(output, None)
    vampytest.assert_instance(output, ReactionMapping)
    vampytest.assert_eq(output, reaction_mapping)


def test__parse_reactions__3():
    """
    tests whether ``parse_reactions` works as intended.
    
    Case: New reactions with old.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['x']
    
    user_id_0 = 202305010019
    user_id_1 = 202305010020
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    old_reaction_mapping = ReactionMapping({
        emoji_1: [user_0, user_1],
        emoji_2: [user_1]
    })
    
    reaction_mapping_0 = ReactionMapping({
        emoji_1: [None, None],
        emoji_2: [None, None]
    })
    
    expected_output = ReactionMapping({
        emoji_1: [user_0, user_1],
        emoji_2: [None, None]
    })
    
    input_data = {
        'reactions': reaction_mapping_0.to_data()
    }
    
    output = parse_reactions(input_data, old_reaction_mapping)
    vampytest.assert_is_not(output, None)
    vampytest.assert_instance(output, ReactionMapping)
    vampytest.assert_is(output, old_reaction_mapping)
    vampytest.assert_eq(output, expected_output)
