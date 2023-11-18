__all__ = ()

from types import CodeType


VALUABLE_CODE_FIELDS = (CodeType.co_consts, CodeType.co_code, CodeType.co_names)


def _hash_function(function):
    """
    Hashes the give function.
    
    Parameters
    ----------
    function : `None | FunctionType | MethodType`
        The function to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    if function is None:
        return 0
    
    code = function.__code__
    
    hash_value = 0
    
    for descriptor in VALUABLE_CODE_FIELDS:
        hash_value ^= hash(type(descriptor).__get__(descriptor, code))
    
    return hash_value


def _eq_functions(function_0, function_1):
    """
    Returns whether the two given functions are the same.
    
    Parameters
    ----------
    function_0 : `None | FunctionType | MethodType`
        Function to equal with.
    function_1 : `None | FunctionType | MethodType`
        Function to equal with.
    
    Returns
    -------
    are_equal : `bool`
    """
    if function_0 is function_1:
        return True
    
    if (function_0 is None) or (function_1 is None):
        return False
    
    code_0 = function_0.__code__
    code_1 = function_1.__code__
    
    for descriptor in VALUABLE_CODE_FIELDS:
        getter = type(descriptor).__get__
        if getter(descriptor, code_0) != getter(descriptor, code_1):
            return False
    
    return True


SORT_KEY = lambda item: item[0]


def _hash_dict(value):
    """
    Hashes the given dictionary.
    
    Parameters
    ----------
    value : `dict<hashable & sortable, hashable>`
        Value to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    return  hash((*sorted(value.items(), key = SORT_KEY),))


def _hash_change_value(value):
    """
    Hashes an audit log change's `.before` or `.after` value.
    
    Parameters
    ----------
    value : `None | hashable | dict<hashable & sortable, hashable>`
        Value to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    if value is None:
        hash_value = 0
    elif isinstance(value, dict):
        hash_value = _hash_dict(value)
    else:
        hash_value = hash(value)

    return hash_value
