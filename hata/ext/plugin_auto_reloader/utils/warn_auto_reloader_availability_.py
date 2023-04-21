__all__ = ('warn_auto_reloader_availability',)

import warnings

from ..compatibility import AUTO_RELOAD_SUPPORTED, IS_LINUX


def warn_auto_reloader_availability(*, do_raise = False):
    """
    Warns if auto reload is not available.
    
    Parameters
    ----------
    do_raise : `bool` = `False`, Optional (Keyword only)
        Whether an exception should be raised instead.
    
    Raises
    ------
    RuntimeError
        - If auto reloading is no available.
    """
    if AUTO_RELOAD_SUPPORTED:
        return
    
    if not IS_LINUX:
        reason = 'Auto reloader only is available only on linux.'
    else:
        reason = 'Required package `inotify_simple` is not installed.'
    
    message = f'Plugin auto reloading is not available:\n{reason}'
    
    if do_raise:
        raise RuntimeError(message)
    
    warnings.warn(message, RuntimeWarning, stacklevel = 2)
