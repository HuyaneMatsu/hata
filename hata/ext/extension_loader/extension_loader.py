__all__ = ('EXTENSION_LOADER', 'ExtensionLoader', )

import warnings
from io import StringIO
from threading import current_thread

from ...backend.event_loop import EventThread
from ...backend.utils import alchemy_incendiary, HybridValueDictionary
from ...backend.futures import is_coroutine_function, Task
from ...backend.export import export

from ...discord.core import KOKORO

from .extension import EXTENSIONS, Extension, EXTENSION_STATE_LOADED
from .utils import PROTECTED_NAMES, _iter_extension_names_and_paths, _validate_entry_or_exit, \
    validate_extension_parameters, _get_path_extension_name
from .exceptions import ExtensionError


def _get_extensions(name):
    """
    Gets the extensions with the given name.
    
    Parameters
    ----------
    name : `str` or `iterable` of `str`
        Extension by name to find.
    
    Returns
    -------
    extensions : `set` of ``Extension``
        The found extensions.
    
    Raises
    ------
    ExtensionError
        If an extension could not be found.
    """
    extensions = set()
    
    extension_names_and_paths = set(_iter_extension_names_and_paths(name))
    for extension_name, extension_path in extension_names_and_paths:
        if extension_name is None:
            extension_name = _get_path_extension_name(extension_path)
        
        try:
            extension = EXTENSION_LOADER._extensions_by_name[extension_name]
        except KeyError:
            raise ExtensionError(f'No extension was added with name: `{extension_name}`.') from None
        
        extensions.add(extension)
    
    return extensions


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
      File ".../hata/backend/futures.py", line 1602, in _step
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
    
    If an extension's file is not found, then `.add` will raise  `ModuleNotFoundError`. If the passed parameter is not
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
    
    `.load_extension` method supports all the keyword parameters as `.add`.
    
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
    EXTENSION_LOADER.get_extension('cute_commands').remove_default_variables('cake')
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
    _execute_counter : `int`
        Whether the extension loader is executing an extension.
    _extensions_by_name : `dict` of (`str`, ``Extension``) items
        A dictionary of the added extensions to the extension loader in `extension-name` - ``Extension`` relation.
    
    Class Attributes
    ---------------
    _instance : `None` or ``ExtensionLoader``
        The already created instance of the ``ExtensionLoader`` if there is any.
    """
    __slots__ = ('_default_entry_point', '_default_exit_point', '_default_variables', '_execute_counter',
        '_extensions_by_name', )
    
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
            self._extensions_by_name = {}
            self._default_variables = HybridValueDictionary()
            self._execute_counter = 0
        
        return self
    
    @property
    def default_entry_point(self):
        """
        Get-set-del descriptor for modifying the extension loader's default entry point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """
        return self._default_entry_point
    
    @default_entry_point.setter
    def default_entry_point(self, default_entry_point):
        if not _validate_entry_or_exit(default_entry_point):
            raise TypeError(f'`{self.__class__.__name__}.default_entry_point` expected `None`, `str` or a `callable`, '
                f'got {default_entry_point.__class__.__name__}.')
        
        self._default_entry_point = default_entry_point
    
    @default_entry_point.deleter
    def default_entry_point(self):
        self._default_entry_point = None
    
    
    @property
    def default_exit_point(self):
        """
        Get-set-del descriptor for modifying the extension loader's default exit point.
        
        Accepts and returns `None`, `str` or a `callable`. If invalid type is given, raises `TypeError`.
        """
        return self._default_exit_point
    
    @default_exit_point.setter
    def default_exit_point(self, default_exit_point):
        if not _validate_entry_or_exit(default_exit_point):
            raise TypeError(f'`{self.__class__.__name__}.default_exit_point` expected `None`, `str` or a `callable`, '
                f'got {default_exit_point.__class__.__name__}.')
        
        self._default_exit_point = default_exit_point
    
    @default_exit_point.deleter
    def default_exit_point(self):
        self._default_exit_point = None
    
    def add_default_variables(self, **variables):
        """
        Adds default variables to the extension loader.
        
        Parameters
        ----------
        **variables : Keyword Parameters
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
    
    
    def add(self, name, *args, **kwargs):
        """
        Adds an extension to the extension loader.
        
        Parameters
        ----------
        name : `str` or `iterable` of `str`
            The extension's name to load.
        *args : Parameters
            Additional parameters to create the extension with.
        **kwargs : Keyword parameters
            Additional parameters to create the extension with.
        
        Other Parameters
        ----------------
        entry_point : `None`, `str` or `callable`, Optional
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None`, `str` or `callable`, Optional
            Extension specific exit point, to use over the extension loader's default.
        locked : `bool`, Optional
            Whether the given extension(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`, Optional
            Whether snapshot feature should be used.
        **variables : Keyword parameters
            Variables to assign to an extension(s)'s module before they are loaded.
            
        Raises
        ------
        ImportError
            If the given name do not refers to any loadable file.
        TypeError
            - If `entry_point` was not given as `None`, `str` or as `callable`.
            - If `entry_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `exit_point` was not given as `None`, `str` or as `callable`.
            - If `exit_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `extend_default_variables` was not given as `bool`.
            - If `locked` was not given as `bool`.
            - If `name` was not given as `str` or as `iterable` of `str`.
        ValueError
            If a variable name is would be used, what is `module` attribute.
        """
        extension_names_and_paths = set(_iter_extension_names_and_paths(name))
        entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables = \
            validate_extension_parameters(*args, **kwargs)
        
        for extension_name, extension_path in extension_names_and_paths:
            self._add(extension_name, extension_path, entry_point, exit_point, extend_default_variables, locked,
                take_snapshot_difference, default_variables)
    
    
    def _add(self, extension_name, extension_path, entry_point, exit_point, extend_default_variables, locked,
            take_snapshot_difference, default_variables):
        """
        Adds an extension to the extension loader.
        
        Parameters
        ----------
        extension_name : `None` or `str`
            The extension's name to add.
        extension_path : `None` or `str`
            Path of the extension to add.
        entry_point : `None`, `str` or `callable`
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None`, `str` or `callable`
            Extension specific exit point, to use over the extension loader's default.
        extend_default_variables : `bool`
            Whether the extension should use the loader's default variables or just it's own's.
        locked : `bool`
            Whether the given extension(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`
            Whether snapshot feature should be used.
        default_variables : `None` or `HybridValueDictionary` of (`str`, `Any`) items
            An optionally weak value dictionary to store objects for assigning them to modules before loading them.
            If would be empty, is set as `None` instead.
        """
        extension = Extension(extension_name, extension_path, entry_point, exit_point, extend_default_variables,
            locked, take_snapshot_difference, default_variables)
        
        self._extensions_by_name[extension.name] = extension
        
        short_name = extension.short_name
        if (short_name is not None):
            self._extensions_by_name.setdefault(extension.short_name, extension)
    
    
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
        extension_names_and_paths = set(_iter_extension_names_and_paths(name))
        
        for extension_name, extension_path in extension_names_and_paths:
            if (extension_name is None):
                extension_name = _get_path_extension_name(extension_path)
            
            try:
                extension = self._extensions_by_name[extension_name]
            except KeyError:
                continue
            
            if extension._state == EXTENSION_STATE_LOADED:
                raise RuntimeError(f'Extension `{name!r}` can not be removed, meanwhile it is loaded.')
        
        for extension_name, extension_path in extension_names_and_paths:
            if (extension_name is None):
                extension_name = _get_path_extension_name(extension_path)
            
            try:
                extension = self._extensions_by_name[extension_name]
            except KeyError:
                continue
            
            extension._unlink()
    
    
    def load_extension(self, name, *args, **kwargs):
        """
        Adds, then loads the extension.
        
        Parameters
        ----------
        name : `str` or `iterable` of `str`
            The extension's name to load.
        *args : Parameters
            Additional parameters to create the extension with.
        **kwargs : Keyword parameters
            Additional parameters to create the extension with.
        
        Other Parameters
        ----------------
        entry_point : `None`, `str` or `callable`, Optional
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None`, `str` or `callable`, Optional
            Extension specific exit point, to use over the extension loader's default.
        locked : `bool`, Optional
            Whether the given extension(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`, Optional
            Whether snapshot feature should be used.
        **variables : Keyword parameters
            Variables to assign to an extension(s)'s module before they are loaded.
            
        Raises
        ------
        ImportError
            If the given name do not refers to any loadable file.
        TypeError
            - If `entry_point` was not given as `None`, `str` or as `callable`.
            - If `entry_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `exit_point` was not given as `None`, `str` or as `callable`.
            - If `exit_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `extend_default_variables` was not given as `bool`.
            - If `locked` was not given as `bool`.
            - If `name` was not given as `str` or as `iterable` of `str`.
        ValueError
            If a variable name is would be used, what is `module` attribute.
        ExtensionError
            The extension failed to load correctly.
        """
        extension_names_and_paths = set(_iter_extension_names_and_paths(name))
        entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables = \
            validate_extension_parameters(*args, **kwargs)
        
        for extension_name, extension_path in extension_names_and_paths:
            self._add(extension_name, extension_path, entry_point, exit_point, extend_default_variables, locked,
                take_snapshot_difference, default_variables)
            
            return self.load(extension_name)
    
    def load(self, name):
        """
        Loads the extension with the given name. If the extension is already loaded, will do nothing.
        
        Parameters
        ----------
        name : `str` or `iterable` of `str`
            The extension's name.
        
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
        extensions = _get_extensions(name)
        
        task = Task(self._load(extensions), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    async def _load(self, extensions):
        """
        Loads the extension with the given name.
        
        This method is a coroutine.
        
        Parameters
        ----------
        extensions : `set` of ``Extension``
            The extension to load.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Loading the extension failed.
        """
        error_messages = None
        
        for extension in extensions:
            try:
                await self._load_extension(extension)
            except ExtensionError as err:
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(err.message)
        
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
    
    
    def unload(self, name):
        """
        Unloads the extension with the given name.
        
        Parameters
        ----------
        name : `str` or `iterable` of `str`
            The extension's name.
        
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
        extensions = _get_extensions(name)
        
        task = Task(self._unload(extensions), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    async def _unload(self, extensions):
        """
        Unloads the extension with the given name.
        
        This method is a coroutine.
        
        Parameters
        ----------
        extensions : `set` of ``Extension``
            The extension to load.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Unloading the extension failed.
        """
        error_messages = None
        
        for extension in extensions:
            try:
                await self._unload_extension(extension)
            except ExtensionError as err:
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(err.message)
        
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
    
    def reload(self, name):
        """
        Reloads the extension with the given name.
        
        Parameters
        ----------
        name : `str` or `iterable` of `str`
            The extension's name.
        
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
        extensions = _get_extensions(name)
        
        task = Task(self._reload(extensions),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread, EventThread):
            return task.async_wrap(current_thread)
        
        KOKORO.wake_up()
        task.sync_wrap().wait()
    
    
    async def _reload(self, extensions):
        """
        Reloads the extension with the given name.
        
        This method is a coroutine.
        
        Parameters
        ----------
        extensions : `set` of ``Extension``
            The extension to load.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Reloading the extension failed.
        """
        error_messages = None
        
        for extension in extensions:
            try:
                await self._unload_extension(extension)
                await self._load_extension(extension)
            except ExtensionError as err:
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(err.message)
        
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
    
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
        error_messages = None
        
        for extension in EXTENSIONS.values():
            if extension._locked:
                continue
            
            try:
                await self._load_extension(extension)
            except ExtensionError as err:
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(err.message)
        
        if (error_messages is not None):
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
        
        for extension in EXTENSIONS.values():
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
        
        for extension in EXTENSIONS.values():
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
        self._execute_counter += 1
        try:
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
                
                if is_coroutine_function(entry_point):
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
        finally:
            self._execute_counter -= 1
    
    
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
        self._execute_counter += 1
        try:
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
                    
                    if is_coroutine_function(exit_point):
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
        finally:
            self._execute_counter -= 1
    
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
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' extension count=',
            repr(len(EXTENSIONS)),
        ]
        
        entry_point = self._default_entry_point
        if (entry_point is not None):
            repr_parts.append(', default_entry_point=')
            repr_parts.append(repr(entry_point))
        
        exit_point = self._default_exit_point
        if (exit_point is not None):
            repr_parts.append(', default_exit_point=')
            repr_parts.append(repr(exit_point))
        
        default_variables = self._default_variables
        if default_variables:
            repr_parts.append(', default_variables=')
            repr_parts.append(repr(default_variables))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def is_processing_extension(self):
        """
        Returns whether the extension loader is processing an extension.
        
        Returns
        -------
        is_processing_extension : `bool`
        """
        if self._execute_counter:
            is_processing_extension = True
        else:
            is_processing_extension = False
        
        return is_processing_extension
    
    
    def get_extension(self, name):
        """
        Returns the extension loader's extension with the given name.
        
        Parameters
        ----------
        name : `str`
            An extension's name.
        
        Returns
        -------
        extension : ``Extension`` or `None`.
            The matched extension if any.
        """
        return self._extensions_by_name.get(name, None)


EXTENSION_LOADER = ExtensionLoader()
export(EXTENSION_LOADER, 'EXTENSION_LOADER')
