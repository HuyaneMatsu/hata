import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import ReactionMapping
from ....user import User

from ..fields import validate_reactions


def test__validate_reactions__0():
    """
    Tests whether ``validate_reactions`` works as intended.
    
    Case: passing.
    """
    reactions = ReactionMapping()
    
    for input_value, expected_output in (
        (None, None),
        (reactions, reactions),
    ):
        output = validate_reactions(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_reactions__1():
    """
    Tests whether ``validate_reactions`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_reactions(input_value)


def test__validate_reactions__2():
    """
    Tests whether ``validate_reactions`` works as intended.
    
    Case: Successful conversion.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['x']
    
    user_id_0 = 202305010021
    user_id_1 = 202305010022
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    input_value = {
        emoji_1: [user_0, user_1],
        emoji_2: [user_1]
    }
    expected_output = ReactionMapping(input_value)
    
    output = validate_reactions(input_value)
    vampytest.assert_eq(output, expected_output)
