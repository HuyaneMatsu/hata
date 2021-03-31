# -*- coding: utf-8 -*-
__all__ = ('EXTENSION_LOADER', 'EXTENSIONS', 'ExtensionError', 'ExtensionLoader', )

import sys
from io import StringIO
from importlib.util import find_spec, module_from_spec
from importlib import reload as reload_module
from threading import current_thread

from ...backend.event_loop import EventThread
from ...backend.utils import alchemy_incendiary, HybridValueDictionary, WeakValueDictionary, DOCS_ENABLED
from ...backend.futures import is_coroutine_function as is_coro, Task
from ...backend.analyzer import CallableAnalyzer

from ...discord.client_core import KOKORO

from .snapshot import take_snapshot, calculate_snapshot_difference, revert_snapshot

EXTENSIONS = WeakValueDictionary()

EXTENSION_STATE_UNDEFINED = 0
EXTENSION_STATE_LOADED    = 1
EXTENSION_STATE_UNLOADED  = 2

class ExtensionError(Exception):
    """
    An exception raised by the ``ExtensionLoader``, if loading, reloading or unloading an extension fails with any
    reason.
    
    Attributes
    ----------
    _message : `str` or `list` of `str`
        The error's message.
    """
    
    def __init__(self, message):
        """
        Creates a new extension error.
        
        Parameters
        ----------
        message : `str` or `list` of `str`
            The error's message.
        """
        self._message = message
    
    @property
    def message(self):
        """
        Returns the extension error's message.
        
        If the extension error contains more message,s connects them.
        
        Returns
        -------
        message : ``Message``
        """
        message = self._message
        if type(message) is str:
            return message
        
        return '\n\n'.join(message)
    
    @property
    def messages(self):
        """
        Returns a list containing the exception error's messages.
        
        Returns
        -------
        messages : `list` of `str`
        """
        message = self._message
        if type(message) is str:
           return [message]
        
        return message
    
    def __len__(self):
        """Returns the amount of messages, what the extension error contains."""
        message = self._message
        if type(message) is str:
            return 1
        
        return len(message)
    
    def __repr__(self):
        """Returns the exception error's representation."""
        return f'{self.__class__.__name__} ({len(self)}):\n{self.message}\n'
    
    __str__ = __repr__

