__all__ = ()

from importlib.machinery import ModuleSpec

from scarletio import export

from .source_loader import ExtensionSourceLoader


@export
class ExtensionModuleSpecType(ModuleSpec):
    """
    Extends the builtin spec with extension checking.
    """
    def __init__(self, other):
        """
        `ModuleSpec` subclass implementing rich context for extensions.
        
        Parameters
        ----------
        other : ``ModuleSpec``
            The other module spec to inherit from.
        """
        self.__dict__.update(other.__dict__)
        loader = other.loader
        self.loader = ExtensionSourceLoader(loader.name, loader.path)
        self._initializing_internal = False
    
    
    def is_initialised(self):
        """
        Returns whether the module spec is initialised.
        
        Returns
        -------
        is_initialised : `bool`
        """
        loader = self.loader
        if loader is None:
            return False
        
        if not isinstance(loader, ExtensionSourceLoader):
            return False
        
        if loader._module is None:
            return False
        
        return True
    
    
    def get_module(self):
        """
        Returns the module spec's real module.
        
        Returns
        -------
        module : `None`, ``ModuleType``
        """
        loader = self.loader
        if loader is None:
            return None
        
        if not isinstance(loader, ExtensionSourceLoader):
            return None
        
        return loader._module
    
    
    def get_module_proxy(self):
        """
        Returns the module spec's proxy module.
        
        Returns
        -------
        module : `None`, ``ExtensionModuleProxyType``
        """
        loader = self.loader
        if loader is None:
            return None
        
        if not isinstance(loader, ExtensionSourceLoader):
            return None
        
        return loader._module_proxy
