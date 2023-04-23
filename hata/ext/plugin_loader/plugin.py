__all__ = ()

import sys, warnings
from importlib.util import module_from_spec, spec_from_file_location
from os.path import basename as get_file_name, splitext as split_file_name_and_extension
from py_compile import PyCompileError, compile as compile_module

from scarletio import HybridValueDictionary, RichAttributeErrorBaseType, WeakSet, include

from .constants import (
    IN_DIRECTORY_PLUGIN_RP, LOADING_PLUGINS, PLUGINS, PLUGIN_ACTION_FLAG_SYNTAX_CHECK, PLUGIN_STATE_LOADED,
    PLUGIN_STATE_UNDEFINED, PLUGIN_STATE_UNLOADED, PLUGIN_STATE_UNSATISFIED, PLUGIN_STATE_VALUE_TO_NAME
)
from .exceptions import DoNotLoadPlugin, PluginError
from .helpers import PROTECTED_NAMES, _get_path_plugin_name, _validate_entry_or_exit
from .import_overwrite.module_proxy_type import PluginModuleProxyType
from .import_overwrite.module_spec_type import PluginModuleSpecType
from .plugin_root import register_plugin_root
from .snapshot import calculate_snapshot_difference, revert_snapshot, take_snapshot


PLUGIN_LOADER = include('PLUGIN_LOADER')


