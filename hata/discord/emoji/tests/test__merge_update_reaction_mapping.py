import vampytest

from ...user import User

from ..emoji import Emoji
from ..reaction_mapping import ReactionMapping
from ..utils import merge_update_reaction_mapping


def test__merge_update_reaction_mapping__0():
    """
    Tests whether ``merge_update_reaction_mapping`` works as intended.
    """
    emoji_0 = Emoji.precreate(202210010000)
    emoji_1 = Emoji.precreate(202210010003)
    user_0 = User.precreate(202210010001)
    user_1 = User.precreate(202210010002)
    
    for expected_output, input_value_old, input_value_new, input_output_same_entity in (
        (
            None,
            None,
            None,
            0,
        ),
        (
            ReactionMapping(),
            None,
            ReactionMapping(),
            2,
        ),
        (
            ReactionMapping(),
            ReactionMapping(),
            None,
            1,
        ), (
            ReactionMapping({emoji_0: [user_0]}),
            ReactionMapping({emoji_0: [user_0], emoji_1: [user_1]}),
            ReactionMapping({emoji_0: [user_0]}),
            1,
        ), (
            ReactionMapping({emoji_0: [user_0], emoji_1: [user_1]}),
            ReactionMapping({emoji_0: [user_0]}),
            ReactionMapping({emoji_0: [user_0], emoji_1: [user_1]}),
            1,
        ), (
            ReactionMapping({emoji_0: [user_1]}),
            ReactionMapping({emoji_0: [user_0]}),
            ReactionMapping({emoji_0: [user_1]}),
            1,
        ), (
            ReactionMapping({emoji_0: [user_1, None]}),
            ReactionMapping({emoji_0: [user_1]}),
            ReactionMapping({emoji_0: [user_1, None]}),
            1,
        )
    ):
        output = merge_update_reaction_mapping(input_value_old, input_value_new)
        
        vampytest.assert_eq(output, expected_output)
        
        if input_output_same_entity == 1:
            vampytest.assert_is(output, input_value_old)
        elif input_output_same_entity == 2:
            vampytest.assert_is(output, input_value_new)


def test__merge_update_reaction_mapping__1():
    """
    Tests whether ``merge_update_reaction_mapping`` modifies `.fully_loaded` as intended.
    """
    emoji_0 = Emoji.precreate(202210010004)
    user_1 = User.precreate(202210010005)
    
    for input_value_old, input_value_new, expected_fully_loaded in (
        (
            ReactionMapping({emoji_0: [user_1]}),
            ReactionMapping({emoji_0: [user_1, None]}),
            False,
        ), (
            ReactionMapping({emoji_0: [user_1, None]}),
            ReactionMapping({emoji_0: [user_1]}),
            True,
        )
    ):
        output = merge_update_reaction_mapping(input_value_old, input_value_new)
        
        vampytest.assert_eq(output.fully_loaded, expected_fully_loaded)
