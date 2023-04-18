__all__ = ()

from sys import platform


AUTO_RELOAD_SUPPORTED = False
INotify = None
INotifyFlags = None


if platform == 'linux':
    try:
        from inotify_simple import INotify, flags as INotifyFlags
    except ImportError:
        pass
    else:
        AUTO_RELOAD_SUPPORTED = True