class Plugin(RichAttributeErrorBaseType):
    """
    Represents an plugin.
    
    Attributes
    ----------
    _added_variable_names : `list of `str`
        A list of the added variables' names to the module.
    _child_plugins : `None`, ``WeakSet`` of ``Plugin``
        Child plugins.
    _default_variables : `None`, `HybridValueDictionary` of (`str`, `Any`) items
        An optionally weak value dictionary to store objects for assigning them to modules before loading them.
        If it would be set as empty, then it is set as `None` instead.
    _entry_point : `None`, `str`, `callable`
        Internal slot used by the ``.entry_point`` property.
    _exit_point : `None`, `str`, `callable`
        Internal slot used by the ``.exit_point`` property.
    _extend_default_variables : `bool`
        Internal slot used by the ``.extend_default_variables`` property.
    _locked : `bool`
        The internal slot used for the ``.locked`` property.
    _parent_plugins : `None`, ``WeakSet`` of ``Plugin``
        Parent plugins.
    _snapshot_difference : `None`, `list` of ``BaseSnapshotType``
        Snapshot difference if applicable. Defaults to `None`.
    _snapshot_extractions : `None`, `list` of `list` of ``BaseSnapshotType``
        Additional snapshots to extract from own.
    _spec : ``PluginModuleSpecType``
        The module specification for the plugin's module's import system related state.
    _state : `int`
        The state of the plugin. Can be:
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | PLUGIN_STATE_UNDEFINED        | 0     |
        +-------------------------------+-------+
        | PLUGIN_STATE_LOADED           | 1     |
        +-------------------------------+-------+
        | PLUGIN_STATE_UNLOADED         | 2     |
        +-------------------------------+-------+
        | PLUGIN_STATE_UNSATISFIED      | 3     |
        +-------------------------------+-------+
    _sub_module_plugins : `None`, ``WeakSet`` of ``Plugin``
        Sub module plugins.
    _take_snapshot : `bool`
        Whether snapshot difference should be taken.
    """
    __slots__ = (
        '__weakref__', '_added_variable_names', '_child_plugins', '_default_variables', '_entry_point',
        '_exit_point', '_extend_default_variables', '_locked', '_parent_plugins', '_snapshot_difference',
        '_snapshot_extractions', '_spec', '_state', '_sub_module_plugins', '_take_snapshot'
    )
    
    def __new__(
        cls, name, path, entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference,
        default_variables
    ):
        """
        Creates an plugin with the given parameters. If an plugin already exists with the given name, returns
        that.
        
        Parameters
        ----------
        name : `None`, `str`
            The plugin's name (or import path).
        path : `str`
            Path to the plugin file.
        entry_point : `None`, `str`, `callable`
            The entry point of the plugin.
        exit_point : `None`, `str`, `callable`
            The exit point of the plugin.
        extend_default_variables : `bool`
            Whether the plugin should use the loader's default variables or just it's own.
        locked : `bool`
            Whether the plugin should be picked up by the `{}_all` methods of the plugin loader.
        take_snapshot_difference: `bool`
            Whether snapshots should be taken before and after loading an plugin, and when the plugin is unloaded,
            the snapshot difference should be reverted.
        default_variables : `None`, `HybridValueDictionary` of (`str`, `Any`) items
            An optionally weak value dictionary to store objects for assigning them to modules before loading them.
            If would be empty, is set as `None` instead.
        
        Returns
        -------
        self : ``Plugin``
        
        Raises
        ------
        ModuleNotFoundError
            If the plugin was not found.
        """
        if (name is None):
            name = _get_path_plugin_name(path)
        
        try:
            self = PLUGINS[name]
        except KeyError:
            pass
        else:
            if (default_variables is not None):
                self.add_default_variables(**default_variables)
            
            return self
        
        spec = spec_from_file_location(name, path)
        if spec is None:
            raise ModuleNotFoundError(name)
        
        spec = PluginModuleSpecType(spec)
        register_plugin_root(name)
        
        self = object.__new__(cls)
        self._added_variable_names = []
        self._child_plugins = None
        self._parent_plugins = None
        self._default_variables = default_variables
        self._entry_point = entry_point
        self._exit_point = exit_point
        self._extend_default_variables = extend_default_variables
        self._locked = locked
        self._snapshot_difference = None
        self._snapshot_extractions = None
        self._spec = spec
        self._state = PLUGIN_STATE_UNDEFINED
        self._sub_module_plugins = None
        self._take_snapshot = take_snapshot_difference
        
        PLUGINS[name] = self
        
        return self
    
    
    def __hash__(self):
        """Returns the plugin's ``._spec``'s `.origin`'s hash."""
        return hash(self._spec.origin)
    
    
    def __repr__(self):
        """Returns the plugin's representation."""
        repr_parts = []
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        repr_parts.append(' name = ')
        repr_parts.append(repr(self._spec.name))
        
        state = self._state
        repr_parts.append(', state = ')
        state_name = PLUGIN_STATE_VALUE_TO_NAME.get(state, '???')
        repr_parts.append(state_name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(state))
        
        if self._locked:
            repr_parts.append(', locked = True')
        
        default_variables = self._default_variables
        if self._extend_default_variables:
            if (default_variables is not None):
                repr_parts.append(' extends defaults with: ')
                repr_parts.append(repr(default_variables))
        else:
            if default_variables is None:
                repr_parts.append(' clears defaults')
            else:
                repr_parts.append(' clears defaults and uses: ')
                repr_parts.append(repr(default_variables))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.sort_key > other.sort_key
    
    
    def __lt__(self, other):
        """Returns whether self is less than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.sort_key < other.sort_key
    
    
    def add_default_variables(self, **variables):
        """
        Adds default variables to the plugin.
        
        Parameters
        ----------
        **variables : Keyword Parameters
            Variables to assigned to the plugin's module before it is loaded.
        
        Raises
        ------
        ValueError
             If a variable name is would be used, what is `module` attribute.
        """
        if not variables:
            return
        
        default_variables = self._default_variables
        if default_variables is None:
            default_variables = HybridValueDictionary()
            self._default_variables = default_variables
        
        for key, value in variables.items():
            if key in PROTECTED_NAMES:
                raise ValueError(
                    f'The passed {key!r} is a protected variable name of module type.'
                )
            default_variables[key] = value
    
    
    def remove_default_variables(self, *names):
        """
        Removes the mentioned default variables of the plugin.
        
        If a variable with a specified name is not found, no error is raised.
        
        Parameters
        ----------
        *names : `str`
            Default variable names.
        """
        default_variables = self._default_variables
        if default_variables is None:
            return
        
        for name in names:
            try:
                del default_variables[name]
            except KeyError:
                pass
        
        if default_variables:
            return
        
        self._default_variables = None
    
    
    def clear_default_variables(self):
        """
        Removes all the default variables of the plugin.
        """
        self._default_variables = None
    
    
    @property
    def entry_point(self):
        """
        Get-set-del descriptor for modifying the plugin's entry point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """
        return self._entry_point
    
    
    @entry_point.setter
    def entry_point(self, entry_point):
        if not _validate_entry_or_exit(entry_point):
            raise TypeError(
                f'`{self.__class__.__name__}.entry_point` can be `None`, `str`, `callable`, got '
                f'{entry_point.__class__.__name__}; {entry_point!r}.'
            )
        
        self._entry_point = entry_point
    
    
    @entry_point.deleter
    def entry_point(self):
        self._entry_point = None
    
    
    @property
    def exit_point(self):
        """
        Get-set-del descriptor for modifying the plugin's exit point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """
        return self._exit_point
    
    @exit_point.setter
    def exit_point(self, exit_point):
        if not _validate_entry_or_exit(exit_point):
            raise TypeError(
                f'`{self.__class__.__name__}.exit_point` can be `None`, `str`, `callable`, got '
                f'{exit_point.__class__.__name__}; {exit_point!r}.'
            )
        
        self._exit_point = exit_point
    
    @exit_point.deleter
    def exit_point(self):
        self._exit_point = None
    
    
    @property
    def extend_default_variables(self):
        """
        Get-set descriptor to define whether the plugin uses the loader's default variables or just it's own.
        
        Accepts and returns `bool`.
        """
        return self._extend_default_variables
    
    
    @extend_default_variables.setter
    def extend_default_variables(self, extend_default_variables):
        extend_default_variables_type = extend_default_variables.__class__
        if extend_default_variables_type is bool:
            pass
        elif issubclass(extend_default_variables_type, int):
            extend_default_variables = bool(extend_default_variables)
        else:
            raise TypeError(
                f'`extend_default_variables` can be `bool`, got '
                f'{extend_default_variables_type.__name__}; {extend_default_variables!r}.'
            )
        
        self._extend_default_variables = extend_default_variables
    
    
    @property
    def locked(self):
        """
        Get-set property to define whether the plugin should be picked up by the `{}_all` methods of the
        plugin loader.
        
        Accepts and returns `bool`.
        """
        return self._locked
    
    
    @locked.setter
    def locked(self, locked):
        locked_type = locked.__class__
        if locked_type is bool:
            pass
        elif issubclass(locked_type, int):
            locked = bool(locked)
        else:
            raise TypeError(
                f'`locked` can be `bool`, got {locked_type.__name__}; {locked!r}.'
            )
        
        self._locked = locked
    
    
    def _load(self):
        """
        Loads the module and returns it. If it is already loaded returns `None`.
        
        Returns
        -------
        module : `None`, `ModuleType`
        
        Raises
        ------
        ImportError
            Circular imports.
        RuntimeError
            Module already imported.
        BaseException
            Any exception raised from the plugin file.
        """
        if self in LOADING_PLUGINS:
            raise ImportError(
                f'{self.name} is already being loaded. This can happen if there are circular imports. The following '
                f'plugins are being loaded right now: '
                f'{", ".join(plugin.name for plugin in LOADING_PLUGINS)}'
            )
        
        try:
            LOADING_PLUGINS.add(self)
            state = self._state
            if state == PLUGIN_STATE_UNDEFINED:
                
                spec = self._spec
                
                maybe_proxy_module = sys.modules.get(spec.name, None)
                if (maybe_proxy_module is not None) and (not isinstance(maybe_proxy_module, PluginModuleProxyType)):
                    raise RuntimeError(
                        f'Module `{spec.name}` is already imported.'
                    )
                
                module = spec.get_module()
                
                if (module is None):
                    module_from_spec(spec)
                    
                    module = spec.get_module()
                    loaded = self._load_module()
                
                else:
                    loaded = True
                
                if loaded:
                    state = PLUGIN_STATE_LOADED
                else:
                    state = PLUGIN_STATE_UNSATISFIED
                    module = None
                
                self._state = state
                return module
            
            if state == PLUGIN_STATE_LOADED:
                # return None -> already loaded
                return None
            
            if state in (PLUGIN_STATE_UNLOADED, PLUGIN_STATE_UNSATISFIED):
                # reload
                module_from_spec(self._spec)
                loaded = self._load_module()
                
                if loaded:
                    state = PLUGIN_STATE_LOADED
                    module =  self._spec.get_module()
                else:
                    state = PLUGIN_STATE_UNSATISFIED
                    module = None
                
                self._state = state
                
                return module
            
            return None
            # no more cases
        
        finally:
            LOADING_PLUGINS.discard(self)
    
    
    def _load_module(self):
        """
        Loads the module and returns whether it was successfully loaded.
        
        Returns
        -------
        loaded : `bool`
        
        Raises
        ------
        BaseException
            Any exception raised from the plugin file.
        """
        spec = self._spec
        module = spec.get_module()
        
        added_variable_names = self._added_variable_names
        if self._extend_default_variables:
            for name, value in PLUGIN_LOADER._default_variables.items():
                setattr(module, name, value)
                added_variable_names.append(name)
        
        default_variables = self._default_variables
        if (default_variables is not None):
            for name, value in default_variables.items():
                setattr(module, name, value)
                added_variable_names.append(name)
        
        for plugin in self.iter_loaded_plugins_in_directory():
            setattr(module, plugin.short_name, plugin.get_module_proxy())
        
        active_plugins_at_start = LOADING_PLUGINS.copy()
        
        if self._take_snapshot:
            snapshot_old = take_snapshot()
        else:
            snapshot_old = None
        
        try:
            spec.loader.exec_module(module)
        except DoNotLoadPlugin:
            loaded = False
        else:
            loaded = True
        
        if loaded:
            active_plugins_at_end = LOADING_PLUGINS.copy()
            plugin_intersection = active_plugins_at_start & active_plugins_at_end
            plugin_intersection.discard(self)
            
            if (snapshot_old is not None):
                snapshot_new = take_snapshot()
                snapshot_difference = calculate_snapshot_difference(snapshot_new, snapshot_old)
                
                for snapshot_extraction in self.iter_snapshot_extractions():
                    snapshot_difference = calculate_snapshot_difference(
                        snapshot_difference, snapshot_extraction
                    )
                
                self.clear_snapshot_extractions()
                
                self._snapshot_difference = snapshot_difference
                
                for plugin in plugin_intersection:
                    plugin.add_snapshot_extraction(snapshot_difference)
            
            else:
                for snapshot_extraction in self.iter_snapshot_extractions():
                    for plugin in plugin_intersection:
                        plugin.add_snapshot_extraction(snapshot_extraction)
                
                self.clear_snapshot_extractions()
        
        return loaded
    
    
    def _check_for_syntax(self):
        """
        Checks the file's new syntax.
        
        Used when reloading, to avoid unloading un-loadable files.
        
        This method is blocking. Run it inside of an executor.
        
        Returns
        -------
        exception : PluginError
            PluginError wrapping invalid syntax.
        """
        if (self._state == PLUGIN_STATE_LOADED) and self._spec.is_initialised():
            file_name = self.file_name
            # python files might not be `.py` files, which we should not compile.
            if file_name.endswith('.py'):
                try:
                    compile_module(file_name, doraise = True)
                except FileNotFoundError:
                    # If the file is deleted, is fine.
                    pass
                
                except FileExistsError:
                    pass
                
                except PyCompileError as err:
                    exception_value = err.exc_value
                    if isinstance(exception_value, SyntaxError):
                        cause = exception_value
                    else:
                        cause = err
                    
                    try:
                        raise PluginError(action = PLUGIN_ACTION_FLAG_SYNTAX_CHECK, cause = cause, plugin = self)
                    finally:
                        cause = None
    
    
    def _unload(self):
        """
        Unloads the module and returns it. If it is already unloaded returns `None`.
        
        Returns
        -------
        module : `None`, `ModuleType`
        
        Raises
        ------
        SyntaxError
            If `check_for_syntax` and the file's syntax is incorrect.
        """
        state = self._state
        if state == PLUGIN_STATE_UNDEFINED:
            return None
        
        if state == PLUGIN_STATE_LOADED:
            self.clear_child_plugins()
            self.clear_parent_plugins()
            
            snapshot_difference = self._snapshot_difference
            if (snapshot_difference is not None):
                self._snapshot_difference = None
                revert_snapshot(snapshot_difference)
            
            self._state = PLUGIN_STATE_UNLOADED
            
            spec = self._spec
            try:
                del sys.modules[spec.name]
            except KeyError:
                pass
            
            return spec.get_module()
        
        if state in (PLUGIN_STATE_UNLOADED, PLUGIN_STATE_UNSATISFIED):
            return None
        
        # no more cases
    
    def _unassign_variables(self):
        """
        Unassigns the assigned variables to the respective module and clears ``._added_variable_names``.
        """
        module = self._spec.get_module()
        if module is None:
            return
        
        added_variable_names = self._added_variable_names
        for name in added_variable_names:
            try:
                delattr(module, name)
            except AttributeError:
                pass
        
        added_variable_names.clear()
    
    
    @property
    def name(self):
        """
        Returns the plugin's name.
        
        Returns
        -------
        name : `str`
        """
        return self._spec.name
    
    
    @property
    def path(self):
        """
        Returns the plugin's name.
        
        Returns
        -------
        name : `str`
        """
        return self._spec.origin
    
    
    @property
    def short_name(self):
        """
        Returns the plugin's name's shortened version.
        
        Returns
        -------
        name : `str`
        """
        name = self._spec.name
        dot_index = name.rfind('.')
        if dot_index == -1:
            short_name = None
        else:
            short_name = name[dot_index + 1:]
        
        return short_name
    
    
    @property
    def file_name(self):
        """
        Returns the plugin's file's name.
        
        Returns
        -------
        file_name : `str`
        """
        return self._spec.origin
    
    
    @property
    def sort_key(self):
        """
        Returns the plugin's sort key.
        
        Returns
        -------
        sort_key : `tuple` of `str`
        """
        return self._spec.name.split('.')
    
    
    def is_loaded(self):
        """
        Returns whether the plugin is loaded.
        
        Returns
        -------
        is_loaded : `bool`
        """
        return (self._state == PLUGIN_STATE_LOADED)
    
   
    def is_unsatisfied(self):
        """
        Returns whether the plugin is unsatisfied.
        
        Returns
        -------
        is_unsatisfied : `bool`
        """
        return (self._state == PLUGIN_STATE_UNSATISFIED)
    
    
    def _unlink(self):
        """
        Removes the plugin's module from the loaded ones.
        
        Should not be called on loaded plugins.
        """
        state = self._state
        if state == PLUGIN_STATE_UNDEFINED:
            pass
        
        elif state == PLUGIN_STATE_LOADED:
            self._state = PLUGIN_STATE_UNLOADED
            module = self._spec.get_module()
            
            if self._extend_default_variables:
                for name in PLUGIN_LOADER._default_variables:
                    try:
                        delattr(module, name)
                    except AttributeError:
                        pass
            
            default_variables = self._default_variables
            if (default_variables is not None):
                for name in default_variables:
                    delattr(module, name)
            
            try:
                del sys.modules[self._spec.name]
            except KeyError:
                pass
        
        elif state in (PLUGIN_STATE_UNLOADED, PLUGIN_STATE_UNSATISFIED):
            try:
                del sys.modules[self._spec.name]
            except KeyError:
                pass
        
        # no more cases
        
        plugins_by_name = PLUGIN_LOADER._plugins_by_name
        for name in (self.name, self.short_name, self.path):
            if plugins_by_name.get(name, None) is self:
                try:
                    del plugins_by_name[name]
                except KeyError:
                    pass
    
    
    def add_child_plugin(self, plugin):
        """
        Registers a child plugin.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to register.
        """
        if plugin is self:
            return
        
        child_plugins = self._child_plugins
        if (child_plugins is None):
            child_plugins = WeakSet()
            self._child_plugins = child_plugins
        
        child_plugins.add(plugin)
    
    
    def iter_child_plugins(self):
        """
        Iterates over the child plugins.
        
        This method is an iterable generator.
        
        Yields
        ------
        child_plugin : `None`
        """
        child_plugins = self._child_plugins
        if (child_plugins is not None):
            yield from child_plugins
    
    
    def are_child_plugins_present_in(self, plugins):
        """
        Returns whether all the child plugins are present in the given `plugins`.
        
        Parameters
        ----------
        plugins : `iterable` of ``Plugin``
            Already present plugins to check satisfaction form.
        
        Returns
        -------
        are_child_plugins_present_in : `bool`
        """
        child_plugins = self._child_plugins
        if (child_plugins is None):
            return True
        
        if child_plugins <= plugins:
            return True
        
        return False
    
    
    def clear_child_plugins(self):
        """
        Clears the child plugins of the plugin.
        """
        child_plugins = self._child_plugins
        if (child_plugins is not None):
            self._child_plugins = None
            
            for child_plugin in child_plugins:
                child_plugin.remove_parent_plugin(self)
    
    
    def remove_child_plugin(self, child_plugin):
        """
        Removes the given plugin from the plugin's children.
        
        Parameters
        ----------
        child_plugin : ``Plugin``
            The plugin to remove.
        """
        child_plugins = self._child_plugins
        if (child_plugins is not None):
            try:
                child_plugins.remove(child_plugin)
            except KeyError:
                pass
            else:
                if not child_plugins:
                    self._child_plugins = child_plugins
    
    
    def add_snapshot_extraction(self, snapshots):
        """
        Adds snapshot extraction to the plugin.
        
        Parameters
        ----------
        snapshots : `list` of ``BaseSnapshotType``
        """
        snapshot_extractions = self._snapshot_extractions
        if (snapshot_extractions is None):
            snapshot_extractions = []
            self._snapshot_extractions = snapshot_extractions
        
        snapshot_extractions.append(snapshots)
    
    
    def iter_snapshot_extractions(self):
        """
        Iterates over the snapshot extractions of the plugin.
        
        This method is an iterable generator.
        
        Yields
        ------
        snapshots : `list` of ``BaseSnapshotType``
        """
        snapshot_extractions = self._snapshot_extractions
        if (snapshot_extractions is not None):
            yield from snapshot_extractions
    
    
    def clear_snapshot_extractions(self):
        """
        Clears the snapshot extractions of the plugin.
        """
        self._snapshot_extractions = None
    
    
    def add_parent_plugin(self, plugin):
        """
        Registers a parent plugin.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to register.
        """
        if plugin is self:
            return
        
        parent_plugins = self._parent_plugins
        if (parent_plugins is None):
            parent_plugins = WeakSet()
            self._parent_plugins = parent_plugins
        
        parent_plugins.add(plugin)
    
    
    def iter_parent_plugins(self):
        """
        Iterates over the parent plugins.
        
        This method is an iterable generator.
        
        Yields
        ------
        parent_plugin : `None`
        """
        parent_plugins = self._parent_plugins
        if (parent_plugins is not None):
            yield from parent_plugins
    
    
    def are_parent_plugins_present_in(self, plugins):
        """
        Returns whether all the parent plugins are present in the given `plugins`.
        
        Parameters
        ----------
        plugins : `iterable` of ``Plugin``
            Already present plugins to check satisfaction form.
        
        Returns
        -------
        are_parent_plugins_present_in : `bool`
        """
        parent_plugins = self._parent_plugins
        if (parent_plugins is None):
            return True
        
        if parent_plugins <= plugins:
            return True
        
        return False
    
    
    def clear_parent_plugins(self):
        """
        Clears the parent plugins of the plugin.
        """
        parent_plugins = self._parent_plugins
        if (parent_plugins is not None):
            self._parent_plugins = parent_plugins
            
            for parent_plugin in parent_plugins:
                parent_plugin.remove_child_plugin(self)
    
    
    def remove_parent_plugin(self, parent_plugin):
        """
        Removes the given plugin from the plugin's parents.
        
        Parameters
        ----------
        parent_plugin : ``Plugin``
            The plugin to remove.
        """
        parent_plugins = self._parent_plugins
        if (parent_plugins is not None):
            try:
                parent_plugins.remove(parent_plugin)
            except KeyError:
                pass
            else:
                if not parent_plugins:
                    self._parent_plugins = parent_plugins
    
    
    @property
    def _module(self):
        """
        Deprecated attribute of ``Plugin``.
        """
        warnings.warn(
            f'`{self.__class__.__name__}._module` is deprecated, please use `.get_module()` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return self._spec.get_module()
    
    
    def get_module(self):
        """
        Returns the module of the plugin.
        
        Returns
        -------
        module : `None`, `ModuleType`
        """
        return self._spec.get_module()
    
    
    def get_module_proxy(self):
        """
        Returns a proxy to the plugin.
        
        Returns
        -------
        module_proxy : ``PluginModuleProxyType``
        """
        return self._spec.get_module_proxy()
    
    
    def is_directory(self):
        """
        Returns whether the plugin is a directory.
        
        Returns
        -------
        is_directory : `bool`
        """
        return split_file_name_and_extension(get_file_name(self._spec.origin))[0] == '__init__'
    
    
    def iter_loaded_plugins_in_directory(self):
        """
        Iterates over the loaded plugins directly under this one. This one must be a directory (so an `__init__` file).
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin : ``Plugin``
        """
        if not self.is_directory():
            return
        
        self_name = self.name
        for plugin in PLUGINS.values():
            if not plugin.is_loaded():
                continue
            
            other_name = plugin.name
            if not other_name.startswith(self_name):
                continue
            
            if IN_DIRECTORY_PLUGIN_RP.fullmatch(other_name[len(self_name):]) is None:
                continue
            
            yield plugin
    
    
    def add_sub_module_plugin(self, plugin):
        """
        Registers a sub module plugin.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to register.
        """
        if plugin is self:
            return
        
        sub_module_plugins = self._sub_module_plugins
        if (sub_module_plugins is None):
            sub_module_plugins = WeakSet()
            self._sub_module_plugins = sub_module_plugins
        
        sub_module_plugins.add(plugin)
    
    
    def iter_sub_module_plugins(self):
        """
        Iterates over the sub module plugins.
        
        This method is an iterable generator.
        
        Yields
        ------
        sub_module_plugin : `None`
        """
        sub_module_plugins = self._sub_module_plugins
        if (sub_module_plugins is not None):
            yield from sub_module_plugins
    
    
    def are_sub_module_plugins_present_in(self, plugins):
        """
        Returns whether all the sub module plugins are present in the given `plugins`.
        
        Parameters
        ----------
        plugins : `iterable` of ``Plugin``
            Already present plugins to check satisfaction form.
        
        Returns
        -------
        are_sub_module_plugins_present_in : `bool`
        """
        sub_module_plugins = self._sub_module_plugins
        if (sub_module_plugins is None):
            return True
        
        if sub_module_plugins <= plugins:
            return True
        
        return False
    
    
    def clear_sub_module_plugins(self):
        """
        Clears the sub module plugins of the plugin.
        """
        sub_module_plugins = self._sub_module_plugins
        if (sub_module_plugins is not None):
            self._sub_module_plugins = None
    
    
    def remove_sub_module_plugin(self, sub_module_plugin):
        """
        Removes the given plugin from the plugin's sub modules.
        
        Parameters
        ----------
        sub_module_plugin : ``Plugin``
            The plugin to remove.
        """
        sub_module_plugins = self._sub_module_plugins
        if (sub_module_plugins is not None):
            try:
                sub_module_plugins.remove(sub_module_plugin)
            except KeyError:
                pass
            else:
                if not sub_module_plugins:
                    self._sub_module_plugins = sub_module_plugins
