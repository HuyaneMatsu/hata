__all__ = ('EXTENSION_LOADER', 'ExtensionLoader', )

from functools import partial as partial_func

from scarletio import (
    HybridValueDictionary, RichAttributeErrorBaseType, Task, alchemy_incendiary, export, is_coroutine_function,
    render_exception_into, run_coroutine, shield
)

from ...discord.core import KOKORO

from .constants import EXTENSION_STATE_LOADED, EXTENSIONS
from .exceptions import ExtensionError
from .extension import Extension, __file__ as EXTENSION_LOADER_EXTENSION_FILE_PATH
from .helpers import (
    PROTECTED_NAMES, _build_extension_tree, _get_extension_name_and_path, _get_path_extension_name,
    _iter_extension_names_and_paths, _validate_entry_or_exit, validate_extension_parameters
)


EXTENSION_LOADER_EXTENSION_LOADER_FILE_PATH = __file__


def _render_exception_message(exception, header):
    """
    Renders an exception' traceback.
    
    Parameters
    ----------
    exception : `BaseException`
        The exception to render.
    header : `list` of `str`
        Header of the rendered traceback.
    
    Returns
    -------
    message : `str`
        The `exception`'s rendered traceback.
    
    Notes
    -----
    This function should run in an executor.
    """
    return ''.join(render_exception_into(exception, header, filter=_ignore_module_import_frames))


async def _render_exception_message_async(exception, header):
    """
    Returns the exception message inside of an executor.
    
    Parameters
    ----------
    exception : `BaseException`
        The exception to render.
    header : `list` of `str`
        Header of the rendered traceback.
    
    Returns
    -------
    message : `str`
        The `exception`'s rendered traceback.
    """
    return await KOKORO.run_in_executor(alchemy_incendiary(_render_exception_message, (exception, header)))


def _try_get_extension(extension_name, extension_path):
    """
    Tries to get extension for the given name or path.
    
    Parameters
    ----------
    extension_name : `None`, `str`
        Extension's  name.
    extension_path : `str`
        Path of the extension file.
    
    Returns
    -------
    extension : `None`, ``Extension``
        The found extension if any.
    """
    try:
        return EXTENSION_LOADER._extensions_by_name[extension_path]
    except KeyError:
        pass
    
    if extension_name is None:
        extension_name = _get_path_extension_name(extension_path)
    
    try:
        return EXTENSION_LOADER._extensions_by_name[extension_name]
    except KeyError:
        pass


async def _get_extensions(name, deep):
    """
    Gets the extensions with the given name.
    
    Parameters
    ----------
    name : `str`, `iterable` of `str`
        Extension by name to find.
    deep : `bool`
        Whether the extension with all of it's parent and with their child should be returned.
    
    Returns
    -------
    extensions : `list` of ``Extension``
        The found extensions.
    
    Raises
    ------
    ExtensionError
        If an extension could not be found.
    """
    try:
        extensions = set()
        
        extension_names_and_paths = set(_iter_extension_names_and_paths(name))
        for extension_name, extension_path in extension_names_and_paths:
            extension = _try_get_extension(extension_name, extension_path)
            if extension is None:
                raise ExtensionError(f'No extension was added with name: `{extension_name}`.')
            
            extensions.add(extension)
            continue
        
        if not extensions:
            raise ExtensionError(
                f'No extensions found with the given name: {name!r}.'
            )
        
        return _build_extension_tree(extensions, deep)
    
    except GeneratorExit:
        raise
    
    except ExtensionError:
        raise
    
    except BaseException as err:
        message = await _render_exception_message_async(
            err,
            [
                'Exception occurred meanwhile looking up extensions for name: `',
                repr(name),
                '`.\n',
            ]
        )
        
        raise ExtensionError(message)


