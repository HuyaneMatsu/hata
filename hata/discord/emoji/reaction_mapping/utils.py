__all__ = ('merge_update_reaction_mapping',)

def merge_update_reaction_mapping(old_reactions, new_reactions):
    """
    Merges the two reaction mapping, so values wont be overwritten if not required.
    
    Parameters
    ----------
    old_reactions : `None`, ``ReactionMapping``
        The old reactions on a message.
    new_reactions : `None`, ``ReactionMapping``
        The new reactions on a message.
    
    Returns
    -------
    real_reactions : `None`, ``ReactionMapping``
        The real merged reactions on a message.
    """
    if (old_reactions is None):
        return new_reactions
    
    elif (new_reactions is None):
        old_reactions.clear()
        return old_reactions
    
    old_emojis = {*old_reactions.keys()}
    new_emojis = {*new_reactions.keys()}
    
    for emoji in old_emojis - new_emojis:
        del old_reactions[emoji]
    
    for emoji in new_emojis - old_emojis:
        old_reactions[emoji] = new_reactions[emoji].copy()
    
    for emoji in new_emojis & old_emojis:
        old_users = old_reactions[emoji]
        new_users = new_reactions[emoji]
        
        if (len(old_users) != len(new_users)) or (not (old_users >= new_users)):
            old_reactions[emoji] = new_reactions[emoji].copy()
    
    old_reactions._full_check()
    
    return old_reactions
