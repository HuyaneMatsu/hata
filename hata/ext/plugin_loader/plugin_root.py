__all__ = ()

from .constants import PLUGIN_ROOTS


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


def register_plugin_root(name):
    """
    Registers an plugin root. Plugin roots might be used to detect nested plugin files.
    
    Parameters
    ----------
    name : `str`
        A plugin's name.
    """
    name_split = tuple(name.split('.'))
    
    for plugin_root in PLUGIN_ROOTS:
        if is_tuple_starting_with(name_split, plugin_root):
            return
    
    to_remove_roots = None
    
    for plugin_root in PLUGIN_ROOTS:
        if is_tuple_starting_with(plugin_root, name_split):
            if to_remove_roots is None:
                to_remove_roots = []
            
            to_remove_roots.append(plugin_root)
    
    if (to_remove_roots is not None):
        for plugin_root in to_remove_roots:
            PLUGIN_ROOTS.discard(plugin_root)
    
    PLUGIN_ROOTS.add(name_split)


def is_in_plugin_root(name):
    """
    Returns whether the given name is inside of an plugin root.
    
    Parameters
    ----------
    name : `str`
        A plugin's name.
    
    Returns
    -------
    is_in_plugin_root : `bool`
    """
    name_split = tuple(name.split('.'))
    for plugin_root in PLUGIN_ROOTS:
        if is_tuple_starting_with(name_split, plugin_root):
            return True
    
    return False