def _ignore_module_import_frames(file_name, name, line_number, line):
    """
    Ignores import frames of extension loading.
    
    Parameters
    ----------
    file_name : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line_number : `int`
        The line's index where the exception occurred.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    if file_name.startswith('<') and file_name.endswith('>'):
        should_show_frame = False
    
    elif file_name == EXTENSION_LOADER_EXTENSION_FILE_PATH:
        if name == '_load':
            if line == 'loaded = self._load_module()':
                should_show_frame = False
        
        elif name == '_load_module':
            if line == 'spec.loader.exec_module(module)':
                should_show_frame = False
    
    elif file_name == EXTENSION_LOADER_EXTENSION_LOADER_FILE_PATH:
        if name == '_extension_loader_task':
            if line in (
                'module = await KOKORO.run_in_executor(extension._load)',
                'await entry_point(module)',
                'entry_point(module)',
            ):
                should_show_frame = False
        
        elif name == '_extension_unloader_task':
            if line in (
                'await exit_point(module)',
                'exit_point(module)',
            ):
                should_show_frame = False
    
    return should_show_frame


def _pop_unloader_task_callback(extension, task):
    """
    Removes the unloader task of the extension loader for the given extension.
    
    Parameters
    ----------
    extension : ``Extension``
        The extension to remove it's task of.
    task : ``Task``
        The finished task.
    """
    try:
        del EXTENSION_LOADER._unloader_tasks[extension]
    except KeyError:
        pass


def _pop_loader_task_callback(extension, task):
    """
    Removes the loader task of the extension loader for the given extension.
    
    Parameters
    ----------
    extension : ``Extension``
        The extension to remove it's task of.
    task : ``Task``
        The finished task.
    """
    try:
        del EXTENSION_LOADER._loader_tasks[extension]
    except KeyError:
        pass


def _run_maybe_blocking(coroutine, blocking):
    """
    Starts the given coroutine inside of a task. Returns a wrapped task, or it's result depending from where it was
    called.
    
    Parameters
    ----------
    coroutine : `CoroutineType`
        The coroutine to run.
    blocking : `bool`
        Whether the operation should be blocking when called from a non-async thread.
    
    Returns
    -------
    result : `None`, ``Task``, ``FutureAsyncWrapper``
    """
    if blocking:
        return run_coroutine(coroutine, KOKORO)
    else:
        return KOKORO.create_task_thread_safe(coroutine)


class ExtensionLoader(RichAttributeErrorBaseType):
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
    now = datetime.utcnow()
    
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
      File ".../hata/ext/extension_loader/extension_loader.py", line 652, in reload_all
        task.sync_wrap().wait()
      File ".../scarletio/core/traps/future_sync_wrapper.py", line 823, in wait
        return self.result()
      File ".../scarletio/core/traps/future_sync_wrapper.py", line 723, in result
        raise exception
      File ".../scarletio/core/traps/task.py", line 1602, in _step
        result = coroutine.throw(exception)
      File ".../hata/ext/extension_loader/extension_loader.py", line 670, in _reload_all_task
        raise ExtensionError(error_messages) from None
    hata.ext.extension_loader.ExtensionError: ExtensionError (1):
    Exception occurred meanwhile loading an extension: `extension`.
    
    Traceback (most recent call last):
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
    `str` or not `iterable` of `str`, `TypeError` is raised.
    
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
    the client's thread, a ``Task`` is returned what can be `awaited`. If called from other ``EventThread``, then the
    task is async wrapped and that is returned. When calling from any other thread (like the main thread for example),
    the task is sync wrapped and the thread is blocked till the extension's loading is finished.
    
    Attributes
    ----------
    _default_entry_point : `None`, `str`, `callable`
        Internal slot for the ``.default_entry_point`` property.
    _default_exit_point : `None`, `str`, `callable`
        Internal slot for the ``.default_exit_point`` property.
    _default_variables : `None`, `HybridValueDictionary` of (`str`, `Any`) items
        An optionally weak value dictionary to store objects for assigning them to modules before loading them.
        If it would be set as empty, then it is set as `None` instead.
    _done_callbacks : `None`, `list` of `callable`
        Callbacks, which run when loading / unloading the extensions is done.
        
        > These callbacks are only called once, and then cleared out.
    _execute_counter : `int`
        Whether the extension loader is executing an extension.
    _extensions_by_name : `dict` of (`str`, ``Extension``) items
        A dictionary of the added extensions to the extension loader in `extension-name` - ``Extension`` relation.
    _loader_tasks : `dict` of (``Extension``, ``Task``) items
        Active extension loading tasks.
    _unloader_tasks : `dict` of (``Extension``, ``Task``) items
        Active extension unloading tasks.
    
    Class Attributes
    ---------------
    _instance : `None`, ``ExtensionLoader``
        The already created instance of the ``ExtensionLoader`` if there is any.
    """
    __slots__ = (
        '_default_entry_point', '_default_exit_point', '_default_variables', '_done_callbacks', '_execute_counter',
        '_extensions_by_name', '_loader_tasks', '_unloader_tasks'
    )
    
    _instance = None
    
    def __new__(cls):
        """
        Creates an ``ExtensionLoader``. If the `ExtensionLoader` was instanced already, then returns that
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
            self._done_callbacks = None
            self._extensions_by_name = {}
            self._default_variables = HybridValueDictionary()
            self._execute_counter = 0
            self._loader_tasks = {}
            self._unloader_tasks = {}
            
            cls._instance = self
        
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
            raise TypeError(
                f'`{self.__class__.__name__}.default_entry_point` can be `None`, `str`, `callable`, got '
                f'{default_entry_point.__class__.__name__}; {default_entry_point!r}.'
            )
        
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
            raise TypeError(
                f'`{self.__class__.__name__}.default_exit_point` can be `None`, `str`, `callable`, got '
                f'{default_exit_point.__class__.__name__}; {default_exit_point!r}.'
            )
        
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
                raise ValueError(
                    f'The passed {key!r} is a protected variable name of module type.'
                )
            
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
        
        If the extension already exists, returns that one.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension's name to load.
        *args : Parameters
            Additional parameters to create the extension with.
        **kwargs : Keyword parameters
            Additional parameters to create the extension with.
        
        Other Parameters
        ----------------
        entry_point : `None`, `str`, `callable`, Optional
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None`, `str`, `callable`, Optional
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
            - If `entry_point` was not given as `None`, `str`, `callable`.
            - If `entry_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `exit_point` was not given as `None`, `str`, `callable`.
            - If `exit_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `extend_default_variables` was not given as `bool`.
            - If `locked` was not given as `bool`.
            - If `name` was not given as `str`, `iterable` of `str`.
        ValueError
            If a variable name is would be used, what is `module` attribute.
        """
        extension_names_and_paths = set(_iter_extension_names_and_paths(name, register_directories_as_roots=True))
        entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables = \
            validate_extension_parameters(*args, **kwargs)
        
        for extension_name, extension_path in extension_names_and_paths:
            self._add(
                extension_name, extension_path, entry_point, exit_point, extend_default_variables, locked,
                take_snapshot_difference, default_variables
            )
    
    
    def _add(self, extension_name, extension_path, entry_point, exit_point, extend_default_variables, locked,
            take_snapshot_difference, default_variables):
        """
        Adds an extension to the extension loader.
        
        If the extension already exists, returns that one.
        
        Parameters
        ----------
        extension_name : `None`, `str`
            The extension's name to add.
        extension_path : `None`, `str`
            Path of the extension to add.
        entry_point : `None`, `str`, `callable`
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None`, `str`, `callable`
            Extension specific exit point, to use over the extension loader's default.
        extend_default_variables : `bool`
            Whether the extension should use the loader's default variables or just it's own.
        locked : `bool`
            Whether the given extension(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`
            Whether snapshot feature should be used.
        default_variables : `None`, `HybridValueDictionary` of (`str`, `Any`) items
            An optionally weak value dictionary to store objects for assigning them to modules before loading them.
            If would be empty, is set as `None` instead.
        
        Returns
        -------
        extension : ``Extension``
            The registered extension.
        """
        extension = Extension(
            extension_name, extension_path, entry_point, exit_point, extend_default_variables,
            locked, take_snapshot_difference, default_variables
        )
        
        self._extensions_by_name[extension.name] = extension
        self._extensions_by_name[extension.file_name] = extension
        
        short_name = extension.short_name
        if (short_name is not None):
            self._extensions_by_name.setdefault(extension.short_name, extension)
        
        return extension
    
    
    def remove(self, name):
        """
        Removes one or more extensions from the extension loader.
        
        If any of the extensions is not found, no errors will be raised.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension(s)'s name(s) to remove.
        
        Raises
        ------
        TypeError
            If `name` was not given as `str`, `iterable` of `str`.
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
                raise RuntimeError(
                    f'Extension `{name!r}` can not be removed meanwhile it is loaded.'
                )
        
        for extension_name, extension_path in extension_names_and_paths:
            if (extension_name is None):
                extension_name = _get_path_extension_name(extension_path)
            
            try:
                extension = self._extensions_by_name[extension_name]
            except KeyError:
                continue
            
            extension._unlink()
    
    
    def load_extension(self, name, *parameters, blocking=True, **keyword_parameters):
        """
        Adds, then loads the extension.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension's name to load.
        
        *parameters : Parameters
            Additional parameters to create the extension with.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to create the extension with.
        
        Other Parameters
        ----------------
        entry_point : `None`, `str`, `callable`, Optional
            Extension specific entry point, to use over the extension loader's default.
        exit_point : `None`, `str`, `callable`, Optional
            Extension specific exit point, to use over the extension loader's default.
        locked : `bool`, Optional
            Whether the given extension(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`, Optional
            Whether snapshot feature should be used.
        **variables : Keyword parameters
            Variables to assign to an extension(s)'s module before they are loaded.
        
        Returns
        -------
        task : `set` of ``Extension``, ``Task`` -> ``Extension``, ``FutureAsyncWrapper`` -> ``Extension``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
            
            When finished returns the loaded extension.
        
        Raises
        ------
        ImportError
            If the given name do not refers to any loadable file.
        TypeError
            - If `entry_point` was not given as `None`, `str`, `callable`.
            - If `entry_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `exit_point` was not given as `None`, `str`, `callable`.
            - If `exit_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `extend_default_variables` was not given as `bool`.
            - If `locked` was not given as `bool`.
            - If `name` was not given as `str`, `iterable` of `str`.
        ValueError
            If a variable name is would be used, what is `module` attribute.
        ExtensionError
            The extension failed to load correctly.
        """
        return _run_maybe_blocking(self._load_extension_task(name, parameters, keyword_parameters), blocking)
    
    
    async def _load_extension_task(self, name, parameters, keyword_parameters):
        """
        Adds, then loads the extension.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`
            The extension's name.
        parameters : `tuple` of `Any`
            Additional parameters to create the extension with.
        keyword_parameters : `dict` of (`str`, `Any`) items
            Additional parameters to create the extension with.
        
        Returns
        -------
        extension : ``Extension``
            The loaded extension.
        
        Raises
        ------
        ImportError
            If the given name do not refers to any loadable file.
        TypeError
            - If `entry_point` was not given as `None`, `str`, `callable`.
            - If `entry_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `exit_point` was not given as `None`, `str`, `callable`.
            - If `exit_point` was given as `callable`, but accepts less or more positional parameters, as would be
                given.
            - If `extend_default_variables` was not given as `bool`.
            - If `locked` was not given as `bool`.
            - If `name` was not given as `str`, `iterable` of `str`.
        ValueError
            If a variable name is would be used, what is `module` attribute.
        ExtensionError
            The extension failed to load correctly.
        """
        extension_name, extension_path = _get_extension_name_and_path(name)
        extension = _try_get_extension(extension_name, extension_path)
        
        entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables = \
            validate_extension_parameters(*parameters, **keyword_parameters)
    
        if (extension is None):
            extension = self._add(
                extension_name, extension_path, entry_point, exit_point, extend_default_variables, locked,
                take_snapshot_difference, default_variables
            )
            
        else:
            if (default_variables is not None):
                extension.add_default_variables(**default_variables)
            
            if extension.is_loaded():
                return extension
        
        extension_error = await self._extension_loader(extension)
        if (extension_error is not None):
            raise extension_error
        
        return extension
    
    
    def load(self, name, *, blocking=True, deep=True):
        """
        Loads the extension with the given name. If the extension is already loaded, will do nothing.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension's name.
        deep : `bool` = `True`, Optional (Keyword only)
            Whether the extension with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        task : `list` of ``Extension``, ``Task`` -> `list` of ``Extension``,
                ``FutureAsyncWrapper`` -> `list` of ``Extension``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
            
            When finished returns the loaded extension.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Loading the extension failed.
        """
        return _run_maybe_blocking(self._load_task(name, deep), blocking)
    
    
    async def _load_task(self, name, deep):
        """
        Loads the given extensions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str'
            The extension(s) name to load.
        deep : `bool`
            Whether the extension with all of it's parent and with their child should be reloaded.

        Returns
        -------
        extensions : `list` of ``Extension``
            The loaded extensions.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Loading the extension failed.
        """
        extensions = await _get_extensions(name, deep)
        
        error_messages = None
        
        for extension in extensions:
            exception = await self._extension_loader(extension)
            if (exception is not None):
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(exception.message)
        
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
        
        return extensions
    
    
    def unload(self, name, *, blocking=True, deep=True):
        """
        Unloads the extension with the given name.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension's name.
        
        deep : `bool` = `True`, Optional (Keyword only)
            Whether the extension with all of it's parent and with their child should be reloaded.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Returns
        -------
        task : `list` of ``Extension``, ``Task`` -> `list` of ``Extension``,
                ``FutureAsyncWrapper`` -> `list` of ``Extension``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            unloading is done. However if called from a sync thread, will block till the unloading is done.
            
            When finished returns the unloaded extension.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Unloading the extension failed.
        """
        return _run_maybe_blocking(self._unload_task(name, deep), blocking)
    
    
    async def _unload_task(self, name, deep):
        """
        Unloads the extension with the given name.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension's name.
        deep : `bool`
            Whether the extension with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        extensions : `list` of ``Extension``
            The unloaded extensions.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Unloading the extension failed.
        """
        extensions = await _get_extensions(name, deep)
        
        error_messages = None
        
        for extension in extensions:
            exception = await self._extension_unloader(extension)
            if (exception is not None):
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(exception.message)
        
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
        
        return extensions
    
    
    def reload(self, name, *, blocking=True, deep=True):
        """
        Reloads the extension with the given name.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension's name.

        deep : `bool` = `True`, Optional (Keyword only)
            Whether the extension with all of it's parent and with their child should be reloaded.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Returns
        -------
        task : `list` of ``Extension``, ``Task`` -> `list` of ``Extension``,
                ``FutureAsyncWrapper`` -> `list` of ``Extension``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            reloading is done. However if called from a sync thread, will block till the reloading is done.
            
            When finished returns the reloaded extensions.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Reloading the extension failed.
        """
        return _run_maybe_blocking(self._reload_task(name, deep), blocking)
    
    
    async def _reload_task(self, name, deep):
        """
        Reloads the extension with the given name.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The extension's name.
        deep : `bool`
            Whether the extension with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        extensions : `list` of ``Extension``
            The reloaded extensions.
        
        Raises
        ------
        ExtensionError
            - No extension is added with the given name.
            - Reloading the extension failed.
        """
        extensions = await _get_extensions(name, deep)
        
        await self._check_for_syntax(extensions)
        
        error_messages = None
        
        for extension in extensions:
            exception = await self._extension_unloader(extension)
            if (exception is not None):
                if error_messages is None:
                    error_messages = {}
                
                error_messages[extension.name] = exception.message
        
        
        for extension in extensions:
            if (error_messages is not None) and (extension.name in error_messages):
                continue
            
            exception = await self._extension_loader(extension)
            if (exception is not None):
                if error_messages is None:
                    error_messages = {}
                
                error_messages[extension.name] = exception.message
        
        if (error_messages is not None):
            raise ExtensionError([*error_messages.values()]) from None
        
        return extensions
    
    
    def load_all(self, *, blocking=True):
        """
        Loads all the extension of the extension loader. If anything goes wrong, raises an ``ExtensionError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Raises
        ------
        ExtensionError
            If any extension failed to load correctly.
        """
        return _run_maybe_blocking(self._load_all_task(), blocking)
    
    
    async def _load_all_task(self):
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
        
        for extension in tuple(EXTENSIONS.values()):
            if extension._locked:
                continue
            
            exception = await self._extension_loader(extension)
            if (exception is not None):
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(exception.message)
        
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
    
    
    def unload_all(self, *, blocking=True):
        """
        Unloads all the extension of the extension loader. If anything goes wrong, raises an ``ExtensionError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            unloading is done. However if called from a sync thread, will block till the unloading is done.
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Raises
        ------
        ExtensionError
            If any extension failed to unload correctly.
        """
        return _run_maybe_blocking(self._unload_all_task(), blocking)
    
    
    async def _unload_all_task(self):
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
        error_messages = None
        
        for extension in tuple(EXTENSIONS.values()):
            if extension._locked:
                continue
            
            exception = await self._extension_unloader(extension)
            if (exception is not None):
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(exception.message)
            
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
    
    
    def reload_all(self, *, blocking=True):
        """
        Reloads all the extension of the extension loader. If anything goes wrong, raises an ``ExtensionError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            reloading is done. However if called from a sync thread, will block till the reloading is done.
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Raises
        ------
        ExtensionError
            If any extension failed to reload correctly.
        """
        return _run_maybe_blocking(self._reload_all_task(), blocking)
    
    
    async def _reload_all_task(self):
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
        error_messages = None
        
        extensions = _build_extension_tree(
            [extension for extension in EXTENSIONS.values() if not extension._locked],
            False,
        )
        await self._check_for_syntax(extensions)
        
        for extension in extensions:
            exception = await self._extension_unloader(extension)
            if (exception is None):
                exception = await self._extension_loader(extension)
            
            if (exception is not None):
                if error_messages is None:
                    error_messages = []
                
                error_messages.append(exception.message)
        
        if (error_messages is not None):
            raise ExtensionError(error_messages) from None
    
    
    async def _extension_loader(self, extension):
        """
        Loads the given extension. This method synchronises extension loading.
        
        This method is a coroutine.
        
        Parameters
        ----------
        extension : ``Extension``
            The extension to unload.
        
        Returns
        -------
        exception : `None`, ``ExtensionError``
        """
        try:
            unloader_task = self._unloader_tasks[extension]
        except KeyError:
            pass
        else:
            try:
                exception = await shield(unloader_task, KOKORO)
            except:
                raise
            else:
                if (exception is not None):
                    return exception
            
            finally:
                unloader_task = None
            
        try:
            loader_task = self._loader_tasks[extension]
        except KeyError:
            loader_task = Task(self._extension_loader_task(extension), KOKORO)
            loader_task.add_done_callback(partial_func(_pop_loader_task_callback, extension))
            
            self._loader_tasks[extension] = loader_task
        
        try:
            return await shield(loader_task, KOKORO)
        finally:
            loader_task = None
    
    
    async def _extension_loader_task(self, extension):
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
        
        Returns
        -------
        exception : `None`, ``ExtensionError``
        """
        self._execute_counter += 1
        try:
            try:
                # loading blocks, but unloading does not
                module = await KOKORO.run_in_executor(extension._load)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                message = await _render_exception_message_async(
                    err,
                    [
                        'Exception occurred meanwhile loading an extension: `',
                        extension.name,
                        '`.\n\n',
                    ],
                )
                
                return ExtensionError(message)
            
            if module is None:
                return # already loaded
            
            entry_point = extension._entry_point
            if entry_point is None:
                entry_point = self._default_entry_point
                if entry_point is None:
                    return
            
            if isinstance(entry_point, str):
                entry_point = getattr(module, entry_point, None)
                if entry_point is None:
                    return
            
            try:
                if is_coroutine_function(entry_point):
                    await entry_point(module)
                else:
                    entry_point(module)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                message = await _render_exception_message_async(
                    err,
                    [
                        'Exception occurred meanwhile entering an extension: `',
                        extension.name,
                        '`.\nAt entry_point:',
                        repr(entry_point),
                        '\n\n',
                    ],
                )
                
                return ExtensionError(message)
        finally:
            execute_counter = self._execute_counter - 1
            self._execute_counter = execute_counter
            if not execute_counter:
                self.call_done_callbacks()
    
    
    async def _extension_unloader(self, extension):
        """
        Unloads the given extension. This method synchronises extension unloading.
        
        This method is a coroutine.
        
        Parameters
        ----------
        extension : ``Extension``
            The extension to unload.
        
        Returns
        -------
        exception : `None`, ``ExtensionError``
        """
        try:
            loader_task = self._loader_tasks[extension]
        except KeyError:
            pass
        else:
            try:
                exception = await shield(loader_task, KOKORO)
            except:
                raise
            else:
                if (exception is not None):
                    return exception
            
            finally:
                loader_task = None
        
        try:
            unloader_task = self._unloader_tasks[extension]
        except KeyError:
            unloader_task = Task(self._extension_unloader_task(extension), KOKORO)
            unloader_task.add_done_callback(partial_func(_pop_unloader_task_callback, extension, ))
            
            self._unloader_tasks[extension] = unloader_task
        
        try:
            return await shield(unloader_task, KOKORO)
        finally:
            unloader_task = None

    
    async def _extension_unloader_task(self, extension):
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
        
        Returns
        -------
        exception : `None`, ``ExtensionError``
        """
        self._execute_counter += 1
        try:
            # loading blocks, but unloading does not
            module = extension._unload()
            
            if module is None:
                return # not loaded
            
            try:
                exit_point = extension._exit_point
                if exit_point is None:
                    exit_point = self._default_exit_point
                    if exit_point is None:
                        return
                
                if isinstance(exit_point, str):
                    exit_point = getattr(module, exit_point, None)
                    if exit_point is None:
                        return
                
                try:
                    
                    if is_coroutine_function(exit_point):
                        await exit_point(module)
                    else:
                        exit_point(module)
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    message = await _render_exception_message_async(
                        err,
                        [
                            'Exception occurred meanwhile unloading an extension: `',
                            extension.name,
                            '`.\nAt exit_point:',
                            repr(exit_point),
                            '\n\n',
                        ],
                    )
                    
                    return ExtensionError(message)
            
            finally:
                extension._unassign_variables()
                
                keys = []
                module_globals = module.__dict__
                for key in module_globals:
                    if (not key.startswith('__')) and (not key.endswith('__')):
                        keys.append(key)
                
                for key in keys:
                    del module_globals[key]
        finally:
            execute_counter = self._execute_counter - 1
            self._execute_counter = execute_counter
            if not execute_counter:
                self.call_done_callbacks()
    
    
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
        extension : ``Extension``, `None`.
            The matched extension if any.
        """
        return self._extensions_by_name.get(name, None)
    
    
    async def _check_for_syntax(self, extensions):
        """
        Checks whether the extensions can be reloaded.
        
        This function is a coroutine.
        
        Parameters
        ----------
        extensions : `list` of ``Extension``
            A list of extensions to check their syntax.
        
        Raises
        ------
        SyntaxError
        """
        return await KOKORO.run_in_executor(alchemy_incendiary(self._check_for_syntax_blocking, (extensions,)))
    
    
    def _check_for_syntax_blocking(self, extensions):
        """
        Checks whether the extensions can be reloaded.
        
        This method is blocking and ran inside of an executor by ``._check_for_syntax``.
        
        Parameters
        ----------
        extensions : `list` of ``Extension``
            A list of extensions to check their syntax.
        
        Raises
        ------
        SyntaxError
        """
        for extension in extensions:
            extension._check_for_syntax()
    
    
    def add_done_callback(self, callback):
        """
        Adds a done callback to be called when the loading / unloading extensions is finished.
        
        These callbacks are only called once, and then cleared out.
        
        Parameters
        ----------
        callback : `callable`
        
        Returns
        -------
        added : `bool`
            Whether the callback was added.
        """
        done_callbacks = self._done_callbacks
        if (done_callbacks is None):
            done_callbacks = []
            self._done_callbacks = done_callbacks
        
        done_callbacks.append(callback)
        return True
    
    
    def add_done_callback_unique(self, callback):
        """
        Adds a done callback to be called when the loading / unloading extensions is finished.
        
        > Ff the callback is already added, does nothing.
        
        These callbacks are only called once, and then cleared out.
        
        Parameters
        ----------
        callback : `callable`
        
        Returns
        -------
        added : `bool`
            Whether the callback was added.
        """
        done_callbacks = self._done_callbacks
        if (done_callbacks is None):
            done_callbacks = []
            self._done_callbacks = done_callbacks
        
        else:
            if (callback in done_callbacks):
                return False
        
        done_callbacks.append(callback)
        return True
    
    
    def call_done_callbacks(self):
        """
        Calls done callbacks of the extension loader.
        """
        done_callbacks = self._done_callbacks
        if (done_callbacks is not None):
            self._done_callbacks = done_callbacks
            
            for done_callback in done_callbacks:
                KOKORO.call_soon(done_callback)


EXTENSION_LOADER = ExtensionLoader()
export(EXTENSION_LOADER, 'EXTENSION_LOADER')
