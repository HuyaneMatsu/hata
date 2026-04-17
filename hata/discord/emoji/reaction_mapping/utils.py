__all__ = ('merge_update_reaction_mapping',)

from ..reaction_mapping_line import merge_update_reaction_mapping_lines


def merge_update_reaction_mapping(new_reactions, old_reactions):
    """
    Merges the two reaction mapping, so values wont be overwritten if not required.
    
    Parameters
    ----------
    new_reactions : `None`, ``ReactionMapping``
        The new reactions on a message.
    old_reactions : `None`, ``ReactionMapping``
        The old reactions on a message.
    
    Returns
    -------
    real_reactions : `None`, ``ReactionMapping``
        The real merged reactions on a message.
    """
    if (old_reactions is None):
        return new_reactions
    
    if (new_reactions is None):
        old_reactions.clear()
        return old_reactions
    
    old_reactions.lines = merge_update_reaction_mapping_lines(new_reactions.lines, old_reactions.lines)
    return old_reactions
