__all__ = ('AUTO_RELOAD_SUPPORTED',)

from sys import platform


AUTO_RELOAD_SUPPORTED = False
INotify = None
INotifyFlags = None

IS_LINUX = platform == 'linux'

if IS_LINUX:
    try:
        from inotify_simple import INotify, flags as INotifyFlags
    except ImportError:
        pass
    else:
        AUTO_RELOAD_SUPPORTED = True
