__all__ = ('PluginModuleProxyType',)

from types import ModuleType

from scarletio import get_last_module_frame, include

from ..constants import PLUGINS

from .spec_finder_helpers import is_spec_in_test_directory


PluginModuleSpecType = include('PluginModuleSpecType')


class PluginModuleProxyType(ModuleType):
    """
    Represents a plugin module's proxy.
    """
    def __init__(self, spec):
        """
        Creates a new plugin module proxy.
        
        Parameters
        ----------
        spec : ``PluginModuleSpecType``
            Module specification.
        """
        ModuleType.__init__(self, spec.name)
        
        self.__spec__ = spec
        self.__file__ = spec.origin
    
    
    def __setattr__(self, attribute_name, attribute_value):
        ModuleType.__setattr__(self, attribute_name, attribute_value)
        
        if attribute_name in {
            '__spec__',
            '__loader__',
            '__package__',
            '__spec__',
            '__path__',
            '__file__',
            '__cached__',
        }:
            return
        
        if isinstance(attribute_value, PluginModuleProxyType):
            spec = self.__spec__
            
            module = spec.get_module()
            if (module is not None):
                setattr(module, attribute_name, attribute_value)
            
            return
        
        if isinstance(attribute_value, ModuleType):
            spec = attribute_value.__spec__
            if (spec is None) or is_spec_in_test_directory(spec):
                return
        
        
        spec = self.__spec__
        module = spec.get_module()
        if (module is not None):
            setattr(module, attribute_name, attribute_value)
        
        current_plugin = PLUGINS.get(spec.name, None)
        if (current_plugin is not None):
            plugin = _try_get_source_plugin()
            if (plugin is not None):
                plugin.add_child_plugin(current_plugin)
                current_plugin.add_parent_plugin(plugin)
    
    
    def __getattr__(self, attribute_name):
        spec = self.__spec__
        module = spec.get_module()
        
        if module is None:
            raise RuntimeError(
                f'Plugin, `{spec.name}` is not yet initialized!'
            )
        
        try:
            attribute_value = getattr(module, attribute_name)
        except AttributeError:
            raise AttributeError(
                f'{self!r} has no attribute `{attribute_name}`.'
            ) from None
        
        current_plugin = PLUGINS.get(spec.name, None)
        if (current_plugin is not None):
            plugin = _try_get_source_plugin()
            if (plugin is not None):
                plugin.add_child_plugin(current_plugin)
                current_plugin.add_parent_plugin(plugin)
        
        return attribute_value
    
    
    def __repr__(self):
        spec = getattr(self, '__spec__', None)
        
        repr_parts = ['<', type(self).__name__]
        
        if spec is None:
            repr_parts.append(' unknown location')
        
        else:
            repr_parts.append(' from ')
            repr_parts.append(spec.name)
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __dir__(self):
        directory = {*ModuleType.__dir__(self)}
        
        module = self.__spec__.get_module()
        if (module is not None):
            directory.update(dir(module))
        
        return sorted(directory)


def _try_get_source_plugin():
    """
    Tries to get the source plugin where the call was made from.
    
    Returns
    -------
    plugin : ``None | Plugin``
    """
    frame = get_last_module_frame()
    if (frame is None):
        return
    
    spec = frame.f_globals.get('__spec__', None)
    if spec is None:
        return
    
    return PLUGINS.get(spec.name)
