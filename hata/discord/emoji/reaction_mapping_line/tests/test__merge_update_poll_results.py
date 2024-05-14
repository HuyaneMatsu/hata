import vampytest

from ....core import BUILTIN_EMOJIS
from ....user import User

from ...reaction import Reaction

from ..reaction_mapping_line import ReactionMappingLine
from ..utils import merge_update_reaction_mapping_lines


def _iter_options():
    user_0 = User.precreate(202405110043)
    user_1 = User.precreate(202405110044)
    
    reaction_0 = Reaction(BUILTIN_EMOJIS['x'])
    reaction_1 =  Reaction(BUILTIN_EMOJIS['heart'])
    reaction_2 = Reaction(BUILTIN_EMOJIS['flan'])
    
    item_0 = reaction_0, ReactionMappingLine(count = 12, users = [user_0, user_1])
    item_1 = reaction_1, ReactionMappingLine(count = 2)
    item_2 = reaction_2, ReactionMappingLine(count = 4)
    item_3 = reaction_2, ReactionMappingLine(count = 5)
    item_4 = reaction_0, ReactionMappingLine(count = 12)
    item_5 = reaction_0, ReactionMappingLine(count = 11)
    
    # No new items
    yield (
        None,
        [item_0, item_1],
        None,
    )
    
    # No old items
    yield (
        [item_1, item_2],
        None,
        {item_1, item_2},
    )
    
    
    # Removed item
    yield (
        [item_0],
        [item_0, item_1],
        {item_0},
    )

    # added item
    yield (
        [item_0, item_2],
        [item_0],
        {item_0, item_2},
    )

    # merged item (count only)
    yield (
        [item_3],
        [item_2],
        {item_3},
    )

    # merged item (user keep)
    yield (
        [item_4],
        [item_0],
        {item_0},
    )

    # merged item (user clean)
    yield (
        [item_5],
        [item_0],
        {item_5},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_update_reaction_mapping_lines(new_lines, old_lines):
    """
    Tests whether ``merge_update_reaction_mapping_lines`` works as intended.
    
    Parameters
    ----------
    new_lines : `None | list<(Reaction, ReactionMappingLine)>`
        New lines.
    old_lines : `None | list<(Reaction, ReactionMappingLine)>`
        Old lines.
    
    Returns
    -------
    lines : `None | set<(Reaction, ReactionMappingLine)>`
    """
    if (new_lines is not None):
        new_lines = {reaction: line.copy() for reaction, line in new_lines}
    
    if (old_lines is not None):
        old_lines = {reaction: line.copy() for reaction, line in old_lines}
    
    output = merge_update_reaction_mapping_lines(new_lines, old_lines)
    vampytest.assert_instance(output, dict, nullable = True)
    if output is None:
        return None
    
    return {*output.items()}
