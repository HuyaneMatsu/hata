import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...reaction import Reaction, ReactionType

from ..fields import validate_reaction


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202309090002, name = 'met')
    
    yield emoji_0, Reaction.from_fields(emoji_0, ReactionType.standard)
    yield emoji_1, Reaction.from_fields(emoji_1, ReactionType.standard)
    yield emoji_0.as_reaction, Reaction.from_fields(emoji_0, ReactionType.standard)
    yield emoji_1.as_reaction, Reaction.from_fields(emoji_1, ReactionType.standard)
    yield Reaction.from_fields(emoji_0, ReactionType.standard), Reaction.from_fields(emoji_0, ReactionType.standard)
    yield Reaction.from_fields(emoji_1, ReactionType.standard), Reaction.from_fields(emoji_1, ReactionType.standard)
    yield Reaction.from_fields(emoji_0, ReactionType.burst), Reaction.from_fields(emoji_0, ReactionType.burst)
    yield Reaction.from_fields(emoji_1, ReactionType.burst), Reaction.from_fields(emoji_1, ReactionType.burst)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_reaction__passing(input_value):
    """
    Tests whether ``validate_reaction`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``Reaction``
    """
    output = validate_reaction(input_value)
    # Check type as well, since `Reaction == Emoji` is supported
    vampytest.assert_instance(output, Reaction)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12)
@vampytest.call_with(None)
def test__validate_reaction__type_error(input_value):
    """
    Tests whether ``validate_reaction`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_reaction(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('x')
def test__validate_reaction__value_error(input_value):
    """
    Tests whether ``validate_reaction`` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    ValueError
    """
    validate_reaction(input_value)
