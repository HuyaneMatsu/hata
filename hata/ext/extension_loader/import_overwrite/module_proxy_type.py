__all__ = ('ExtensionModuleProxyType',)

from types import ModuleType

from scarletio import get_last_module_frame

from ..constants import EXTENSIONS


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
        
        if (extension is not None) and (current_extension is not None):
            extension.add_child_extension(current_extension)
            current_extension.add_parent_extension(extension)
        
        return attribute_value

