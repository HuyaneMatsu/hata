__all__ = ('PLUGIN_AUTO_RELOADER_MANAGER', 'PluginAutoReloaderManager', )

from os import listdir as list_directory
from os.path import dirname as get_parent_directory_path, isdir as is_directory, isfile as is_file, join as join_paths

from scarletio import LOOP_TIME, RichAttributeErrorBaseType, Task, write_exception_async

from ...discord import KOKORO

from ..plugin_loader import PluginError, frame_filter, get_plugin, register_plugin, reload_plugin
from ..plugin_loader.constants import IGNORED_DIRECTORY_NAMES

from .compatibility import AUTO_RELOAD_SUPPORTED, INotify
from .constants import (
    AUTO_RELOAD_DELAY, WATCH_MASK_CREATE, WATCH_MASK_DELETE, WATCH_MASK_DELETE_SELF, WATCH_MASK_GENERAL,
    WATCH_MASK_MOVE_FROM, WATCH_MASK_MOVE_SELF, WATCH_MASK_MOVE_TO, WATCH_MASK_UPDATE
)
from .helpers import _iter_plugin_root_paths, _iter_sub_directories


class PluginAutoReloaderManager(RichAttributeErrorBaseType):
    """
    Plugin auto reloader manager.
    
    Attributes
    ----------
    _directory_watch_identifier_pairs : `set` of `tuple` (`str`, `int`)
        Directory path - watcher identifier pairs.
    _inotify : `None`, `inotify_simple.Inotify`
        Inotify instance used by the auto reloader.
    _plugin_root_paths : `set` of `str`
        Paths to plugin roots.
    _reload_callback_handle : `None`, ``TimerHandle``
        Handle that delays reload.
    _updated_plugins : `set` of ``Plugin``
        Actioned plugins.
    _updated_plugins_at : `float`
        When the last actioned plugin was received in loop time.
    _reload_task_active : `bool`
        Whether reload task is active.
    """
    __slots__ = (
        '_directory_watch_identifier_pairs', '_inotify', '_plugin_root_paths', '_reload_callback_handle',
        '_reload_task_active', '_updated_plugins', '_updated_plugins_at'
    )
    
    _instance = None
    
    def __new__(cls):
        """
        Creates a new plugin reloader manager instance.
        If the type is already instanced, returns the existing instance instead.
        """
        self = cls._instance
        if self is not None:
            return self
        
        self = object.__new__(cls)
        self._directory_watch_identifier_pairs = set()
        self._inotify = None
        self._plugin_root_paths = set()
        self._reload_callback_handle = None
        self._reload_task_active = False
        self._updated_plugins = set()
        self._updated_plugins_at = -AUTO_RELOAD_DELAY
        
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
        
        plugin_root_paths = self._plugin_root_paths
        plugin_root_paths.clear()
        plugin_root_paths.update(_iter_plugin_root_paths())
        
        old_directories = {item[0] for item in self._directory_watch_identifier_pairs}
        new_directories = {*_iter_sub_directories(plugin_root_paths)}
        
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
        """
        Gets directory by watch identifier.
        
        Parameters
        ----------
        watch_identifier : `int`
            Watch identifier.
        
        Returns
        -------
        directory : `None`, `str`
            The matched directory. `None` if not found.
        """
        for iterated_directory, iterated_watch_identifier in self._directory_watch_identifier_pairs:
            if iterated_watch_identifier == watch_identifier:
                return iterated_directory
    
    
    def _get_watch_identifier_by_directory(self, directory):
        """
        Gets watch identifier by directory.
        
        Parameters
        ----------
        directory : `str`
            Directory path.
        
        Returns
        -------
        watch_identifier : `int`
            The matched watch identifier. `None` if not found.
        """
        for iterated_directory, iterated_watch_identifier in self._directory_watch_identifier_pairs:
            if iterated_directory == directory:
                return iterated_watch_identifier
    
    
    def _add_directory(self, directory):
        """
        Adds a new directory to watch.
        
        Parameters
        ----------
        directory : `str`
            Directory path.
        
        Returns
        -------
        success : `bool`
        """
        inotify = self._inotify
        if inotify is None:
            return False
        
        if (self._get_watch_identifier_by_directory(directory) is not None):
            return False
        
        watch_identifier = inotify.add_watch(directory, WATCH_MASK_GENERAL)
        self._directory_watch_identifier_pairs.add((directory, watch_identifier))
        return True
    
    
    def _remove_directory(self, directory):
        """
        Removes the directory from the watched ones.
        
        Parameters
        ----------
        directory : `str`
            Directory path.
        
        Returns
        -------
        success : `bool`
        """
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
        """
        Callback added to `inotify_simple.Inotify` read events.
        
        Reads from the file descriptors and calls ``._handle_event``.
        """
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
        """
        Handles a received inotify event.
        
        Parameters
        ----------
        event : `inotify_simple.Event`
            Inotify event.
        """
        # Get directory
        directory = self._get_directory_by_watch_identifier(event.wd)
        if directory is None:
            # Unknown directory?
            return
        
        # If the name is empty (directory case) we dont want to join it to the directory.
        name = event.name
        if name:
            path = join_paths(directory, name)
        else:
            path = directory
        
        if is_directory(path) and (event.name not in IGNORED_DIRECTORY_NAMES):
            self._handle_directory_event(event, path)
            return
        
        if is_file(path):
            # we only want py files
            if not path.endswith('.py'):
                return
            
            self._handle_file_event(event, path)
            return
        
        mask = event.mask
        
        # If a file is deleted the above two wont trigger.
        if mask & WATCH_MASK_DELETE or mask & WATCH_MASK_MOVE_FROM:
            if path.endswith('.py'):
                self._handle_file_or_plugin_directory_update_or_delete(path)
            return
        
        # If a directory is deleted the top 3 wont trigger (they might, but we ignore them)
        if mask & WATCH_MASK_DELETE_SELF or mask & WATCH_MASK_MOVE_SELF:
            if (self._get_watch_identifier_by_directory(path) is not None):
                self._remove_directory(path)
                self._handle_file_or_plugin_directory_update_or_delete(path)
            
            return
    
    
    def _handle_directory_event(self, event, directory_path):
        """
        Handles a received inotify event for a directory.
        
        Parameters
        ----------
        event : `inotify_simple.Event`
            Inotify event.
        directory_path : `str`
            Path to the directory.
        """
        mask = event.mask
        if mask & (WATCH_MASK_DELETE_SELF | WATCH_MASK_MOVE_FROM):
            self._remove_directory(directory_path)
            return
        
        if mask & WATCH_MASK_CREATE:
            self._handle_directory_create(directory_path)
            return
        
        if mask & WATCH_MASK_MOVE_TO:
            self._handle_directory_move_to(directory_path)
            return
    
    
    def _handle_directory_create(self, directory_path):
        """
        Handles a received directory create inotify event.
        
        Parameters
        ----------
        directory_path : `str`
            Path to the directory.
        """
        self._add_directory(directory_path)
        self._handle_directory_create_initial_entities(directory_path)
    
    
    def _handle_directory_move_to(self, directory_path):
        """
        handles a directory move-to inotify event.
        
        Parameters
        ----------
        directory_path : `str`
            Path to the directory.
        """
        self._handle_directory_create(directory_path)
        
        if get_parent_directory_path(directory_path) in self._plugin_root_paths:
            init_file_path = join_paths(directory_path, '__init__.py')
            if is_file(init_file_path):
                register_plugin(directory_path)
                self._handle_file_or_plugin_directory_update_or_delete(init_file_path)
    
    
    def _handle_directory_create_initial_entities(self, directory_path):
        """
        Called after a directory is created to scan it.
        
        Parameters
        ----------
        directory_path : `str`
            Path to the directory.
        """
        for name in list_directory(directory_path):
            path = join_paths(directory_path, name)
            if is_file(path):
                self._handle_file_create(name, path)
                continue
            
            if is_directory(path) and (name not in IGNORED_DIRECTORY_NAMES):
                self._handle_directory_create(path)
                continue
    
    
    def _handle_file_event(self, event, file_path):
        """
        Handles a received inotify event for a file.
        
        Parameters
        ----------
        event : `inotify_simple.Event`
            Inotify event.
        file_path : `str`
            Path to the file.
        """
        mask = event.mask
        if mask & WATCH_MASK_CREATE:
            self._handle_file_create(event.name, file_path)
            return
        
        if mask & WATCH_MASK_MOVE_TO:
            self._handle_file_move_to_event(event.name, file_path)
            return
        
        if mask & WATCH_MASK_UPDATE:
            self._handle_file_or_plugin_directory_update_or_delete(file_path)
            return
    
    
    def _handle_file_create(self, name, file_path):
        """
        Handles a received file create inotify event.
        
        Parameters
        ----------
        name : `str`
            The file's name.
        file_path : `str`
            Path to the file.
        
        Returns
        -------
        is_registered : `bool`
            Whether the file was registered as a plugin.
        """
        # If we register an init.py file in directory of a plugin root, we register it as a plugin
        if name == '__init__.py':
            parent_directory = get_parent_directory_path(file_path)
            if get_parent_directory_path(parent_directory) in self._plugin_root_paths:
                register_plugin(parent_directory)
                return True
        
        # If we register a file inside of a plugin directory, we again wanna register it as a plugin
        else:
            if get_parent_directory_path(file_path) in self._plugin_root_paths:
                register_plugin(file_path)
                return True
        
        return False
    
    
    def _handle_file_move_to_event(self, name, file_path):
        """
        handles a received file move-to inotify event.
        
        Parameters
        ----------
        name : `str`
            The file's name.
        file_path : `str`
            Path to the file.
        """
        if self._handle_file_create(name, file_path):
            self._handle_file_or_plugin_directory_update_or_delete(file_path)
    
    
    def _handle_file_or_plugin_directory_update_or_delete(self, file_path):
        """
        Handles a received file delete / edit inotify event.
        
        Parameters
        ----------
        file_path : `str`
            Path to the file.
        """
        # Get corresponding plugin
        plugin = get_plugin(file_path)
        if plugin is None:
            return
        
        # Set file path into updated
        self._updated_plugins.add(plugin)
        
        # Set update time
        self._updated_plugins_at = LOOP_TIME()
        
        # Start callback
        reload_callback_handle = self._reload_callback_handle
        if (reload_callback_handle is None):
            self._reload_callback_handle = KOKORO.call_later(AUTO_RELOAD_DELAY, self._reload_callback)
    
    
    def _reload_callback(self):
        """
        Invokes ``._do_reload`` if no new events were triggered since last scheduling.
        If there were events triggered then reschedules itself.
        """
        next = self._updated_plugins_at + AUTO_RELOAD_DELAY
        if next > LOOP_TIME() or self._reload_task_active:
            self._reload_callback_handle = KOKORO.call_at(AUTO_RELOAD_DELAY, self._reload_callback)
            return
        
        self._reload_callback_handle = None
        Task(KOKORO, self._do_reload())
    
    
    async def _do_reload(self):
        """
        Keeps reloading plugins till there are new plugins to reload.
        
        This method is a generator.
        """
        if self._reload_task_active:
            return
        
        self._reload_task_active = True
        try:
            while True:
                self_updated_plugins = self._updated_plugins
                if not self_updated_plugins:
                    return
                
                updated_plugins = self_updated_plugins.copy()
                self_updated_plugins.clear()
                
                try:
                    await reload_plugin(updated_plugins)
                except GeneratorExit:
                    raise
                
                except PluginError as err:
                    await write_exception_async(err, filter = frame_filter)
                    
                except BaseException as err:
                    await write_exception_async(err)
                    return
        
        finally:
            self._reload_task_active = False


PLUGIN_AUTO_RELOADER_MANAGER = PluginAutoReloaderManager()
