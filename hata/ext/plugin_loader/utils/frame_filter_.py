__all__ = ('frame_filter',)

from py_compile import __file__ as PY_COMPILE_FILE_PATH

from ..import_overwrite.source_loader import __file__ as PLUGIN_LOADER_SOURCE_LOADER_FILE_PATH
from ..plugin import __file__ as PLUGIN_LOADER_PLUGIN_FILE_PATH
from ..plugin_loader import __file__ as PLUGIN_LOADER_PLUGIN_LOADER_FILE_PATH


def frame_filter(frame):
    """
    Ignores import frames of plugin loading.
    
    Parameters
    ----------
    frame : ``FrameProxyBase``
        The frame to check.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    file_name = frame.file_name
    name = frame.name
    line = frame.line
    
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
                'exec(code, module.__dict__)',
                'import_plugin(self.name)',
            ):
                should_show_frame = False
    
    elif file_name == PY_COMPILE_FILE_PATH:
        if name == 'compile':
            if line in (
                'code = loader.source_to_code(source_bytes, dfile or file,\n'
                '                             _optimize=optimize)'
            ):
                should_show_frame = False
    
    return should_show_frame
