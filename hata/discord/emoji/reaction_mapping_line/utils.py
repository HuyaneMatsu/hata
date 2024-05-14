__all__ = ('merge_update_reaction_mapping_lines',)


def merge_update_reaction_mapping_lines(new_lines, old_lines):
    """
    Merges reaction mapping lines.
    
    Parameters
    ----------
    new_lines : `None | dict<Reaction, ReactionMappingLine>`
        New lines.
    old_lines : `None | dict<Reaction, ReactionMappingLine>`
        Old lines.
    
    Returns
    -------
    line : `None | list<ReactionMappingLine>`
    """
    if new_lines is None:
        return None
    
    if old_lines is None:
        return new_lines
    
    # Remove not alive answer_id-s
    for reaction, old_line in [*old_lines.items()]:
        if reaction not in new_lines:
            del old_lines[reaction]
    
    # Merge old with new.
    for reaction, new_line in new_lines.items():
        old_line = old_lines.get(reaction, None)
        if old_line is None:
            old_lines[reaction] = new_line
        else:
            old_line._merge_with(new_line)

    return old_lines
