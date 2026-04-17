import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...reaction import Reaction, ReactionType
from ...reaction_mapping_line import ReactionMappingLine

from ..fields import validate_lines


def _iter_options__passing():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = Emoji.precreate(202309090002, name = 'met')
    
    reaction_0 = Reaction.from_fields(emoji_0, ReactionType.standard)
    reaction_1 =  Reaction.from_fields(emoji_1, ReactionType.standard)
    
    line_0 = ReactionMappingLine(count = 3)
    line_1 = ReactionMappingLine(count = 4)
    
    yield None, None
    
    yield [], None
    yield {}, None
    
    yield {reaction_0: line_0, reaction_1: line_1}, {reaction_0: line_0, reaction_1: line_1}
    yield [(reaction_0, line_0), (reaction_1, line_1)], {reaction_0: line_0, reaction_1: line_1}
    
    yield {emoji_0: line_0, emoji_1: line_1}, {reaction_0: line_0, reaction_1: line_1}
    yield [(emoji_0, line_0), (emoji_1, line_1)], {reaction_0: line_0, reaction_1: line_1}


def _iter_options__type_error():
    emoji_0 = BUILTIN_EMOJIS['heart']
    line_0 = ReactionMappingLine(count = 3)
    
    yield object()
    
    yield [12]
    yield [(12, line_0)]
    yield [(emoji_0, 12)]
    
    yield {12: line_0}
    yield {emoji_0: 12}
    
    yield [(emoji_0, line_0, object())]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_lines(input_value):
    """
    Tests whether ``validate_lines`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<Reaction, ReactionMappingLine>`
    
    Raises
    ------
    TypeError
    """
    return validate_lines(input_value)
