__all__ = ()

import sys
from importlib.machinery import SourceFileLoader

from scarletio import include

from .module_proxy_type import PluginModuleProxyType
from .utils import create_module_from_spec


import_plugin = include('import_plugin')


class PluginSourceLoader(SourceFileLoader):
    """
    `SourceFileLoader` subclass used for plugin files.
    
    Attributes
    ----------
    _module : `None`, ``ModuleType``
        The cached module if any.
    _module_proxy : `None`, ``PluginModuleProxyType``
        Module proxy proxying the created module through an plugin.
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
        Creates the module of the plugin source loader.
        
        Returns
        -------
        module : ``PluginModuleProxyType``
        """
        module_proxy = self._module_proxy
        if module_proxy is None:
            module_proxy = PluginModuleProxyType(spec)
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
        module : ``ModuleType``, ``PluginModuleProxyType``
            The module to execute.
            
            > If called from importlib, `module` is passed as ``PluginModuleProxyType``.
        """
        if isinstance(module, PluginModuleProxyType):
            module_proxy = self._module_proxy
            if (module_proxy is None):
                raise RuntimeError(
                    f'Module `{self.name}` is not created yet, but some why called with {module!r}.'
                )
            
            if module is not module_proxy:
                raise RuntimeError(
                    f'`module` must be `{module_proxy!r}, got {module!r}.'
                )
            
            import_plugin(self.name)
            
        else:
            code = self.get_code(module.__name__)
            if code is None:
                raise ImportError(
                    f'cannot load module {module.__name__} when `.get_code` returns None.'
                )
            
            exec(code, module.__dict__)
