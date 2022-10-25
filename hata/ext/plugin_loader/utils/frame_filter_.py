__all__ = ('frame_filter',)

from ..import_overwrite.source_loader import __file__ as PLUGIN_LOADER_SOURCE_LOADER_FILE_PATH
from ..plugin import __file__ as PLUGIN_LOADER_PLUGIN_FILE_PATH
from ..plugin_loader import __file__ as PLUGIN_LOADER_PLUGIN_LOADER_FILE_PATH


def frame_filter(file_name, name, line_number, line):
    """
    Ignores import frames of plugin loading.
    
    Parameters
    ----------
    file_name : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line_number : `int`
        The line's index where the exception occurred.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    if file_name.startswith('<') and file_name.endswith('>'):
        should_show_frame = False
    
    elif file_name == PLUGIN_LOADER_PLUGIN_FILE_PATH:
        if name == '_load':
            if line == 'loaded = self._load_module()':
                should_show_frame = False
        
        elif name == '_load_module':
            if line == 'spec.loader.exec_module(module)':
                should_show_frame = False
    
    elif file_name == PLUGIN_LOADER_PLUGIN_LOADER_FILE_PATH:
        if name == '_plugin_loader_task':
            if line in (
                'module = await KOKORO.run_in_executor(plugin._load)',
                'await entry_point(module)',
                'entry_point(module)',
            ):
                should_show_frame = False
        
        elif name == '_plugin_unloader_task':
            if line in (
                'await exit_point(module)',
                'exit_point(module)',
            ):
                should_show_frame = False
        
        elif name == '_run_maybe_blocking':
            if line == 'return run_coroutine(coroutine, KOKORO)':
                should_show_frame = False
    
    elif file_name == PLUGIN_LOADER_SOURCE_LOADER_FILE_PATH:
        if name == 'exec_module':
            if line in (
                'SourceFileLoader.exec_module(self, self._module)',
                'import_plugin(self.name)',
            ):
                should_show_frame = False
    
    return should_show_frame
