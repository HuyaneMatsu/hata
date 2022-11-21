__all__ = ()

from os.path import  dirname as get_directory_name, join as join_paths
from scarletio import get_frame_module, get_last_module_frame
from scarletio.tools.asynchronous_interactive_console import (
    collect_module_variables, create_banner, create_exit_message, run_asynchronous_interactive_console
)
from scarletio.tools.asynchronous_interactive_console.console_helpers import AWAIT_NOTE

from .... import __package__ as PACKAGE_NAME

from ... import register


PACKAGE = __import__(PACKAGE_NAME)


def is_module_library_main(module):
    """
    Returns whether the module is the library's main file.
    
    Parameters
    ----------
    module : `ModuleType`
        The module to analyze.
    
    Returns
    -------
    is_module_library_main : `bool`
    """
    module_file_name = getattr(module, '__file__', None)
    if module_file_name is None:
        return False
    
    package_file_name = getattr(PACKAGE, '__file__', None)  
    if (package_file_name is None):
        return False
    
    if module_file_name != join_paths(get_directory_name(package_file_name), '__main__.py'):
        return False
    
    return True


def collect_variables():
    """
    Collects variables for the asynchronous console.
    
    Returns
    -------
    module_variables : `dict` of (`str`, `object`) items
    """
    module = get_frame_module(get_last_module_frame())
    if (module is None) or is_module_library_main(module):
        return collect_module_variables(PACKAGE)
    
    return collect_module_variables(module)


@register(
    alters = 'i',
    description =  f'Runs asynchronous python interpreter through scarletio.\n{AWAIT_NOTE}',
)
def interpreter():
    """
    Runs asynchronous console.
    """
    run_asynchronous_interactive_console(
        collect_variables(),
        banner = create_banner(PACKAGE),
        exit_message = create_exit_message(PACKAGE),
    )
