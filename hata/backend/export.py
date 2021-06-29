__all__ = ()

import sys
from importlib.util import module_from_spec
from types import ModuleType

INCLUDED = {}
SATISFIED = {}

def include(obj_name):
    """
    Includes the object with the given name. The requirement is satisfied when the respective object is exported.
    
    Parameters
    ----------
    obj_name : `str`
        The object name to include when exported.
    
    Returns
    -------
    spaceholder : `NotImplementedType`
        Spaceholder to trick the editors.
    """
    frame = sys._getframe().f_back
    spec = frame.f_globals['__spec__']
    module = sys.modules.get(spec.name, None)
    if module is None:
        module = module_from_spec(spec)
    
    try:
        value = SATISFIED[obj_name]
    except KeyError:
        pass
    else:
        return value
    
    try:
        modules = INCLUDED[obj_name]
    except KeyError:
        modules = INCLUDED[obj_name] = set()
    
    modules.add(module)
    
    return NotImplemented


def export(obj, obj_name=None):
    """
    Exports the given object.
    
    Parameters
    ----------
    obj : `Any`
        The object to export.
    obj_name : `str`, Optional
        The name of the object. If not given, is detected from `obj` itself.
    """
    if obj_name is None:
        try:
            obj_name = obj.__name__
        except AttributeError:
            obj_name = obj.__class__.__name__
    
    if type(obj) is ModuleType:
        obj_name = obj_name[obj_name.rfind('.')+1:]
    
    SATISFIED[obj_name] = obj
    
    try:
        modules = INCLUDED.pop(obj_name)
    except KeyError:
        pass
    else:
        for module in modules:
            setattr(module, obj_name, obj)
    
    return obj


def check_satisfaction():
    """
    Checks whether every ``include`` requirement is satisfied with ``export``.
    
    Raises
    ------
    AssertionError
    """
    assert (not INCLUDED), f'Unsatisfied includes: {", ".join(INCLUDED.keys())}'
