__all__ = ('EXTENSIONS', )

import sys
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from importlib import reload as reload_module

from ...backend.utils import HybridValueDictionary, WeakValueDictionary
from ...backend.export import include

from .snapshot import take_snapshot, calculate_snapshot_difference, revert_snapshot
from .utils import _validate_entry_or_exit, PROTECTED_NAMES, _get_path_extension_name
from .exceptions import DoNotLoadExtension

EXTENSION_LOADER = include('EXTENSION_LOADER')

EXTENSIONS = WeakValueDictionary()

EXTENSION_STATE_UNDEFINED = 0
EXTENSION_STATE_LOADED = 1
EXTENSION_STATE_UNLOADED = 2
EXTENSION_STATE_UNSATISFIED = 3

EXTENSION_STATE_VALUE_TO_NAME = {
    EXTENSION_STATE_UNDEFINED: 'undefined',
    EXTENSION_STATE_LOADED: 'loaded',
    EXTENSION_STATE_UNLOADED: 'unloaded',
    EXTENSION_STATE_UNSATISFIED: 'unsatisfied',
}

class Extension:
    """
    Represents an extension.
    
    Attributes
    ----------
    _added_variable_names : `list of `str`
        A list of the added variables' names to the module.
    _default_variables : `None` or `HybridValueDictionary` of (`str`, `Any`) items
        An optionally weak value dictionary to store objects for assigning them to modules before loading them.
        If it would be set as empty, then it is set as `None` instead.
    _entry_point : `None`, `str`, or `callable`
        Internal slot used by the ``.entry_point`` property.
    _exit_point : `None`, `str`, or `callable`
        Internal slot used by the ``.exit_point`` property.
    _extend_default_variables : `bool`
        Internal slot used by the ``.extend_default_variables`` property.
    _lib : `None` or module`
        The extension's module. Set as `module` object if it the extension was already loaded.
    _locked : `bool`
        The internal slot used for the ``.locked`` property.
    _snapshot_difference : `None` or `list` of `tuple` (``Client``, `list` of `tuple` (`str`, `Any`))
        Snapshot difference if applicable. Defaults to `None`.
    _spec : `ModuleSpec`
        The module specification for the extension's module's import system related state.
    _state : `int`
        The state of the extension. Can be:
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | EXTENSION_STATE_UNDEFINED     | 0     |
        +-------------------------------+-------+
        | EXTENSION_STATE_LOADED        | 1     |
        +-------------------------------+-------+
        | EXTENSION_STATE_UNLOADED      | 2     |
        +-------------------------------+-------+
        | EXTENSION_STATE_UNSATISFIED   | 3     |
        +-------------------------------+-------+
    _take_snapshot : `bool`
        Whether snapshot difference should be taken.
    """
    __slots__ = ('__weakref__', '_added_variable_names', '_default_variables', '_entry_point', '_exit_point',
        '_extend_default_variables', '_lib', '_locked', '_snapshot_difference', '_spec', '_state',
        '_take_snapshot', )
    
    def __new__(cls, name, path, entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference,
            default_variables, ):
        """
        Creates an extension with the given parameters. If an extension already exists with the given name, returns
        that.
        
        Parameters
        ----------
        name : `None` or `str`
            The extension's name (or import path).
        path : `str`
            Path to the extension file.
        entry_point : `None`, `str` or `callable`
            The entry point of the extension.
        exit_point : `None`, `str` or `callable`
            The exit point of the extension.
        extend_default_variables : `bool`
            Whether the extension should use the loader's default variables or just it's own's.
        locked : `bool`
            Whether the extension should be picked up by the `{}_all` methods of the extension loader.
        take_snapshot_difference: `bool`
            Whether snapshots should be taken before and after loading an extension, and when the extension is unloaded,
            the snapshot difference should be reverted.
        default_variables : `None` or `HybridValueDictionary` of (`str`, `Any`) items
            An optionally weak value dictionary to store objects for assigning them to modules before loading them.
            If would be empty, is set as `None` instead.
        
        Returns
        -------
        self : ``Extension``
        
        Raises
        ------
        ModuleNotFoundError
            If the extension was not found.
        """
        if (name is None):
            name = _get_path_extension_name(path)
            
            from_path = True
        else:
            from_path = False
        
        try:
            return EXTENSIONS[name]
        except KeyError:
            pass
        
        if from_path:
            spec = spec_from_file_location(name, path)
        else:
            spec = find_spec(name)
        
        if spec is None:
            raise ModuleNotFoundError(name)
        
        self = object.__new__(cls)
        self._state = EXTENSION_STATE_UNDEFINED
        self._spec = spec
        self._lib = None
        self._entry_point = entry_point
        self._exit_point = exit_point
        self._extend_default_variables = extend_default_variables
        self._locked = locked
        self._default_variables = default_variables
        self._added_variable_names = []
        self._take_snapshot = take_snapshot_difference
        self._snapshot_difference = None
        
        EXTENSIONS[name] = self
        
        return self
    
    
    def __hash__(self):
        """Returns the extension's ``._spec``'s `.origin`'s hash."""
        return hash(self._spec.origin)
    
    
    def __repr__(self):
        """Returns the extension's representation."""
        repr_parts = []
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        repr_parts.append(' name=')
        repr_parts.append(repr(self._spec.name))
        
        state = self._state
        repr_parts.append(', state=')
        state_name = EXTENSION_STATE_VALUE_TO_NAME.get(state, '???')
        repr_parts.append(state_name)
        repr_parts.append(' (')
        repr_parts.append(repr(state))
        repr_parts.append(')')
        
        if self._locked:
            repr_parts.append(', locked=True')
        
        default_variables = self._default_variables
        if self._extend_default_variables:
            if (default_variables is not None):
                repr_parts.append(' extends loader\'s defaults with: ')
                repr_parts.append(repr(default_variables))
        else:
            if default_variables is None:
                repr_parts.append(' clears loader\'s defaults')
            else:
                repr_parts.append(' clears loader\'s defaults and uses: ')
                repr_parts.append(repr(default_variables))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def add_default_variables(self, **variables):
        """
        Adds default variables to the extension.
        
        Parameters
        ----------
        **variables : Keyword Parameters
            Variables to assigned to the extension's module before it is loaded.
        
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
                raise ValueError(f'The passed {key!r} is a protected variable name of module type.')
            default_variables[key] = value
    
    
    def remove_default_variables(self, *names):
        """
        Removes the mentioned default variables of the extension.
        
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
        Removes all the default variables of the extension.
        """
        self._default_variables = None
    
    
    @property
    def entry_point(self):
        """
        Get-set-del descriptor for modifying the extension's entry point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """
        return self._entry_point
    
    
    @entry_point.setter
    def entry_point(self, entry_point):
        if not _validate_entry_or_exit(entry_point):
            raise TypeError(f'`{self.__class__.__name__}.entry_point` expected `None`, `str` or a `callable`, got '
                f'{entry_point.__class__.__name__}.')
        
        self._entry_point = entry_point
    
    @entry_point.deleter
    def entry_point(self):
        self._entry_point = None
    
    
    @property
    def exit_point(self):
        """
        Get-set-del descriptor for modifying the extension's exit point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """
        return self._exit_point
    
    @exit_point.setter
    def exit_point(self, exit_point):
        if not _validate_entry_or_exit(exit_point):
            raise TypeError(f'`{self.__class__.__name__}.exit_point` expected `None`, `str` or a `callable`, got '
                f'{exit_point.__class__.__name__}.')
        
        self._exit_point = exit_point
    
    @exit_point.deleter
    def exit_point(self):
        self._exit_point = None
    
    
    @property
    def extend_default_variables(self):
        """
        Get-set descriptor to define whether the extension uses the loader's default variables or just it's own's.
        
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
            raise TypeError(f'`extend_default_variables` should have been passed as `bool`, got '
                f'{extend_default_variables_type.__name__}.')
        
        self._extend_default_variables = extend_default_variables
    
    @property
    def locked(self):
        """
        Get-set property to define whether the extension should be picked up by the `{}_all` methods of the
        extension loader.
        
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
            raise TypeError(f'`locked` should have been passed as `bool`, got: {locked_type.__name__}.')
        
        self._locked = locked
    
    
    def _load(self):
        """
        Loads the module and returns it. If it is already loaded returns `None`.
        
        Returns
        -------
        lib : `None` or `lib`
        """
        state = self._state
        if state == EXTENSION_STATE_UNDEFINED:
            
            spec = self._spec
            lib = sys.modules.get(spec.name, None)
            if lib is None:
                # lib is not imported yet, nice
                lib = module_from_spec(spec)
                
                added_variable_names = self._added_variable_names
                if self._extend_default_variables:
                    for name, value in EXTENSION_LOADER._default_variables.items():
                        setattr(lib, name, value)
                        added_variable_names.append(name)
                
                default_variables = self._default_variables
                if (default_variables is not None):
                    for name, value in default_variables.items():
                        setattr(lib, name, value)
                        added_variable_names.append(name)
                
                if self._take_snapshot:
                    snapshot_old = take_snapshot()
                
                try:
                    spec.loader.exec_module(lib)
                except DoNotLoadExtension:
                    loaded = False
                else:
                    loaded = True
                
                sys.modules[spec.name] = lib
                
                if loaded:
                    if self._take_snapshot:
                        snapshot_new = take_snapshot()
                        
                        self._snapshot_difference = calculate_snapshot_difference(snapshot_old, snapshot_new)
            
            else:
                loaded = True
            
            self._lib = lib
            
            if loaded:
                state = EXTENSION_STATE_LOADED
            else:
                state = EXTENSION_STATE_UNSATISFIED
                lib = None
            
            self._state = state
            return lib
        
        if state == EXTENSION_STATE_LOADED:
            # return None -> already loaded
            return None
        
        if state in (EXTENSION_STATE_UNLOADED, EXTENSION_STATE_UNSATISFIED):
            # reload
            lib = self._lib
            
            added_variable_names = self._added_variable_names
            if self._extend_default_variables:
                for name, value in EXTENSION_LOADER._default_variables.items():
                    setattr(lib, name, value)
                    added_variable_names.append(name)
            
            default_variables = self._default_variables
            if (default_variables is not None):
                for name, value in default_variables.items():
                    setattr(lib, name, value)
                    added_variable_names.append(name)
            
            if self._take_snapshot:
                snapshot_old = take_snapshot()
            
            try:
                reload_module(lib)
            except DoNotLoadExtension:
                loaded = False
            else:
                loaded = True
            
            if loaded:
                if self._take_snapshot:
                    snapshot_new = take_snapshot()
                    
                    self._snapshot_difference = calculate_snapshot_difference(snapshot_old, snapshot_new)
            
            if loaded:
                state = EXTENSION_STATE_LOADED
            else:
                state = EXTENSION_STATE_UNSATISFIED
                lib = None
            
            self._state = state
            
            return lib
        
        return None
        # no more cases
    
    def _unload(self):
        """
        Unloads the module and returns it. If it is already unloaded returns `None`.
        
        Returns
        -------
        lib : `None` or `lib`
        """
        state = self._state
        if state == EXTENSION_STATE_UNDEFINED:
            return None
        
        if state == EXTENSION_STATE_LOADED:
            
            snapshot_difference = self._snapshot_difference
            if (snapshot_difference is not None):
                self._snapshot_difference = None
                revert_snapshot(snapshot_difference)
            
            self._state = EXTENSION_STATE_UNLOADED
            return self._lib
        
        if state in (EXTENSION_STATE_UNLOADED, EXTENSION_STATE_UNSATISFIED):
            return None
        
        # no more cases
    
    def _unassign_variables(self):
        """
        Unassigns the assigned variables to the respective module and clears ``._added_variable_names``.
        """
        lib = self._lib
        if lib is None:
            return
        
        added_variable_names = self._added_variable_names
        for name in added_variable_names:
            try:
                delattr(lib, name)
            except AttributeError:
                pass
        added_variable_names.clear()
    
    @property
    def name(self):
        """
        Returns the extension's name.
        
        Returns
        -------
        name : `str`
        """
        return self._spec.name
    
    @property
    def short_name(self):
        """
        Returns the extension's name's shortened version.
        
        Returns
        -------
        name : `str`
        """
        name = self._spec.name
        dot_index = name.rfind('.')
        if dot_index == -1:
            short_name = None
        else:
            short_name = name[dot_index+1:]
        
        return short_name
    
    
    def is_loaded(self):
        """
        Returns whether the extension is loaded.
        
        Returns
        -------
        is_loaded : `bool`
        """
        return (self._state == EXTENSION_STATE_LOADED)
    
   
    def is_unsatisfied(self):
        """
        Returns whether the extension is unsatisfied.
        
        Returns
        -------
        is_unsatisfied : `bool`
        """
        return (self._state == EXTENSION_STATE_UNSATISFIED)
    
    
    def _unlink(self):
        """
        Removes the extension's module from the loaded ones.
        
        Should not be called on loaded extensions.
        """
        state = self._state
        if state == EXTENSION_STATE_UNDEFINED:
            return
        
        if state == EXTENSION_STATE_LOADED:
            self._state = EXTENSION_STATE_UNLOADED
            lib = self._lib
            
            if self._extend_default_variables:
                for name in EXTENSION_LOADER._default_variables:
                    try:
                        delattr(lib, name)
                    except AttributeError:
                        pass
            
            default_variables = self._default_variables
            if (default_variables is not None):
                for name in default_variables:
                    delattr(lib, name)
            
            try:
                del sys.modules[self._spec.name]
            except KeyError:
                pass
            return
        
        if state in (EXTENSION_STATE_UNLOADED, EXTENSION_STATE_UNSATISFIED):
            try:
                del sys.modules[self._spec.name]
            except KeyError:
                pass
            return
        
        # no more cases
