__all__ = ('mark_as_plugin_root_directory',)

from os import listdir as list_directory
from os.path import (
    basename as get_file_name, dirname as get_directory_name, isdir as is_directory, isfile as is_file,
    join as join_paths
)

from scarletio import get_last_module_frame

from ..constants import IGNORED_DIRECTORY_NAMES

from .import_plugin_ import import_plugin


def mark_as_plugin_root_directory():
    """
    Imports all sub-plugins from the directory.
    
    Returns
    -------
    count : `int`
        The amount of sub-plugins imported.
    
    Raises
    ------
    RuntimeError
        - If called from other file than `__init__.py`.
    """
    module_frame = get_last_module_frame()
    if (module_frame is None):
        return 0
    
    frame_globals = module_frame.f_globals
    spec = frame_globals.get('__spec__', None)
    if spec is None:
        return
    
    source_file_path = spec.origin

    if get_file_name(source_file_path) != '__init__.py':
        raise RuntimeError(
            f'Cannot set directory level environment, top level file is not an `__init__.py` file.'
        )
    
    frame_globals.setdefault('__all__', ())
    
    source_directory_path = get_directory_name(source_file_path)
    source_name = spec.name
    
    for file_name in list_directory(source_directory_path):
        if file_name == '__init__.py':
            continue
        
        file_path = join_paths(source_directory_path, file_name)
        if is_file(file_path):
            if not file_path.endswith('.py'):
                continue
            
            file_name = file_name[:-len('.py')]
        
        elif is_directory(file_path):
            if file_name in IGNORED_DIRECTORY_NAMES:
                continue
            
            if not is_file(join_paths(file_path, '__init__.py')):
                continue
        
        else:
            continue
        
        import_plugin(f'{source_name}.{file_name}')
        continue
