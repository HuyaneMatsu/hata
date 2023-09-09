import vampytest

from ....core import BUILTIN_EMOJIS
from ....user import User

from ...reaction import Reaction, ReactionType

from ..reaction_mapping import ReactionMapping


NotImplementedType = type(NotImplemented)


def _iter_options__bool():
    yield ReactionMapping(), False
    yield ReactionMapping({Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None]}), True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__ReactionMapping__bool(input_value):
    """
    Tests whether ``ReactionMapping.__bool__`` works as intended.
    
    Parameters
    ----------
    input_value : ``ReactionMapping``
        The reaction mapping to get its boolean value of.
    
    Returns
    -------
    output : `bool`
    """
    output = bool(input_value)
    vampytest.assert_instance(output, bool)
    return output


def test__ReactionMapping__repr():
    """
    tests whether ``ReactionMapping.__repr__`` works as intended.
    """
    reaction_mapping = ReactionMapping({
        Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None]}
    )
    vampytest.assert_instance(repr(reaction_mapping), str)


def _iter_options__len():
    yield (
        ReactionMapping(),
        0,
    )
    
    yield (
        ReactionMapping({
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None, None],
        }),
        1,
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None, None, None],
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.burst): [None],
        }),
        2,
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None, None, None],
            Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): [None],
        }),
        2,
    )


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__ReactionMapping__len(input_value):
    """
    Tests whether ``ReactionMapping.__len__`` works as intended.
    
    Parameters
    ----------
    input_value : ``ReactionMapping``
        The reaction mapping to get its length value of.
    
    Returns
    -------
    output : `int`
    """
    output = len(input_value)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__eq():
    emoji_0 = BUILTIN_EMOJIS['x']
    emoji_1 = BUILTIN_EMOJIS['heart']
    user_0 = User.precreate(202210010037)
    
    yield (
        ReactionMapping(),
        ReactionMapping(),
        True,
    )
    yield (
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [None]}),
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [None]}),
        True,
    )
    yield (
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [None]}),
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [None, None]}),
        False,
    )
    yield (
        ReactionMapping(),
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [None]}),
        False,
    )
    yield (
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [user_0]}),
        {Reaction.from_fields(emoji_1, ReactionType.standard): [user_0]},
        True,
    )
    yield (
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [user_0]}),
        {Reaction.from_fields(emoji_1, ReactionType.standard): [user_0, None]},
        False,
    )
    yield (
        ReactionMapping(),
        {Reaction.from_fields(emoji_1, ReactionType.standard): [None]},
        False,
    )
    yield (
        ReactionMapping(),
        {Reaction.from_fields(emoji_1, ReactionType.standard): [12.6]},
        NotImplemented,
    )
    yield (
        ReactionMapping(),
        {12.6: [None]},
        NotImplemented,
    )
    yield (
        ReactionMapping(),
        {Reaction.from_fields(emoji_1, ReactionType.standard): 12.5},
        NotImplemented,
    )
    yield (
        ReactionMapping(),
        22.0,
        NotImplemented,
    )
    yield (
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [user_0]}),
        {Reaction.from_fields(emoji_1, ReactionType.standard): 12.5},
        NotImplemented,
    )
    yield (
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.standard): [None]}),
        {emoji_1: [None]},
        True,
    )
    yield (
        ReactionMapping({Reaction.from_fields(emoji_1, ReactionType.burst): [None]}),
        {emoji_1: [None]},
        False,
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_1, ReactionType.standard): [user_0],
        }),
        ReactionMapping({
            Reaction.from_fields(emoji_1, ReactionType.burst): [user_0],
        }),
        False,
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
        ReactionMapping({
            Reaction.from_fields(emoji_1, ReactionType.standard): [user_0],
        }),
        False,
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.burst): [user_0],
        }),
        ReactionMapping({
            Reaction.from_fields(emoji_1, ReactionType.burst): [user_0],
        }),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ReactionMapping__eq(value_0, value_1):
    """
    Tests whether ``ReactionMapping.__eq__`` works as intended.
    
    Parameters
    ----------
    value_0 : ``ReactionMapping``
        The reaction mapping to execute `==` with.
    value_1 : `object`
        Other value to compare to.
    
    Returns
    -------
    output : `bool`, `NotImplementedType`
    """
    output = ReactionMapping.__eq__(value_0, value_1)
    vampytest.assert_instance(output, bool, NotImplementedType)
    return output


def test__ReactionMapping__hash():
    """
    Tests whether ``ReactionMapping.__hash__`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['x']
    
    user_0 = User.precreate(202305040096)
    user_1 = User.precreate(202305040097)
    
    mapping = ReactionMapping({
        Reaction.from_fields(emoji_0, ReactionType.standard): [user_0, None, None],
        Reaction.from_fields(emoji_0, ReactionType.burst): [user_0, None, None],
        Reaction.from_fields(emoji_1, ReactionType.standard): [user_1],
    })
    
    vampytest.assert_instance(hash(mapping), int)
