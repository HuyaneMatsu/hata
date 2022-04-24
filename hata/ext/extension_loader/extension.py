__all__ = ()

import sys, warnings
from importlib.util import module_from_spec, spec_from_file_location
from py_compile import compile as compile_module

from scarletio import HybridValueDictionary, RichAttributeErrorBaseType, WeakSet, include

from .constants import (
    EXTENSIONS, EXTENSION_STATE_LOADED, EXTENSION_STATE_UNDEFINED, EXTENSION_STATE_UNLOADED,
    EXTENSION_STATE_UNSATISFIED, EXTENSION_STATE_VALUE_TO_NAME, LOADING_EXTENSIONS
)
from .exceptions import DoNotLoadExtension
from .extension_root import register_extension_root
from .helpers import PROTECTED_NAMES, _get_path_extension_name, _validate_entry_or_exit
from .import_overwrite.module_spec_type import ExtensionModuleSpecType
from .import_overwrite.module_proxy_type import ExtensionModuleProxyType
from .snapshot import calculate_snapshot_difference, revert_snapshot, take_snapshot


EXTENSION_LOADER = include('EXTENSION_LOADER')


class Extension(RichAttributeErrorBaseType):
    """
    Represents an extension.
    
    Attributes
    ----------
    _added_variable_names : `list of `str`
        A list of the added variables' names to the module.
    _child_extensions : `None`, ``WeakSet`` of ``Extension``
        Child extensions.
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
    _parent_extensions : `None`, ``WeakSet`` of ``Extension``
        Parent extensions.
    _snapshot_difference : `None`, `list` of ``BaseSnapshotType``
        Snapshot difference if applicable. Defaults to `None`.
    _snapshot_extractions : `None`, `list` of `list` of ``BaseSnapshotType``
        Additional snapshots to extract from own.
    _spec : ``ExtensionModuleSpecType``
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
    __slots__ = (
        '__weakref__', '_added_variable_names', '_child_extensions', '_default_variables', '_entry_point',
        '_exit_point', '_extend_default_variables', '_locked', '_parent_extensions', '_snapshot_difference',
        '_snapshot_extractions', '_spec', '_state', '_take_snapshot'
    )
    
    def __new__(cls, name, path, entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference,
            default_variables, ):
        """
        Creates an extension with the given parameters. If an extension already exists with the given name, returns
        that.
        
        Parameters
        ----------
        name : `None`, `str`
            The extension's name (or import path).
        path : `str`
            Path to the extension file.
        entry_point : `None`, `str`, `callable`
            The entry point of the extension.
        exit_point : `None`, `str`, `callable`
            The exit point of the extension.
        extend_default_variables : `bool`
            Whether the extension should use the loader's default variables or just it's own.
        locked : `bool`
            Whether the extension should be picked up by the `{}_all` methods of the extension loader.
        take_snapshot_difference: `bool`
            Whether snapshots should be taken before and after loading an extension, and when the extension is unloaded,
            the snapshot difference should be reverted.
        default_variables : `None`, `HybridValueDictionary` of (`str`, `Any`) items
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
        
        try:
            self = EXTENSIONS[name]
        except KeyError:
            pass
        else:
            if (default_variables is not None):
                self.add_default_variables(**default_variables)
            
            return self
        
        spec = spec_from_file_location(name, path)
        if spec is None:
            raise ModuleNotFoundError(name)
        
        spec = ExtensionModuleSpecType(spec)
        register_extension_root(name)
        
        self = object.__new__(cls)
        self._added_variable_names = []
        self._child_extensions = None
        self._parent_extensions = None
        self._default_variables = default_variables
        self._entry_point = entry_point
        self._exit_point = exit_point
        self._extend_default_variables = extend_default_variables
        self._locked = locked
        self._snapshot_difference = None
        self._snapshot_extractions = None
        self._spec = spec
        self._state = EXTENSION_STATE_UNDEFINED
        self._take_snapshot = take_snapshot_difference
        
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
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.name > other.name
    
    
    def __lt__(self, other):
        """Returns whether self is less than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.name < other.name
    
    
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
                raise ValueError(
                    f'The passed {key!r} is a protected variable name of module type.'
                )
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
        Get-set-del descriptor for modifying the extension's exit point.
        
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
        Get-set descriptor to define whether the extension uses the loader's default variables or just it's own.
        
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
            Any exception raised from the extension file.
        """
        if self in LOADING_EXTENSIONS:
            raise ImportError(
                f'{self.name} is already being loaded. This can happen if there are circular imports. The following '
                f'extensions are being loaded right now: '
                f'{", ".join(extension.name for extension in LOADING_EXTENSIONS)}'
            )
        
        try:
            LOADING_EXTENSIONS.add(self)
            state = self._state
            if state == EXTENSION_STATE_UNDEFINED:
                
                spec = self._spec
                
                maybe_proxy_module = sys.modules.get(spec.name, None)
                if (maybe_proxy_module is not None) and (not isinstance(maybe_proxy_module, ExtensionModuleProxyType)):
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
                    state = EXTENSION_STATE_LOADED
                else:
                    state = EXTENSION_STATE_UNSATISFIED
                    module = None
                
                self._state = state
                return module
            
            if state == EXTENSION_STATE_LOADED:
                # return None -> already loaded
                return None
            
            if state in (EXTENSION_STATE_UNLOADED, EXTENSION_STATE_UNSATISFIED):
                # reload
                module_from_spec(self._spec)
                loaded = self._load_module()
                
                if loaded:
                    state = EXTENSION_STATE_LOADED
                    module =  self._spec.get_module()
                else:
                    state = EXTENSION_STATE_UNSATISFIED
                    module = None
                
                self._state = state
                
                return module
            
            return None
            # no more cases
        
        finally:
            LOADING_EXTENSIONS.discard(self)
    
    
    def _load_module(self):
        """
        Loads the module and returns whether it was successfully loaded.
        
        Returns
        -------
        loaded : `bool`
        
        Raises
        ------
        BaseException
            Any exception raised from the extension file.
        """
        spec = self._spec
        module = spec.get_module()
        
        added_variable_names = self._added_variable_names
        if self._extend_default_variables:
            for name, value in EXTENSION_LOADER._default_variables.items():
                setattr(module, name, value)
                added_variable_names.append(name)
        
        default_variables = self._default_variables
        if (default_variables is not None):
            for name, value in default_variables.items():
                setattr(module, name, value)
                added_variable_names.append(name)
        
        
        active_extensions_at_start = LOADING_EXTENSIONS.copy()
        
        if self._take_snapshot:
            snapshot_old = take_snapshot()
        else:
            snapshot_old = None
        
        try:
            spec.loader.exec_module(module)
        except DoNotLoadExtension:
            loaded = False
        else:
            loaded = True
        
        if loaded:
            active_extensions_at_end = LOADING_EXTENSIONS.copy()
            extension_intersection = active_extensions_at_start & active_extensions_at_end
            extension_intersection.discard(self)
            
            if (snapshot_old is not None):
                snapshot_new = take_snapshot()
                snapshot_difference = calculate_snapshot_difference(snapshot_new, snapshot_old)
                
                for snapshot_extraction in self.iter_snapshot_extractions():
                    snapshot_difference = calculate_snapshot_difference(
                        snapshot_difference, snapshot_extraction
                    )
                
                self.clear_snapshot_extractions()
                
                self._snapshot_difference = snapshot_difference
                
                for extension in extension_intersection:
                    extension.add_snapshot_extraction(snapshot_difference)
            
            else:
                for snapshot_extraction in self.iter_snapshot_extractions():
                    for extension in extension_intersection:
                        extension.add_snapshot_extraction(snapshot_extraction)
                
                self.clear_snapshot_extractions()
        
        return loaded
    
    
    def _check_for_syntax(self):
        """
        Checks the file's new syntax.
        
        Used when reloading, to avoid unloading un-loadable files.
        
        This method is blocking. Run it inside of an executor.
        
        Raises
        ------
        SyntaxError
        """
        if (self._state == EXTENSION_STATE_LOADED) and self._spec.is_initialised():
            file_name = self.file_name
            # python files might not be `.py` files, which we should not compile.
            if file_name.endswith('.py'):
                try:
                    compile_module(file_name)
                except FileNotFoundError:
                    # If the file is deleted, is fine.
                    pass
    
    
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
        if state == EXTENSION_STATE_UNDEFINED:
            return None
        
        if state == EXTENSION_STATE_LOADED:
            self.clear_child_extensions()
            self.clear_parent_extensions()
            
            snapshot_difference = self._snapshot_difference
            if (snapshot_difference is not None):
                self._snapshot_difference = None
                revert_snapshot(snapshot_difference)
            
            self._state = EXTENSION_STATE_UNLOADED
            
            spec = self._spec
            try:
                del sys.modules[spec.name]
            except KeyError:
                pass
            
            return spec.get_module()
        
        if state in (EXTENSION_STATE_UNLOADED, EXTENSION_STATE_UNSATISFIED):
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
        Returns the extension's name.
        
        Returns
        -------
        name : `str`
        """
        return self._spec.name
    
    
    @property
    def path(self):
        """
        Returns the extension's name.
        
        Returns
        -------
        name : `str`
        """
        return self._spec.origin
    
    
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
            short_name = name[dot_index + 1:]
        
        return short_name
    
    
    @property
    def file_name(self):
        """
        Returns the extension's file's name.
        
        Returns
        -------
        file_name : `str`
        """
        return self._spec.origin
    
    
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
            module = self._spec.get_module()
            
            if self._extend_default_variables:
                for name in EXTENSION_LOADER._default_variables:
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
            return
        
        if state in (EXTENSION_STATE_UNLOADED, EXTENSION_STATE_UNSATISFIED):
            try:
                del sys.modules[self._spec.name]
            except KeyError:
                pass
            return
        
        # no more cases
    
    
    def add_child_extension(self, extension):
        """
        Registers a child extension.
        
        Parameters
        ----------
        extension : ``Extension``
            The extension to register.
        """
        child_extensions = self._child_extensions
        if (child_extensions is None):
            child_extensions = WeakSet()
            self._child_extensions = child_extensions
        
        child_extensions.add(extension)
    
    
    def iter_child_extensions(self):
        """
        Iterates over the child extensions.
        
        This method is an iterable generator.
        
        Yields
        ------
        child_extension : `None`
        """
        child_extensions = self._child_extensions
        if (child_extensions is not None):
            yield from child_extensions
    
    
    def are_child_extensions_present_in(self, extensions):
        """
        Returns whether all the child extensions are present in the given `extensions`.
        
        Parameters
        ----------
        extensions : `iterable` of ``Extension``
            Already present extensions to check satisfaction form.
        
        Returns
        -------
        are_child_extensions_present_in : `bool`
        """
        child_extensions = self._child_extensions
        if (child_extensions is None):
            return True
        
        if child_extensions <= extensions:
            return True
        
        return False
    
    
    def clear_child_extensions(self):
        """
        Clears the child extensions of the extension.
        """
        child_extensions = self._child_extensions
        if (child_extensions is not None):
            self._child_extensions = None
            
            for child_extension in child_extensions:
                child_extension.remove_parent_extension(self)
    
    
    def remove_child_extension(self, child_extension):
        """
        Removes the given extension from the extension's children.
        
        Parameters
        ----------
        child_extension : ``Extension``
            The extension to remove.
        """
        child_extensions = self._child_extensions
        if (child_extensions is not None):
            try:
                child_extensions.remove(child_extension)
            except KeyError:
                pass
            else:
                if not child_extensions:
                    self._child_extensions = child_extensions
    
    
    def add_snapshot_extraction(self, snapshots):
        """
        Adds snapshot extraction to the extension.
        
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
        Iterates over the snapshot extractions of the extension.
        
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
        Clears the snapshot extractions of the extension.
        """
        self._snapshot_extractions = None


    def add_parent_extension(self, extension):
        """
        Registers a parent extension.
        
        Parameters
        ----------
        extension : ``Extension``
            The extension to register.
        """
        parent_extensions = self._parent_extensions
        if (parent_extensions is None):
            parent_extensions = WeakSet()
            self._parent_extensions = parent_extensions
        
        parent_extensions.add(extension)
    
    
    def iter_parent_extensions(self):
        """
        Iterates over the parent extensions.
        
        This method is an iterable generator.
        
        Yields
        ------
        parent_extension : `None`
        """
        parent_extensions = self._parent_extensions
        if (parent_extensions is not None):
            yield from parent_extensions
    
    
    def are_parent_extensions_present_in(self, extensions):
        """
        Returns whether all the parent extensions are present in the given `extensions`.
        
        Parameters
        ----------
        extensions : `iterable` of ``Extension``
            Already present extensions to check satisfaction form.
        
        Returns
        -------
        are_parent_extensions_present_in : `bool`
        """
        parent_extensions = self._parent_extensions
        if (parent_extensions is None):
            return True
        
        if parent_extensions <= extensions:
            return True
        
        return False
    
    
    def clear_parent_extensions(self):
        """
        Clears the parent extensions of the extension.
        """
        parent_extensions = self._parent_extensions
        if (parent_extensions is not None):
            self._parent_extensions = parent_extensions
            
            for parent_extension in parent_extensions:
                parent_extension.remove_child_extension(self)
    
    
    def remove_parent_extension(self, parent_extension):
        """
        Removes the given extension from the extension's parents.
        
        Parameters
        ----------
        parent_extension : ``Extension``
            The extension to remove.
        """
        parent_extensions = self._parent_extensions
        if (parent_extensions is not None):
            try:
                parent_extensions.remove(parent_extension)
            except KeyError:
                pass
            else:
                if not parent_extensions:
                    self._parent_extensions = parent_extensions
    
    
    @property
    def _module(self):
        """
        Deprecated attribute of ``Extension``.
        """
        warnings.warn(
            f'`{self.__class__.__name__}._module` is deprecated, please use `._spec.get_module()` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return self._spec.get_module()
    
    
    def get_module(self):
        """
        Returns the module of the extension.
        
        Returns
        -------
        module : `None`, `ModuleType`
        """
        return self._spec.get_module()
