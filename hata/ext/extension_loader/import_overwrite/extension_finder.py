__all__ = ()

from importlib.machinery import PathFinder, ExtensionFileLoader

from ..constants import EXTENSIONS
from ..extension_root import is_in_extension_root

from .spec_finder_helpers import find_spec_in_paths
from .module_spec_type import ExtensionModuleSpecType


class ExtensionFinder(PathFinder):
    """
    Extension finder type. Subclass of ``PathFinder``
    """
    @classmethod
    def find_spec(cls, full_name, paths=None, target=None):
        """
        Tries to find the module specification of the given name.
        
        Parameters
        ----------
        full_name : `str`
            The full name of the module to find.
        paths : `None`, `list` of `str` = `None`, Optional
            Path to find the module in.
        target : `None`, `Any` = `None`, Optional
            Helper value to find the target specification.
            
            > Could not find a case where this value is actually used.
        """
        try:
            extension = EXTENSIONS[full_name]
        except KeyError:
            pass
        else:
            return extension._spec
        
        if not is_in_extension_root(full_name):
            return None
        
        spec = find_spec_in_paths(full_name, paths)
        if spec is None:
            return None
        
        loader = spec.loader
        if loader is None:
            return None
        
        if isinstance(loader, ExtensionFileLoader):
            return spec
        
        return ExtensionModuleSpecType(spec)
