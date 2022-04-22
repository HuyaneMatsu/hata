__all__ = ('ExtensionModuleProxyType',)

from types import ModuleType


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
        module = self.__spec__.get_module()
        
        if module is None:
            raise RuntimeError(
                f'Extension, {self.__extension__!r} is not yet initialized!'
            )
        
        return getattr(module, attribute_name)