def _validate_entry_or_exit(point):
    """
    Validates the given entry or exit point, returning `True`, if they passed.
    
    Parameters
    ----------
    point : `None`, `str` or `callable`
        The point to validate.
    
    Raises
    ------
    TypeError
        If `point` was given as `callable`, but accepts less or more positional arguments, as would be given.
    """
    if point is None:
        return True
    
    if isinstance(point, str):
        return True
    
    if callable(point):
        analyzer = CallableAnalyzer(point)
        min_, max_ = analyzer.get_non_reserved_positional_argument_range()
        if min_ > 1:
            raise TypeError(f'`{point!r}` excepts at least `{min_!r}` non reserved arguments, meanwhile the event '
                'expects to pass `1`.')
        
        if min_ == 1:
            return True
        
        #min<expected
        if max_ >= 1:
            return True
        
        if analyzer.accepts_args():
            return True
        
        raise TypeError(f'`{point!r}` expects maximum `{max_!r}` non reserved arguments  meanwhile the event expects '
            'to pass `1`.')
    
    return False


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
        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | EXTENSION_STATE_UNDEFINED | 0     |
        +---------------------------+-------+
        | EXTENSION_STATE_LOADED    | 1     |
        +---------------------------+-------+
        | EXTENSION_STATE_UNLOADED  | 2     |
        +---------------------------+-------+
    _take_snapshot : `bool`
        Whether snapshot difference should be taken.
    """
    __slots__ = ('__weakref__', '_added_variable_names', '_default_variables', '_entry_point', '_exit_point',
        '_extend_default_variables', '_lib', '_locked', '_snapshot_difference', '_spec', '_state',
        '_take_snapshot', )
    
    def __new__(cls, name, entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference,
            default_variables, ):
        """
        Creates an extension with the given parameters. If an extension already exists with the given name, returns
        that.
        
        Parameters
        ----------
        name : `str`
            The extension's name (or import path).
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
        try:
            return EXTENSIONS[name]
        except KeyError:
            pass
        
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
        result = []
        result.append('<')
        result.append(self.__class__.__name__)
        result.append(' name=')
        result.append(repr(self._spec.name))
        
        state = self._state
        result.append(', state=')
        result.append(repr(state))
        result.append(' (')
        result.append(('undefined', 'loaded', 'unloaded')[state])
        result.append(')')
        
        if self._locked:
            result.append(', locked=True')
        
        default_variables = self._default_variables
        if self._extend_default_variables:
            if (default_variables is not None):
                result.append(' extends loader\'s defaults with: ')
                result.append(repr(default_variables))
        else:
            if default_variables is None:
                result.append(' clears loader\'s defaults')
            else:
                result.append(' clears loader\'s defaults and uses: ')
                result.append(repr(default_variables))
        
        result.append('>')
        
        return ''.join(result)
    
    def add_default_variables(self, **variables):
        """
        Adds default variables to the extension.
        
        Parameters
        ----------
        **variables : Keyword Arguments
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
        
        self._default_variables=None
    
    def clear_default_variables(self):
        """
        Removes all the default variables of the extension.
        """
        self._default_variables=None
        
    def _get_entry_point(self):
        return self._entry_point
    
    def _set_entry_point(self, entry_point):
        if not _validate_entry_or_exit(entry_point):
            raise TypeError(f'`{self.__class__.__name__}.entry_point` expected `None`, `str` or a `callable`, got '
                f'{entry_point.__class__.__name__}.')
        
        self._entry_point = entry_point
    
    def _del_entry_point(self):
        self._entry_point = None
    
    entry_point = property(_get_entry_point, _set_entry_point, _del_entry_point)
    del _get_entry_point, _set_entry_point, _del_entry_point
    
    if DOCS_ENABLED:
        entry_point.__doc__ = ("""
        Get-set-del descriptor for modifying the extension's entry point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """)
    
    def _get_exit_point(self):
        return self._exit_point
    
    def _set_exit_point(self, exit_point):
        if not _validate_entry_or_exit(exit_point):
            raise TypeError(f'`{self.__class__.__name__}.exit_point` expected `None`, `str` or a `callable`, got '
                f'{exit_point.__class__.__name__}.')
        
        self._exit_point = exit_point
    
    def _del_exit_point(self):
        self._exit_point = None
    
    exit_point = property(_get_exit_point, _set_exit_point, _del_exit_point)
    del _get_exit_point, _set_exit_point, _del_exit_point
    
    if DOCS_ENABLED:
        exit_point.__doc__ = ("""
        Get-set-del descriptor for modifying the extension's exit point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """)
    
    def _get_extend_default_variables(self):
        return self._extend_default_variables
    
    def _set_extend_default_variables(self, extend_default_variables):
        extend_default_variables_type = extend_default_variables.__class__
        if extend_default_variables_type is bool:
            pass
        elif issubclass(extend_default_variables_type, int):
            extend_default_variables = bool(extend_default_variables)
        else:
            raise TypeError(f'`extend_default_variables` should have been passed as `bool`, got '
                f'{extend_default_variables_type.__name__}.')
        
        self._extend_default_variables = extend_default_variables
    
    extend_default_variables = property(_get_extend_default_variables,_set_extend_default_variables)
    del _get_extend_default_variables, _set_extend_default_variables
    
    if DOCS_ENABLED:
        extend_default_variables.__doc__ = ("""
        Set-del descriptor to define whether the extension uses the loader's default variables or just it's own's.
        
        Accepts and returns `bool`.
        """)
    
    def _get_locked(self):
        return self._locked
    
    def _set_locked(self, locked):
        locked_type = locked.__class__
        if locked_type is bool:
            pass
        elif issubclass(locked_type, int):
            locked = bool(locked)
        else:
            raise TypeError(f'`locked` should have been passed as `bool`, got: {locked_type.__name__}.')
        
        self._locked = locked
    
    locked = property(_get_locked, _set_locked)
    del _get_locked, _set_locked
    
    if DOCS_ENABLED:
        locked.__doc__ = ("""
        Set-del descriptor to define whether the extension should be picked up by the `{}_all` methods of the
        extension loader.
        
        Accepts and returns `bool`.
        """)
    
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
            lib = sys.modules.get(spec.name)
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
                
                spec.loader.exec_module(lib)
                sys.modules[spec.name] = lib
            
                if self._take_snapshot:
                    snapshot_new = take_snapshot()
                    
                    self._snapshot_difference = calculate_snapshot_difference(snapshot_old, snapshot_new)
            
            self._lib = lib
            
            self._state = EXTENSION_STATE_LOADED
            return lib
        
        if state == EXTENSION_STATE_LOADED:
            # return None -> already loaded
            return None
        
        if state == EXTENSION_STATE_UNLOADED:
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
            
            reload_module(lib)
            
            if self._take_snapshot:
                snapshot_new = take_snapshot()
                
                self._snapshot_difference = calculate_snapshot_difference(snapshot_old, snapshot_new)
            
            self._state = EXTENSION_STATE_LOADED
            return lib
        
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
        
        if state == EXTENSION_STATE_UNLOADED:
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
            
            del sys.modules[self._spec.name]
            return
        
        if state == EXTENSION_STATE_UNLOADED:
            del sys.modules[self._spec.name]
            return
        
        # no more cases

