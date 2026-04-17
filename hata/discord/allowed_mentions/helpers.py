__all__ = ()


def _nullable_list_intersection(list_0, list_1):
    """
    Returns the intersection of 2 nullable lists.
    
    Parameters
    ----------
    list_0 : `None | list`
        Input list.
    list_1 : `None | list`
        Input list.
    
    Returns
    -------
    intersection : `None | list`
        A list with the two list's intersection.
    """
    if list_0 is None:
        return None
    
    if list_1 is None:
        return None
    
    intersection = {*list_0} & {*list_1}
    if not intersection:
        return None
    
    return [*intersection]


def _nullable_list_symmetric_difference(list_0, list_1):
    """
    Returns the symmetric difference of 2 nullable lists.
    
    Parameters
    ----------
    list_0 : `None | list`
        Input list.
    list_1 : `None | list`
        Input list.
    
    Returns
    -------
    symmetric_difference : `None | list`
        A list with the two list's symmetric difference.
    """
    if list_0 is None:
        if list_1 is None:
            return None
        
        else:
            return list_1.copy()
    
    else:
        if list_1 is None:
            return list_0.copy()
    
    symmetric_difference = {*list_0} ^ {*list_1}
    if not symmetric_difference:
        return None
    
    return [*symmetric_difference]


def _nullable_list_union(list_0, list_1):
    """
    Returns the union of 2 nullable lists.
    
    Parameters
    ----------
    list_0 : `None | list`
        Input list.
    list_1 : `None | list`
        Input list.
    
    Returns
    -------
    union : `None | list`
        A list with the two list's union.
    """
    if list_0 is None:
        if list_1 is None:
            return None
        
        else:
            return list_1.copy()
    
    else:
        if list_1 is None:
            return list_0.copy()
        
        else:
            return [*{*list_0, *list_1}]


def _nullable_list_difference(list_0, list_1):
    """
    Returns the a copy of `list_0` without the elements of `list_1`.
    
    Parameters
    ----------
    list_0 : `None | list`
        Input list.
    list_1 : `None | list`
        Input list.
    
    Returns
    -------
    difference : `None | list`
        A list with the two list's difference.
    """
    if list_0 is None:
        return None
    
    if list_1 is None:
        return list_0.copy()
    
    difference = {*list_0} - {*list_1}
    if not difference:
        return None
    
    return [*difference]

