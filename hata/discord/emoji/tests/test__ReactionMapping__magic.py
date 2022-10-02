import vampytest

from ...core import BUILTIN_EMOJIS
from ...user import User

from ..emoji import Emoji
from ..reaction_mapping import ReactionMapping


def test__ReactionMapping__bool():
    """
    tests whether ``ReactionMapping.__bool__`` works as intended.
    """
    for reaction_mapping, expected_output in (
        (ReactionMapping(), False),
        (ReactionMapping({BUILTIN_EMOJIS['heart']: [None]}), True),
    ):
        vampytest.assert_eq(bool(reaction_mapping), expected_output)


def test__ReactionMapping__repr():
    """
    tests whether ``ReactionMapping.__repr__`` works as intended.
    """
    reaction_mapping = ReactionMapping({BUILTIN_EMOJIS['heart']: [None]})
    vampytest.assert_instance(repr(reaction_mapping), str)


def test__ReactionMapping__len():
    """
    Tests whether ``ReactionMapping.__len__`` works as intended.
    """
    reaction_mapping = ReactionMapping({BUILTIN_EMOJIS['heart']: [None, None]})
    
    length = len(reaction_mapping)
    
    vampytest.assert_instance(length, int)
    vampytest.assert_eq(length, 1)


def test__ReactionMapping__eq():
    """
    Tests whether ``ReactionMapping.__eq__`` works as intended.
    """
    emoji_1 = BUILTIN_EMOJIS['heart']
    user_1 = User.precreate(202210010037)
        
    for value_1, value_2, expected_output in (
        (ReactionMapping(), ReactionMapping(), True),
        (ReactionMapping({emoji_1: [None]}), ReactionMapping({emoji_1: [None]}), True),
        (ReactionMapping({emoji_1: [None]}), ReactionMapping({emoji_1: [None, None]}), False),
        (ReactionMapping(), ReactionMapping({emoji_1: [None]}), False),
        (ReactionMapping({emoji_1: [user_1]}), {emoji_1: [user_1]}, True),
        (ReactionMapping({emoji_1: [user_1]}), {emoji_1: [user_1, None]}, False),
        (ReactionMapping(), {emoji_1: [None]}, False),
        (ReactionMapping(), {emoji_1: [12.6]}, NotImplemented),
        (ReactionMapping(), {12.6: [None]}, NotImplemented),
        (ReactionMapping(), {emoji_1: 12.5}, NotImplemented),
        (ReactionMapping(), 22.0, NotImplemented),
        (ReactionMapping({emoji_1: [user_1]}), {emoji_1: 12.5}, NotImplemented),
    ):
        output = ReactionMapping.__eq__(value_1, value_2)
        
        vampytest.assert_eq(output, expected_output)
