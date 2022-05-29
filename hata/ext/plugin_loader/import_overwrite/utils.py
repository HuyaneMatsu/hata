__all__ = ()

from types import ModuleType


def try_set_attribute(module, attribute_name, attribute_value):
    """
    Tries to set to the module the given attributes.
    
    Parameters
    ----------
    module : ``ModuleType``
        The module type to set the attribute to.
    attribute_name : `str`
        The attribute's name to set.
    attribute_value : `object`
        The attribute value.
    """
    try:
        setattr(module, attribute_name, attribute_value)
    except AttributeError:
        pass


def create_module_from_spec(spec):
    """
    Creates a module from the given spec.
    
    Parameters
    ----------
    spec : ``PluginModuleSpecType``
        The module spec to create it's module for.
    
    Returns
    -------
    module : `ModuleType`
    """
    module = ModuleType(spec.name)
    
    try_set_attribute(module, '__name__', spec.name)
    try_set_attribute(module, '__loader__', spec.loader)
    try_set_attribute(module, '__package__', spec.parent)
    try_set_attribute(module, '__spec__', spec)
    try_set_attribute(module, '__path__', spec.submodule_search_locations)
    try_set_attribute(module, '__file__', spec.origin)
    try_set_attribute(module, '__cached__', spec.cached)
    
    return module
