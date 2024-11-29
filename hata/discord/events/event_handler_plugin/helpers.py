__all__ = ()


def _merge_to_type(iterable_0, iterable_1, target_type):
    """
    Merges the two iterable to one of the given type.
    
    Parameters
    ----------
    iterable_0 : `None | iterable`
        the first iterable to merge.
    
    iterable_1 : `None | iterable`
        the second iterable to merge.
    
    target_type : `type`
        The expected output type.
    
    Returns
    -------
    merged : `None | instance<target_type>`
        Returns `None` if both `iterable_0` and `iterable_1` are `None`.
    """
    if iterable_0 is None:
        if iterable_1 is None:
            merged = None
        else:
            if type(iterable_1) is target_type:
                merged = iterable_1
            else:
                merged = target_type(iterable_1)
    
    else:
        if iterable_1 is None:
            if type(iterable_0) is target_type:
                merged = iterable_0
            else:
                merged = target_type(iterable_0)
        
        else:
            merged = [*iterable_0, *iterable_1]
            
            if target_type is not list:
                merged = target_type(merged)
    
    return merged
