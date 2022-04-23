__all__ = ()

from .constants import EXTENSION_ROOTS

def is_tuple_starting_with(tuple_1, tuple_2):
    """
    Returns whether `tuple_1` starts with `tuple_2`.
    
    Parameters
    ----------
    tuple_1 : `tuple`
        The first tuple which should start with the second one.
    tuple_2 : `tuple`
        The second tuple.
    
    Returns
    -------
    is_tuple_starting_with : `bool`
    """
    tuple_1_length = len(tuple_1)
    tuple_2_length = len(tuple_2)
    
    if tuple_1_length > tuple_2_length:
        return tuple_1[:tuple_2_length] == tuple_2
    
    if tuple_1_length == tuple_2_length:
        return tuple_1 == tuple_2
    
    return False


def register_extension_root(name):
    """
    Registers an extension root. Extensions roots might be used to detect nested extension files.
    
    Parameters
    ----------
    name : `str`
        An extension's name.
    """
    name_split = tuple(name.split('.'))
    
    for extension_root in EXTENSION_ROOTS:
        if is_tuple_starting_with(name_split, extension_root):
            return
    
    to_remove_roots = None
    
    for extension_root in EXTENSION_ROOTS:
        if is_tuple_starting_with(extension_root, name_split):
            if to_remove_roots is None:
                to_remove_roots = []
            
            to_remove_roots.append(extension_root)
    
    if (to_remove_roots is not None):
        for extension_root in to_remove_roots:
            EXTENSION_ROOTS.discard(extension_root)
    
    EXTENSION_ROOTS.add(name_split)


def is_in_extension_root(name):
    """
    Returns whether the given name is inside of an extension root.
    
    Parameters
    ----------
    name : `str`
        An extension's name.
    
    Returns
    -------
    is_in_extension_root : `bool`
    """
    name_split = tuple(name.split('.'))
    for extension_root in EXTENSION_ROOTS:
        if is_tuple_starting_with(name_split, extension_root):
            return True
    
    return False
