__all__ = ()

from importlib.machinery import PathFinder, ExtensionFileLoader

from ..constants import PLUGINS
from ..plugin_root import is_in_plugin_root

from .spec_finder_helpers import find_spec_in_paths, is_spec_in_test_directory
from .module_spec_type import PluginModuleSpecType


class PluginFinder(PathFinder):
    """
    Plugin finder type. Subclass of ``PathFinder``
    """
    @classmethod
    def find_spec(cls, full_name, paths = None, target = None):
        """
        Tries to find the module specification of the given name.
        
        Parameters
        ----------
        full_name : `str`
            The full name of the module to find.
        paths : `None`, `list` of `str` = `None`, Optional
            Path to find the module in.
        target : `None`, `object` = `None`, Optional
            Helper value to find the target specification.
            
            > Could not find a case where this value is actually used.
        
        Returns
        -------
        module_specification : `None`, ``PluginModuleSpecType``
        """
        try:
            plugin = PLUGINS[full_name]
        except KeyError:
            pass
        else:
            return plugin._spec
        
        if not is_in_plugin_root(full_name):
            return None
        
        spec = find_spec_in_paths(full_name, paths)
        if spec is None:
            return None
        
        if is_spec_in_test_directory(spec):
            return None
        
        loader = spec.loader
        if loader is None:
            return None
        
        if isinstance(loader, ExtensionFileLoader):
            return spec
        
        return PluginModuleSpecType(spec)
