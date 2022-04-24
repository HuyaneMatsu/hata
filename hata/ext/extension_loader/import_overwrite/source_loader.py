__all__ = ()

import sys
from importlib.machinery import SourceFileLoader

from scarletio import include

from .module_proxy_type import ExtensionModuleProxyType
from .utils import create_module_from_spec

import_extension = include('import_extension')


class ExtensionSourceLoader(SourceFileLoader):
    """
    `SourceFileLoader` subclass used for extension files.
    
    Attributes
    ----------
    _module : `None`, ``ModuleType``
        The cached module if any.
    _module_proxy : `None`, ``ExtensionModuleProxyType``
        Module proxy proxying the created module through an extension.
    name : `str`
        The name of the represented module.
    path : `str`
        Path to the represented module.
    """
    def __init__(self, name, path):
        """
        Initialises the source file loader.
        
        Parameters
        ----------
        name : `str`
            The name of the represented module.
        path : `str`
            Path to the represented module.
        """
        SourceFileLoader.__init__(self, name, path)
        self._module = None
        self._module_proxy = None
    
    
    def create_module(self, spec):
        """
        Creates the module of the extension source loader.
        
        Returns
        -------
        module : ``ExtensionModuleProxyType``
        """
        module_proxy = self._module_proxy
        if module_proxy is None:
            module_proxy = ExtensionModuleProxyType(spec)
            self._module_proxy = module_proxy
        
        module = self._module
        if module is None:
            module = create_module_from_spec(spec)
            self._module = module
        
        sys.modules[self.name] = module_proxy
        
        return module_proxy
    
    
    def exec_module(self, module):
        """
        Executes the given module in the context.
        
        Parameters
        ----------
        module : ``ModuleType``, ``ExtensionModuleProxyType``
            The module to execute.
            
            > If called from importlib, `module` is passed as ``ExtensionModuleProxyType``.
        """
        if isinstance(module, ExtensionModuleProxyType):
            module_proxy = self._module_proxy
            if (module_proxy is None):
                raise RuntimeError(
                    f'Module `{self.name}` is not created yet, but some why called with {module!r}.'
                )
            
            if module is not module_proxy:
                raise RuntimeError(
                    f'`module` must be `{module_proxy!r}, got {module!r}.'
                )
            
            import_extension(self.name)
        else:
            SourceFileLoader.exec_module(self, self._module)
