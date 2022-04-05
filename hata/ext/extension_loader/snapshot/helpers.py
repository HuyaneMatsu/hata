__all__ = ()

def _merge_list_groups(group_1, group_2):
    """
    Mergers the two list groups.
    
    Merging groups is a pre-operation of difference calculation, so copying is not required.
    
    Parameters
    ----------
    group_1 : `None`, `list` of `Any`
        The first group to merge.
    group_2 : `None`, `list` of `Any`
        The second group to merge.
    
    Returns
    -------
    merged_group : `None`, `list` of `Any`
        The merged groups.
    """
    if group_1 is None:
        return group_2
    
    if group_2 is None:
        return group_1
    
    merged_group = [*group_1]
    for value in group_2:
        if (value not in merged_group):
            merged_group.append(value)
    
    return merged_group


def _merge_set_groups(group_1, group_2):
    """
    Mergers the two set groups.
    
    Merging groups is a pre-operation of difference calculation, so copying is not required.
    
    Parameters
    ----------
    group_1 : `None`, `set` of `Any`
        The first group to merge.
    group_2 : `None`, `set` of `Any`
        The second group to merge.
    
    Returns
    -------
    merged_group : `None`, `set` of `Any`
        The merged groups.
    """
    if group_1 is None:
        return group_2
    
    if group_2 is None:
        return group_1
    
    return {*group_1, *group_2}


def _get_list_difference(group_1, group_2):
    """
    Calculates the difference between the two event value group.
    
    The returned lists are always a copy of the original.
    
    Parameters
    ----------
    group_1 : `None`, `list` of `Any`
        The first group.
    group_2 : `None`, `list` of `Any`
        The second group.
    
    Returns
    -------
    group_1 : `None`, `list` of `Any`
        The first group.
    group_2 : `None`, `list` of `Any`
        The second group.
    """
    not_null = 0
    
    if (group_1 is not None):
        group_1 = group_1.copy()
        not_null += 1
        
    if (group_2 is not None):
        group_2 = group_2.copy()
        not_null += 1
    
    if not_null == 2:
        for index in reversed(range(len(group_1))):
            value = group_1[index]
            try:
                group_2.remove(value)
            except ValueError:
                pass
            else:
                del group_1[index]
        
        if not group_2:
            group_2 = None
        
        if not group_1:
            group_1 = None
    
    return group_1, group_2


def _get_set_difference(group_1, group_2):
    """
    Calculates the difference between the two event value group.
    
    The returned sets are always a copy of the original.
    
    Parameters
    ----------
    group_1 : `None`, `set` of `Any`
        The first group.
    group_2 : `None`, `set` of `Any`
        The second group.
    
    Returns
    -------
    new_group_1 : `None`, `set` of `Any`
        The first group.
    new_group_2 : `None`, `set` of `Any`
        The second group.
    """
    if (group_1 is None) or (group_2 is None):
        if (group_1 is None):
            new_group_1 = None
        else:
            new_group_1 = group_1.copy()
            
        if (group_2 is None):
            new_group_2 = None
        else:
            new_group_2 = group_2.copy()
    
    else:
        new_group_1 = group_1 - group_2
        new_group_2 = group_2 - group_1
        
        if not new_group_1:
            new_group_1 = None
        
        if not new_group_2:
            new_group_2 = None
    
    return new_group_1, new_group_2
