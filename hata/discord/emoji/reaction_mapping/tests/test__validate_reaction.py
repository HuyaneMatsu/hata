import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...reaction import Reaction, ReactionType

from ..fields import validate_reaction


def _iter_options__passing():
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


def _iter_options__type_error():
    yield None
    yield 12


def _iter_options__value_error():
    yield 'x'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_reaction(input_value):
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
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_reaction(input_value)
    # Check type as well, since `Reaction == Emoji` is supported
    vampytest.assert_instance(output, Reaction)
    return output
