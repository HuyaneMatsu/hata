__all__ = ('ExtensionModuleProxyType',)

import warnings
from types import ModuleType

from scarletio import get_last_module_frame, include

from ..constants import EXTENSIONS

ExtensionModuleSpecType = include('ExtensionModuleSpecType')


class ExtensionModuleProxyType(ModuleType):
    """
    Represents an extension module's proxy.
    """
    def __init__(self, spec):
        """
        Creates a new extension module proxy.
        
        Parameters
        ----------
        spec : ``ExtensionModuleSpecType``
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
        
        elif isinstance(attribute_value, ExtensionModuleProxyType):
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
                f'Extension, {self.__extension__!r} is not yet initialized!'
            )
        
        attribute_value = getattr(module, attribute_name)
        
        frame = get_last_module_frame()
        if (frame is None):
            spec = None
        else:
            spec = frame.f_globals.get('__spec__', None)
        
        if spec is None:
            extension = None
        else:
            extension = EXTENSIONS.get(spec.name)
        
        current_extension = EXTENSIONS.get(spec.name, None)
        
        if (extension is not None) and (current_extension is not None) and (extension is not current_extension):
            extension.add_child_extension(current_extension)
            current_extension.add_parent_extension(extension)
        
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
