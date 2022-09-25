__all__ = ('PluginModuleProxyType',)

import warnings
from types import ModuleType

from scarletio import get_last_module_frame, include

from ..constants import PLUGINS

PluginModuleSpecType = include('PluginModuleSpecType')


class PluginModuleProxyType(ModuleType):
    """
    Represents an plugin module's proxy.
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
            pass
        
        elif isinstance(attribute_value, PluginModuleProxyType):
            spec = self.__spec__
            
            module = spec.get_module()
            if (module is not None):
                setattr(module, attribute_name, attribute_value)
        
        else:
            warnings.warn(
                f'Unallowed attribute assignment: `{attribute_name} = {attribute_value!r}` of type '
                f'`{type(attribute_value).__name__}` to `{self.__spec__.name}`'
            )
    
    
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
        
        frame = get_last_module_frame()
        if (frame is None):
            spec = None
        else:
            spec = frame.f_globals.get('__spec__', None)
        
        if spec is None:
            plugin = None
        else:
            plugin = PLUGINS.get(spec.name)
        
        
        if (plugin is not None) and (current_plugin is not None):
            plugin.add_child_plugin(plugin)
            current_plugin.add_parent_plugin(current_plugin)
        
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