PROTECTED_NAMES = {
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_cached',
    '_set_fileattr',
    'cached',
    'has_location',
    'loader',
    'loader_state',
    'name',
    'origin',
    'parent',
    'submodule_search_locations',
        }

class ExtensionLoader:
    """
    There are some cases when you probably want to change some functional part of your client in runtime. Load,
    unload or reload code. Hata provides an easy to use (that's what she said) solution to solve this issue.
    
    It is called extension loader is an extension of hata. It is separated from `commands` extension, but it does not
    mean they do not go well together. But what more, extension loader was made to complement it.
    
    Usage
    -----
    The ``ExtensionLoader`` class is instanced already as `EXTENSION_LOADER` and that can be imported as well from
    `extension_loader.py`. Instancing the class again will yield the same object.
    
    Because hata can have more clients, we needed a special extension loader what can handle using more clients at any
    file, so the choice ended up on a  really interesting idea: assign variables to a module before it is (re)loaded.
    
    To show this is not blackmagic, here is an example:
    
    **main.py**
    
    ```py
    from hata.ext.extension_loader import EXTENSION_LOADER
    from datetime import datetime
    
    cake = 'cake'
    now = datetime.now()
    
    EXTENSION_LOADER.add_default_variables(cake=cake, now=now)
    EXTENSION_LOADER.load_extension('extension')
    ```
    
    **extension.py**
    
    ```py
    print(cake, now)
    ```
    
    Make sure you start `main.py` with interactive mode. If you never did it, just use the `-i` option like:
    
    ```
    $ python3 -i main.py
    ```
    
    Or on windows:
    
    ```
    $ python -i main.py
    ```
    
    After you ran `main.py` you should see the following (the date should be different tho):
    
    ```
    cake 2020-03-14 09:40:41.587673
    ```
    
    Because now we have the interpreter, you can change the variables.
    
    ```py
    >>> EXTENSION_LOADER.add_default_variables(cake='cakes taste good, and now is:')
    >>> EXTENSION_LOADER.reload_all()
    ```
    
    And a different text is printed out:
    
    ```
    cakes taste good, and now is: 2020-03-14 09:40:41.587673
    ```
    
    Now lets edit `extension.py`.
    
    ```py
    cake = cake.split()
    print(*cake, now, sep='\\n')
    ```
    
    And reload the extension:
    
    ```py
    >>> EXTENSION_LOADER.reload_all()
    ```
    
    The printed text really changed again:
    
    ```
    cakes
    taste
    good,
    and
    now
    is:
    2020-03-14 09:40:41.587673
    ```
    
    If you remove default variables and the extension file still uses them, you get an ``ExtensionError``:
    
    ```py
    >>> EXTENSION_LOADER.remove_default_variables('cake')
    >>> EXTENSION_LOADER.reload_all()
    ```
    
    ```
    Traceback (most recent call last):
      File "<pyshell#13>", line 1, in <module>
        EXTENSION_LOADER.reload_all()
      File ".../hata/backend/extension_loader.py", line 652, in reload_all
        task.sync_wrap().wait()
      File ".../hata/backend/futures.py", line 823, in wait
        return self.result()
      File ".../hata/backend/futures.py", line 723, in result
        raise exception
      File ".../hata/backend/futures.py", line 1602, in __step
        result=coro.throw(exception)
      File ".../hata/ext/extension_loader/extension_loader.py", line 670, in _reload_all
        raise ExtensionError(error_messages) from None
    hata.ext.extension_loader.ExtensionError: ExtensionError (1):
    Exception occurred meanwhile loading an extension: `extension`.
    
    Traceback (most recent call last):
      File ".../hata/ext/extension_loader/extension_loader.py", line 675, in _load_extension
        lib = await KOKORO.run_in_executor(extension.load)
      File ".../hata/extension_loader.py", line 270, in load
        reload_module(lib)
      File ".../importlib/__init__.py", line 169, in reload
        _bootstrap._exec(spec, module)
      File "<frozen importlib._bootstrap>", line 630, in _exec
      File "<frozen importlib._bootstrap_external>", line 728, in exec_module
      File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
      File ".../extension.py", line 1, in <module>
        cake = cake.split()
    NameError("name 'cake' is not defined")
    ```
    
    Adding Extensions
    -----------------
    Extensions can be added with the `.add` method.
    
    ```py
    EXTENSION_LOADER.add('cute_commands')
    ```
    
    Or more extension can be added as well by passing an iterable:
    
    ```py
    EXTENSION_LOADER.add(['cute_commands', 'nice_commands'])
    ```
    
    If an extension's file is not found, then `.add` will raise  `ModuleNotFoundError`. If the passed argument is not
    `str` instance or not `iterable` of `str`, `TypeError` is raised.
    
    Loading
    -------
    Extensions can be loaded by their name:
    
    ```py
    EXTENSION_LOADER.load('cute_commands')
    ```
    
    All extension can be loaded by using:
    
    ```py
    EXTENSION_LOADER.load_all()
    ```
    
    Or extension can be added and loaded at the same time as well:
    
    ```py
    EXTENSION_LOADER.load_extension('cute_commands')
    ```
    
    `.load_extension` method supports all the keyword arguments as `.add`.
    
    ##### Passing variables to extensions
    
    You can pass variables to extensions with the `.add_default_variables` method:
    
    ```py
    EXTENSION_LOADER.add_default_variables(cake=cake, now=now)
    ```
    
    Adding or removing variables wont change the already loaded extensions' state, those needs to be reloaded to see
    them.
    
    Or pass variables to just specific extensions:
    
    ```py
    EXTENSION_LOADER.add('cute_commands', cake=cake, now=now)
    ```
    
    You can specify if the extension should use just it's own variables and ignore the default ones too:
    
    ```py
    EXTENSION_LOADER.add('cute_commands', extend_default_variables=False, cake=cake, now=now)
    ```
    
    Every variable added is stored in an optionally weak value dictionary, but you are able remove the added variables as well:
    
    ```py
    EXTENSION_LOADER.remove_default_variables('cake', 'now')
    ```
    
    The extensions can be accessed by their name as well, then you can use their properties to modify them.
    
    ```py
    EXTENSION_LOADER.extensions['cute_commands'].remove_default_variables('cake')
    ```
    
    Unloading And Exit Point
    ------------------------
    You can unload extension on the same way as loading them.
    
    ```py
    EXTENSION_LOADER.unload('cute_commands')
    ```
    
    Or unload all:
    
    ```py
    EXTENSION_LOADER.unload_all()
    ```
    
    When unloading an extension, the extension loader will search a function at the extension, what we call
    `exit_point` and will run it. By default it looks for a variable named `teardown`. `exit_point` acts on the same
    way as the `entry_point`, so it can be modified for looking for other name to defining and passing a callable
    (can be async again).
    
    Can be set almost on the same way as well:
    
    ```py
    EXTENSION_LOADER.default_exit_point = 'exit'
    ```
    
    Or:
    
    ```py
    EXTENSION_LOADER.add('cute_commands', exit_point='exit')
    ```
    
    There are also methods for reloading: `.reload(name)` and `.reload_all()`
    
    Removing Extensions
    -------------------
    
    Unloaded extensions can be removed from the extension loader by using the `.remove` method:
    
    ```py
    EXTENSION_LOADER.remove('cute_commands')
    ```
    
    Or more extension with an iterable:
    
    ```py
    EXTENSION_LOADER.remove(['cute_commands', 'nice_commands'])
    ```
    
    Removing loaded extension will yield `RuntimeError`.
    
    Threading Model
    ---------------
    When you call the different methods of the extension loader, they ll run on the ``Clients`` thread, what is named
    `KOKORO` internally.
    
    These methods are:
    - ``.load_extension``
    - ``.load``
    - ``.load_all``
    - ``.unload``
    - ``.unload_all``
    - ``.reload``
    - ``.reload_all``
    
    Meanwhile loading and executing the extension's code the thread is switched to an executor, so blocking tasks can
    be executed easily. The exception under this rule are the `entry_point`-s and the `exit_point`-s, which always run
    on the same thread as the clients, that is why they can be async as well.
    
    These methods also act differently depending from which thread they were called from. Whenever they are called from
    the client's thread, a ``Task`` is returned what can be `awaited`. If called from other ``EventThread``, then the task
    is async_wrapped and that is returned. When calling from any other thread (like the main thread for example), the
    task is sync_wrapped and the thread is blocked till the extension's loading is finished.
    
    Attributes
    ----------
    _default_entry_point : `None`, `str` or `callable`
        Internal slot for the ``.default_entry_point`` property.
    _default_exit_point : `None`, `str` or `callable`
        Internal slot for the ``.default_exit_point`` property.
    _default_variables : `None` or `HybridValueDictionary` of (`str`, `Any`) items
        An optionally weak value dictionary to store objects for assigning them to modules before loading them.
        If it would be set as empty, then it is set as `None` instead.
    extensions : `dict` of (`str`, ``Extension``) items
        A dictionary of the added extensions to the extension loader in `extension-name` - ``Extension`` relation.
    
    Class Attributes
    ---------------
    _instance : `None` or ``ExtensionLoader``
        The already created instance of the ``ExtensionLoader`` if there is any.
    """
    __slots__ = ('_default_entry_point', '_default_exit_point', '_default_variables', 'extensions', )
    
    _instance = None
    def __new__(cls,):
        """
        Creates an ``ExtensionLoader`` instance. If the `ExtensionLoader` was instanced already, then returns that
        instead.
        
        Returns
        -------
        self : ``ExtensionLoader``
        """
        self = cls._instance
        if self is None:
            self = object.__new__(cls)
            self._default_entry_point = 'setup'
            self._default_exit_point = 'teardown'
            self.extensions = {}
            self._default_variables = HybridValueDictionary()
        
        return self
    
    def _get_default_entry_point(self):
        return self._default_entry_point
    
    def _set_default_entry_point(self, default_entry_point):
        if not _validate_entry_or_exit(default_entry_point):
            raise TypeError(f'`{self.__class__.__name__}.default_entry_point` expected `None`, `str` or a `callable`, '
                f'got {default_entry_point.__class__.__name__}.')
        
        self._default_entry_point=default_entry_point
    
    def _del_default_entry_point(self):
        self._default_entry_point = None
    
    default_entry_point = property(_get_default_entry_point, _set_default_entry_point, _del_default_entry_point)
    del _get_default_entry_point, _set_default_entry_point, _del_default_entry_point
    
    if DOCS_ENABLED:
        default_entry_point.__doc__ = ("""
        Get-set-del descriptor for modifying the extension loader's default entry point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """)
    
    def _get_default_exit_point(self):
        return self._default_exit_point
    
    def _set_default_exit_point(self, default_exit_point):
        if not _validate_entry_or_exit(default_exit_point):
            raise TypeError(f'`{self.__class__.__name__}.default_exit_point` expected `None`, `str` or a `callable`, '
                f'got {default_exit_point.__class__.__name__}.')
        
        self._default_exit_point=default_exit_point
    
    def _del_default_exit_point(self):
        self._default_exit_point=None
    
    default_exit_point = property(_get_default_exit_point, _set_default_exit_point, _del_default_exit_point)
    del _get_default_exit_point, _set_default_exit_point, _del_default_exit_point
    
    if DOCS_ENABLED:
        default_exit_point.__doc__ = ("""
        Get-set-del descriptor for modifying the extension loader's default exit point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """)
    
    def add_default_variables(self, **variables):
        """
        Adds default variables to the extension loader.
        
        Parameters
        ----------
        **variables : Keyword Arguments
            Variables to assigned to an extension's module before it is loaded.
        
        Raises
        ------
        ValueError
             If a variable name is would be used, what is `module` attribute.
        """
        default_variables = self._default_variables
        for key, value in variables.items():
            if key in PROTECTED_NAMES:
                raise ValueError(f'The passed {key!r} is a protected variable name of module type.')
            default_variables[key] = value
    
    def remove_default_variables(self, *names):
        """
        Removes the mentioned default variables of the extension loader.
        
        If a variable with a specified name is not found, no error is raised.
        
        Parameters
        ----------
        *names : `str`
            Default variable names.
        """
        default_variables = self._default_variables
        for name in names:
            try:
                del default_variables[name]
            except KeyError:
                pass
    
    def clear_default_variables(self):
        """
        Removes all the default variables of the extension loader.
        """
        self._default_variables.clear()
    
    def add(self, name, entry_point=None, exit_point=None, extend_default_variables=True, locked=False,
            take_snapshot_difference=True, **variables):
        """
        Adds an extension to the extension loader.
        
        Parameters
        ----------
        name : `str` or `iterable` of `str`
            The extension(s)'s name(s) to add.
        entry_point : `None, `str` or `callable`, Optional
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None, `str` or `callable`, Optional
            Extension specific exit point, to use over the extension loader's default.
        locked : `bool`
            Whether the given extension(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`
            Whether snapshot feature should be used.
        **variables : Keyword arguments
            Variables to assign to an extension(s)'s module before they are loaded.
        
        Raises
        ------
        TypeError
            - If `entry_point` was not given as `None`, `str` or as `callable`.
            - If `entry_point` was given as `callable`, but accepts less or more positional arguments, as would be
                given.
            - If `exit_point` was not given as `None`, `str` or as `callable`.
            - If `exit_point` was given as `callable`, but accepts less or more positional arguments, as would be
                given.
            - If `extend_default_variables` was not given as `bool`.
            - If `locked` was not given as `bool`.
            - If `name` was not given as `str` or as `iterable` of `str`.
        ValueError
            If a variable name is would be used, what is `module` attribute.
        """
        if not _validate_entry_or_exit(entry_point):
            raise TypeError(f'`{self.__class__.__name__}.add` expected `None`, `str` or a `callable` as '
                f'`entry_point`, got {entry_point.__class__.__name__}.')
        
        if not _validate_entry_or_exit(exit_point):
            raise TypeError(f'`{self.__class__.__name__}.add` expected `None`, `str` or a `callable` as `exit_point`, '
                f'got {exit_point.__class__.__name__}.')
        
        if variables:
            default_variables = HybridValueDictionary(variables)
            for key, value in variables.items():
                if key in PROTECTED_NAMES:
                    raise ValueError(f'The passed {key!r} is a protected variable name of module type.')
                default_variables[key] = value
        else:
            default_variables = None
        
        extend_default_variables_type = extend_default_variables.__class__
        if extend_default_variables_type is bool:
            pass
        elif issubclass(extend_default_variables_type, int):
            extend_default_variables = bool(extend_default_variables)
        else:
            raise TypeError(f'`extend_default_variables` should have been passed as `bool`, got: '
                f'{extend_default_variables_type.__name__}.')
        
        locked_type = locked.__class__
        if locked_type is bool:
            pass
        elif issubclass(locked_type, int):
            locked = bool(locked)
        else:
            raise TypeError(f'`locked` should have been passed as `bool`, got: {locked_type.__name__}.')
        
        name_type = name.__class__
        if name_type is str:
            pass
        
        elif issubclass(name_type, str):
            name = str(name)
        
        if hasattr(name_type, '__iter__'):
            names = []
            index = 1
            for name_ in name:
                name_type = name_.__class__
                if name_type is str:
                    pass
                elif issubclass(name_type, str):
                    name = str(name)
                else:
                    raise TypeError(f'`{self.__class__.__name__}.add` expected `str` or `iterable` of `str` as '
                        f'`name`, got, `iterable`, but it\'s {index}. element is not `str` instance, got: '
                        f'{name_type.__class__}')
                
                names.append(name)
                index += 1
            
            for name in names:
                extension = Extension(name, entry_point, exit_point, extend_default_variables, locked,
                    take_snapshot_difference, default_variables)
                
                self.extensions[name] = extension
                
                dot_index = name.rfind('.')
                if dot_index != -1:
                    name = name[dot_index+1:]
                    
                    self.extensions.setdefault(name, extension)
            
            return
        else:
            raise TypeError(f'`{self.__class__.__name__}.add` expected `str` or `iterable of str` as `name`, got '
                f'`{name_type.__name__}`.')
        
        extension = Extension(name, entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference,
            default_variables)
        
        self.extensions[name] = extension
        
        dot_index = name.rfind('.')
        if dot_index != -1:
            name = name[dot_index+1:]
            
            self.extensions.setdefault(name, extension)
        
    def remove(self, name):
        """
        Removes one or more extensions from the extension loader.
        
        If any of the extensions is not found, no errors will be raised.
        
        Parameters
        ----------
        name : `str` or `iterable` of `str`
            The extension(s)'s name(s) to remove.
        
        Raises
        ------
        TypeError
            If `name` was not given as `str` or as `iterable` of `str`.
        RuntimeError
            If a loaded extension would be removed.
        """
        name_type = name.__class__
        if name_type is str:
            pass
        
        elif issubclass(name_type, str):
            name = str(name)
        
        elif hasattr(name_type, '__iter__'):
            names = []
            index = 1
            for name in name:
                name_type = name.__class__
                if name_type is str:
                    pass
                elif issubclass(name_type, str):
                    name = str(name)
                else:
                    raise TypeError(f'`{self.__class__.__name__}.remove` expected `str` or `iterable` of `str` as '
                        f'`name`, got, `iterable`, but it\'s {index}. element is not `str` instance, got: '
                        f'{name_type.__class__}')
                
                names.append(name)
                index += 1
            
            collected = []
            extensions = self.extensions
            for name in names:
                try:
                    extension = extensions[name]
                except KeyError:
                    continue
                
                if extension._state == EXTENSION_STATE_LOADED:
                    raise RuntimeError(f'Extension `{name!r}` can not be removed, meanwhile it is loaded.')
                
                collected.append(extension)
                
            for extension in collected:
                extension._unlink()
            
            return
        else:
            #no more good case -> raise
            raise TypeError(f'`{self.__class__.__name__}.remove` expected `str` or `iterable of str` as `name`, got '
                f'{name_type.__name__}.')

        try:
            extension = self.extensions[name]
        except KeyError:
            return
        
        if extension._state == EXTENSION_STATE_LOADED:
            raise RuntimeError(f'Extension `{name!r}` can not be removed, meanwhile it is loaded.')
        
        extension._unlink()
        return
    
    def load_extension(self, name, *args, **kwargs):
        """
        Adds, then loads the extension.
        
        Parameters
        ----------
        name : `str`
            The extension's name.
        *args : Argument
            Additional argument to create the extension with.
        **kwargs : Keyword Arguments
            Additional keyword arguments to create the extension with.
        
        Other Parameters
        ----------------
        entry_point : `None, `str` or `callable`, Optional
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None, `str` or `callable`, Optional
            Extension specific exit point, to use over the extension loader's default.
        locked : `bool`
            Whether the given extension(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`
            Whether snapshot feature should be used.
        **variables : Keyword arguments
            Variables to assign to an extension(s)'s module before they are loaded.
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
        
        Raises
        ------
        TypeError
            - If `name` was not given as `str`.
            - If `entry_point` was not given as `None`, `str` or as `callable`.
            - If `entry_point` was given as `callable`, but accepts less or more positional arguments, as would be
                given.
            - If `exit_point` was not given as `None`, `str` or as `callable`.
            - If `exit_point` was given as `callable`, but accepts less or more positional arguments, as would be
                given.
            - If `extend_default_variables` was not given as `bool`.
            - If `locked` was not given as `bool`.
        ValueError
            If a variable name is would be used, what is `module` attribute.
        ExtensionError
            The extension failed to load correctly.
        """
        name_type = name.__class__
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(f'`name` should have be given as `str` instance, got {name_type.__name__}.')
        
        self.add(name, *args, **kwargs)
        return self.load(name)
    
    def load(self, name):
        """
        Loads the extension with the given name. If the extension is already loaded, will do nothing.
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Loading the extension failed.
        """
        task = Task(self._load(name), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    async def _load(self, name):
        """
        Loads the extension with the given name.
        
        This method is a coroutine.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Loading the extension failed.
        """
        try:
            extension = self.extensions[name]
        except KeyError:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from None
        
        await self._load_extension(extension)
        
    def unload(self, name):
        """
        Unloads the extension with the given name.
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            unloading is done. However if called from a sync thread, will block till the unloading is done.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Unloading the extension failed.
        """
        task = Task(self._unload(name), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    async def _unload(self, name):
        """
        Unloads the extension with the given name.
        
        This method is a coroutine.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Unloading the extension failed.
        """
        try:
            extension = self.extensions[name]
        except KeyError:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from None
        
        await self._unload_extension(extension)
        
    def reload(self, name):
        """
        Reloads the extension with the given name.
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            reloading is done. However if called from a sync thread, will block till the reloading is done.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Reloading the extension failed.
        """
        task = Task(self._reload(name),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    async def _reload(self, name):
        """
        Reloads the extension with the given name.
        
        This method is a coroutine.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Reloading the extension failed.
        """
        try:
            extension = self.extensions[name]
        except KeyError:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from None
        
        await self._unload_extension(extension)
        await self._load_extension(extension)
    
    def load_all(self):
        """
        Loads all the extension of the extension loader. If anything goes wrong, raises an ``ExtensionError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
        
        Raises
        ------
        ExtensionError
            If any extension failed to load correctly.
        """
        task = Task(self._load_all(),KOKORO)

        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
        
    async def _load_all(self):
        """
        Loads all the extensions of the extension loader.
        
        Loads each extension one after the other. The raised exceptions' messages are collected into one exception,
        what will be raised only at the end. If any of the extensions raises, will still try to unload the leftover
        ones.
        
        This method is a coroutine.
        
        Raises
        ------
        ExtensionError
            If any extension failed to load correctly.
        """
        error_messages = []
        
        for extension in self.extensions.values():
            if extension._locked:
                continue
            
            try:
                await self._load_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
            
        if error_messages:
            raise ExtensionError(error_messages) from None
        
    def unload_all(self):
        """
        Unloads all the extension of the extension loader. If anything goes wrong, raises an ``ExtensionError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            unloading is done. However if called from a sync thread, will block till the unloading is done.
        
        Raises
        ------
        ExtensionError
            If any extension failed to unload correctly.
        """
        task = Task(self._unload_all(), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    async def _unload_all(self):
        """
        Unloads all the extensions of the extension loader.
        
        Unloads each extension one after the other. The raised exceptions' messages are collected into one exception,
        what will be raised only at the end. If any of the extensions raises, will still try to unload the leftover
        ones.
        
        This method is a coroutine.
        
        Raises
        ------
        ExtensionError
            If any extension failed to unload correctly.
        """
        error_messages = []
        
        for extension in self.extensions.values():
            if extension._locked:
                continue
            
            try:
                await self._unload_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
            
        if error_messages:
            raise ExtensionError(error_messages) from None
    
    def reload_all(self):
        """
        Reloads all the extension of the extension loader. If anything goes wrong, raises an ``ExtensionError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            reloading is done. However if called from a sync thread, will block till the reloading is done.
        
        Raises
        ------
        ExtensionError
            If any extension failed to reload correctly.
        """
        task = Task(self._reload_all(), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    async def _reload_all(self):
        """
        Reloads all the extensions of the extension loader.
        
        If an extension is not unloaded, will load it, if the extension is loaded, will unload, then load it.
        Reloads each extension one after the other. The raised exceptions' messages are collected into one exception,
        what will be raised at the end. If any of the extensions raises, will still try to reload the leftover ones.
        
        This method is a coroutine.
        
        Raises
        ------
        ExtensionError
            If any extension failed to reload correctly.
        """
        error_messages = []
        
        for extension in self.extensions.values():
            if extension._locked:
                continue
            
            try:
                await self._unload_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
                continue
            
            try:
                await self._load_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
        
        if error_messages:
            raise ExtensionError(error_messages) from None
    
    async def _load_extension(self, extension):
        """
        Loads the extension. If the extension is loaded, will do nothing.
        
        Loading an exception can be separated to 4 parts:
        
        - Assign the default variables.
        - Load the module.
        - Find the entry point (if needed).
        - Ensure the entry point (if found).
        
        If any of these fails, an ``ExtensionError`` will be raised. If step 1 raises, then a traceback will be
        included as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        extension : ``Extension``
            The extension to load.
        
        Raises
        ------
        ExtensionError
            Extension entry point raised.
        """
        try:
            # loading blocks, but unloading does not
            lib = await KOKORO.run_in_executor(extension._load)
        except BaseException as err:
            message = await KOKORO.run_in_executor(alchemy_incendiary(
                self._render_exc, (err, [
                'Exception occurred meanwhile loading an extension: `', extension.name, '`.\n\n',],
                    )))
            
            raise ExtensionError(message) from None
        
        if lib is None:
            return # already loaded
        
        entry_point = extension._entry_point
        if entry_point is None:
            entry_point = self._default_entry_point
            if entry_point is None:
                return
        
        if isinstance(entry_point, str):
            entry_point = getattr(lib, entry_point, None)
            if entry_point is None:
                return
        
        try:
            
            if is_coro(entry_point):
                await entry_point(lib)
            else:
                entry_point(lib)
        
        except BaseException as err:
            message = await KOKORO.run_in_executor(alchemy_incendiary(
                self._render_exc, (err, [
                'Exception occurred meanwhile entering an extension: `', extension.name,
                '`.\nAt entry_point:', repr(entry_point), '\n\n',],
                    )))
            
            raise ExtensionError(message) from None
    
    async def _unload_extension(self, extension):
        """
        Unloads the extension. If the extension is not loaded, will do nothing.
        
        Loading an exception can be separated to 3 parts:
        
        - Find the exit point (if needed).
        - Ensure the exit point (if found).
        - Remove the default variables.
        
        If any of these fails, an ``ExtensionError`` will be raised. If step 2 raises, then a traceback will be
        included as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        extension : ``Extension``
            The extension to unload.
        
        Raises
        ------
        ExtensionError
            Extension exit point raised.
        """
        # loading blocks, but unloading does not
        lib = extension._unload()
        
        if lib is None:
            return # not loaded
        
        try:
            exit_point = extension._exit_point
            if exit_point is None:
                exit_point = self._default_exit_point
                if exit_point is None:
                    return
            
            if isinstance(exit_point, str):
                exit_point = getattr(lib, exit_point, None)
                if exit_point is None:
                    return
            
            try:
                
                if is_coro(exit_point):
                    await exit_point(lib)
                else:
                    exit_point(lib)
            
            except BaseException as err:
                message = await KOKORO.run_in_executor(alchemy_incendiary(
                    self._render_exc, (err, [
                    'Exception occurred meanwhile unloading an extension: `', extension.name,
                    '`.\nAt exit_point:', repr(exit_point), '\n\n',],
                        )))
                
                raise ExtensionError(message) from None
        
        finally:
            extension._unassign_variables()
            
            keys = []
            lib_globals = lib.__dict__
            for key in lib_globals:
                if (not key.startswith('__')) and (not key.endswith('__')):
                    keys.append(key)
            
            for key in keys:
                del lib_globals[key]
    
    @staticmethod
    def _render_exc(exception, header):
        """
        Renders an exception' traceback.
        
        Parameters
        ----------
        exception : `BaseException` instance
            The exception to render.
        header : `str` or `list` of `str`
            Header of the rendered traceback.
        
        Returns
        -------
        message : `str`
            The `exception`'s rendered traceback.
        
        Notes
        -----
        This function should run in an executor.
        """
        file = StringIO()
        EventThread._render_exc_sync(exception, before=header, after=None, file=file)
        message = file.getvalue()
        file.close()
        
        return message
    
    def __repr__(self):
        """Returns the extension loader's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' extension count=',
            repr(len(self.extensions)),
                ]
        
        entry_point = self._default_entry_point
        if (entry_point is not None):
            result.append(', default_entry_point=')
            result.append(repr(entry_point))
        
        exit_point = self._default_exit_point
        if (exit_point is not None):
            result.append(', default_exit_point=')
            result.append(repr(exit_point))
        
        default_variables = self._default_variables
        if default_variables:
            result.append(', default_variables=')
            result.append(repr(default_variables))
        
        result.append('>')
        
        return ''.join(result)

EXTENSION_LOADER = ExtensionLoader()
