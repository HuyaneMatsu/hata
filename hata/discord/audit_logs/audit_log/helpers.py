__all__ = ()


def _merge_dictionaries(iterator):
    """
    Merges multiple dictionaries into one.
    
    Parameters
    ----------
    iterator : `iterable<None | dict>`
        An iterable over multiple dictionaries.
    
    Returns
    -------
    output : `None | dict`
    """
    output = None
    
    for dictionary in iterator:
        if dictionary is None:
            continue
        
        if output is None:
            output = {}
        
        output.update(dictionary)
    
    return output


def _merge_lists(iterator):
    """
    Merges multiple lists into one.
    
    Parameters
    ----------
    iterator : `iterable<None | list>`
        An iterable over multiple lists.
    
    Returns
    -------
    output : `None | list`
    """
    output = None
    
    for list_ in iterator:
        if list_ is None:
            continue
        
        if output is None:
            output = []
        
        output.extend(list_)
    
    return output
