__all__ = ('PLUGIN_AUTO_RELOADER_MANAGER', 'PluginAutoReloaderManager', )

from os.path import join as join_paths

from scarletio import LOOP_TIME, Task
from scarletio import write_exception_async

from ...discord import KOKORO

from ..plugin_loader import PluginError, frame_filter, reload_plugin
from ..plugin_loader.constants import PLUGIN_ACTION_FLAG_NAME_LOOKUP

from .compability import AUTO_RELOAD_SUPPORTED, INotify
from .constants import AUTO_RELOAD_DELAY, WATCH_MASK_GENERAL
from .helpers import _iter_plugin_root_paths, _iter_sub_directories


class PluginAutoReloaderManager:
    _instance = None
    
    def __new__(cls):
        self = cls._instance
        if self is not None:
            return self
        
        self = object.__new__(cls)
        self._directory_watch_identifier_pairs = set()
        self._inotify = None
        self._updated_directories = {}
        self._updated_directories_at = -AUTO_RELOAD_DELAY
        self._last_failed_plugin_trees = None
        self._reload_callback_handle = None
        self._reload_task_active = False
        
        cls._instance = self
        return self
    
    
    def start(self):
        """
        Starts the auto reload manager.
        
        Returns
        -------
        success : `bool`
        """
        inotify = self._inotify
        if inotify is not None:
            return False
        
        if not AUTO_RELOAD_SUPPORTED:
            return False
        
        inotify = INotify(nonblocking = True)
        self._inotify = inotify
        KOKORO.add_reader(inotify.fd, self._reader_callback)
        
        self.update()
        return True
    
    
    def update(self):
        """
        Updates the auto reloaded directories.
        
        Returns
        -------
        success : `bool`
        """
        inotify = self._inotify
        if inotify is None:
            return False
        
        old_directories = {item[0] for item in self._directory_watch_identifier_pairs}
        new_directories = {*_iter_sub_directories(_iter_plugin_root_paths())}
        
        success = True
        
        for directory in new_directories - old_directories:
            if not self._add_directory(directory):
                success = False
        
        for directory in old_directories - new_directories:
            if not self._remove_directory(directory):
                success = False
        
        return success
    
    
    def stop(self):
        """
        Stops the auto reloader.
        
        Returns
        -------
        success : `bool`
        """
        inotify = self._inotify
        if (inotify is None):
            return False
        
        self._inotify = None
        KOKORO.remove_reader(inotify.fd)
        inotify.close()
        
        reload_callback_handle = self._reload_callback_handle
        if (reload_callback_handle is not None):
            self._reload_callback_handle = None
            reload_callback_handle.cancel()
    
    
    # Operations
    
    def _get_directory_by_watch_identifier(self, watch_identifier):
        for iterated_directory, iterated_watch_identifier in self._directory_watch_identifier_pairs:
            if iterated_watch_identifier == watch_identifier:
                return iterated_directory
    
    
    def _get_watch_identifier_by_directory(self, directory):
        for iterated_directory, iterated_watch_identifier in self._directory_watch_identifier_pairs:
            if iterated_directory == directory:
                return iterated_watch_identifier
    
    
    def _add_directory(self, directory):
        inotify = self._inotify
        if inotify is None:
            return False
        
        if (self._get_watch_identifier_by_directory(directory) is not None):
            return False
        
        watch_identifier = inotify.add_watch(directory, WATCH_MASK_GENERAL)
        self._directory_watch_identifier_pairs.add((directory, watch_identifier))
        return True
    
    
    def _remove_directory(self, directory):
        inotify = self._inotify
        if inotify is None:
            return False
        
        watch_identifier = self._get_watch_identifier_by_directory(directory)
        if (watch_identifier is None):
            return False
        
        try:
            inotify.rm_watch(watch_identifier)
        except OSError:
            return False
        
        self._directory_watch_identifier_pairs.discard((directory, watch_identifier))
        return True
    
    
    def _reader_callback(self):
        inotify = self._inotify
        if inotify is None:
            # Should not happen
            return
        
        try:
            events = inotify.read(timeout = 0.0)
        except BlockingIOError:
            return
        
        for event in events:
            self._handle_event(event)
    
    
    def _handle_event(self, event):
        # We only wanna handle py files.
        name = event.name
        if not event.name.endswith('.py'):
            return
        
        # Get directory
        directory = self._get_directory_by_watch_identifier(event.wd)
        if directory is None:
            # Unknown directory?
            return
        
        # Set file path into updated
        file_path = join_paths(directory, name)
        updated_directories = self._updated_directories
        updated_directories[file_path] = event.mask | updated_directories.get(file_path, 0)
        
        # Set update time
        self._updated_directories_at = LOOP_TIME()
        
        # Start callback
        reload_callback_handle = self._reload_callback_handle
        if (reload_callback_handle is None):
            self._reload_callback_handle = KOKORO.call_later(AUTO_RELOAD_DELAY, self._reload_callback)
        
    
    def _reload_callback(self):
        next = self._updated_directories_at + AUTO_RELOAD_DELAY
        if next > LOOP_TIME() or self._reload_task_active:
            self._reload_callback_handle = KOKORO.call_at(AUTO_RELOAD_DELAY, self._reload_callback)
            return
        
        self._reload_callback_handle = None
        
        Task(self._do_reload(), KOKORO)
    
    
    async def _do_reload(self):
        if self._reload_task_active:
            return
        
        self._reload_task_active = True
        try:
            while True:
                self_updated_directories = self._updated_directories
                if not self_updated_directories:
                    return
                
                updated_directories = self_updated_directories.copy()
                self_updated_directories.clear()
                
                plugin_names = [*updated_directories.keys()]
                
                while True:
                    try:
                        await reload_plugin(plugin_names)
                    except GeneratorExit:
                        raise
                    
                    except PluginError as err:
                        await write_exception_async(err, filter = frame_filter)
                        
                        if err.action & PLUGIN_ACTION_FLAG_NAME_LOOKUP:
                            plugin_name_path_pair = err.value
                            # Finding the failed plugin.
                            if plugin_name_path_pair is not None:
                                try:
                                    plugin_names.remove(plugin_name_path_pair[1])
                                except ValueError:
                                    pass
                                else:
                                    continue
                        
                    break
        
        finally:
            self._reload_task_active = False


PLUGIN_AUTO_RELOADER_MANAGER = PluginAutoReloaderManager()
