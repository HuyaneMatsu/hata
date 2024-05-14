import vampytest

from ....user import User

from ...emoji import Emoji
from ...reaction import Reaction, ReactionType
from ...reaction_mapping_line import ReactionMappingLine

from ..reaction_mapping import ReactionMapping
from ..utils import merge_update_reaction_mapping


def _iter_options():
    emoji_0 = Emoji.precreate(202210010000)
    emoji_1 = Emoji.precreate(202210010003)
    user_0 = User.precreate(202210010001)
    user_1 = User.precreate(202210010002)
    

    yield (
        None,
        None,
        0,
        None,
    )
        
    yield (
        ReactionMapping(),
        None,
        1,
        ReactionMapping(),
    )
        
    yield (
        None,
        ReactionMapping(),
        2,
        ReactionMapping(),
    )
    
    yield (
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        ),
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            }
        ),
        2,
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        ),
    )
    
    yield (
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            },
        ),
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        ),
        2,
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            },
        ),
    )
    
    yield (
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            },
        ),
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        ),
        2,
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            },
        ),
    )
    """
    
    
    yield (
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_1]),
            },
        ),
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            },
        ),
        2,
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_1]),
            },
        ),
    )
    """

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_update_reaction_mapping(reaction_mapping_new, reaction_mapping_old, input_output_same_entity):
    """
    Tests whether ``merge_update_reaction_mapping`` works as intended.
    
    Parameters
    ----------
    reaction_mapping_old : `None | ReactionMapping`
        Old reaction mapping.
    reaction_mapping_new : `None | ReactionMapping`
        New reaction mapping.
    input_output_same_entity : `int`
        Whether the output should be either nothing / `reaction_mapping_new` / `reaction_mapping_old`.
    
    Returns
    -------
    output : `None | ReactionMapping`
    """
    if (reaction_mapping_old is not None):
        reaction_mapping_old = reaction_mapping_old.copy()
    
    if (reaction_mapping_new is not None):
        reaction_mapping_new = reaction_mapping_new.copy()
    
    output = merge_update_reaction_mapping(reaction_mapping_new, reaction_mapping_old)
    
    if input_output_same_entity == 1:
        vampytest.assert_is(output, reaction_mapping_new)
    elif input_output_same_entity == 2:
        vampytest.assert_is(output, reaction_mapping_old)
    
    return output
