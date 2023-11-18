__all__ = ()


def value_merger_sorted_array(value_0, value_1):
    """
    Merges two sorted array.
    
    Parameters
    ----------
    value_0 : `None | tuple<sortable>`
        Self instance's value.
    value_1 : `None | tuple<sortable>`
        Other instance's value.
    
    Returns
    -------
    new : `None | tuple<sortable>`
    """
    if value_0 is None:
        return value_1
    
    if value_1 is None:
        return value_0
    
    merged = [*value_0, *value_1]
    merged.sort()
    
    return tuple(merged)


def value_merger_replace(value_0, value_1):
    """
    Merges any 2 values.
    
    Parameters
    ----------
    value_0 : `None | object`
        Self instance's value.
    value_1 : `None | object``
        Other instance's value.
    
    Returns
    -------
    new : `None | object`
    """
    if value_0 is None:
        return value_1
    
    if value_1 is None:
        return value_0
    
    return value_1
