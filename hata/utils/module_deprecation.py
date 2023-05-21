__all__ = ()

import sys, warnings
from types import ModuleType


DEPRECATIONS = []


def deprecated_import(obj = None, obj_name = None):
    """
    Deprecates the import.
    
    Parameters
    ----------
    obj : `object` = `None`, Optional
        The object to export.
    obj_name : `str` = `None`, Optional
        The name of the object. If not given, is detected from `obj` itself.
    
    Returns
    -------
    obj / wrapper : `object`, `functools.partial`
        Object if defined, else a wrapper.
    """
    if obj_name is None:
        if isinstance(obj, ModuleType):
            obj_name = obj.__name__
            dot_index = obj_name.rfind('.')
            if dot_index != -1:
                obj_name = obj_name[dot_index + 1:]
        
        else:
            try:
                obj_name = obj.__name__
            except AttributeError:
                obj_name = obj.__class__.__name__
    
    spec_name = sys._getframe().f_back.f_globals['__spec__'].name
    
    spec_access_path = tuple(spec_name.split('.'))
    DEPRECATIONS.append((spec_access_path, obj, obj_name))
    
    return obj


def _get_deprecations_for_spec_name(name):
    """
    Gets registered deprecations for the given spec name.
    
    Parameters
    ----------
    name : `str`
        Spec name.
    
    Returns
    -------
    deprecations : `dict` of (`str`, `object`) items
    """
    target_spec_access_path = tuple(name.split('.'))
    target_spec_access_path_length = len(target_spec_access_path)
    
    deprecations = {}
    
    for spec_access_path, obj, obj_name in DEPRECATIONS:
        spec_access_path_length = len(spec_access_path)
        
        if spec_access_path_length < target_spec_access_path_length:
            continue
        
        if spec_access_path_length > target_spec_access_path_length:
            spec_access_path = spec_access_path[:target_spec_access_path_length]
        
        if target_spec_access_path == spec_access_path:
            deprecations[obj_name] = obj
    
    return deprecations



def get_deprecation_function():
    """
    Creates a deprecation function deprecating everything under the current module.
    
    Returns
    -------
    __getattr__ : `FunctionType`
    """
    spec_name = sys._getframe().f_back.f_globals['__spec__'].name
    deprecations = _get_deprecations_for_spec_name(spec_name)
    
    
    def __getattr__(attribute_name):
        try:
            attribute_value = deprecations[attribute_name]
        except KeyError:
            pass
        else:
            warnings.warn(
                f'{spec_name}.{attribute_name} is deprecated.',
                FutureWarning,
                stacklevel = 2,
            )
            
            return attribute_value
        
        raise AttributeError(attribute_name)
    
    
    return __getattr__
