__all__ = ('PLUGIN_LOADER', 'PluginLoader', )

from functools import partial as partial_func
from itertools import chain
from os.path import isfile as is_file

from scarletio import (
    CauseGroup, HybridValueDictionary, RichAttributeErrorBaseType, Task, alchemy_incendiary, export,
    is_coroutine_function, run_coroutine, shield
)

from ...discord.core import KOKORO

from .constants import (
    PLUGINS, PLUGIN_ACTION_FLAG_LOAD, PLUGIN_ACTION_FLAG_SYNTAX_CHECK, PLUGIN_ACTION_FLAG_UNLINK,
    PLUGIN_ACTION_FLAG_UNLOAD, PLUGIN_STATE_LOADED
)
from .exceptions import PluginError
from .helpers import (
    PROTECTED_NAMES, _add_plugin_name_to_plugin_root_names, _get_plugin_name_and_path,
    _is_plugin_name_in_plugin_root_names, _try_get_plugin, _validate_entry_or_exit, validate_plugin_parameters
)
from .plugin import Plugin
from .plugin_extractor import PluginExtractor
from .plugin_tree.plugin_tree_helpers import (
    _build_and_sort_plugin_trees, _sort_plugin_trees, _unwrap_plugin_trees_into_plugins
)
from .plugin_tree.plugin_tree_iterator import PluginTreeIterator


def _pop_unloader_task_callback(plugin, task):
    """
    Removes the unloader task of the plugin loader for the given plugin.
    
    Parameters
    ----------
    plugin : ``Plugin``
        The plugin to remove it's task of.
    task : ``Task``
        The finished task.
    """
    try:
        del PLUGIN_LOADER._unloader_tasks[plugin]
    except KeyError:
        pass


def _pop_loader_task_callback(plugin, task):
    """
    Removes the loader task of the plugin loader for the given plugin.
    
    Parameters
    ----------
    plugin : ``Plugin``
        The plugin to remove it's task of.
    task : ``Task``
        The finished task.
    """
    try:
        del PLUGIN_LOADER._loader_tasks[plugin]
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
    result : `None`, ``Task``, ``FutureWrapperAsync``
    """
    if blocking:
        return run_coroutine(coroutine, KOKORO)
    else:
        return KOKORO.create_task_thread_safe(coroutine)


class PluginLoader(RichAttributeErrorBaseType):
    """
    There are some cases when you probably want to change some functional part of your client in runtime. Load,
    unload or reload code. Hata provides an easy to use (that's what she said) solution to solve this issue.
    
    It is called plugin loader is a plugin of hata. It is separated from `commands` plugin, but it does not
    mean they do not go well together. But what more, plugin loader was made to complement it.
    
    Usage
    -----
    The ``PluginLoader`` class is instanced already as `PLUGIN_LOADER` and that can be imported as well from
    `plugin_loader.py`. Instancing the class again will yield the same object.
    
    Because hata can have more clients, we needed a special plugin loader what can handle using more clients at any
    file, so the choice ended up on a  really interesting idea: assign variables to a module before it is (re)loaded.
    
    To show this is not blackmagic, here is an example:
    
    **main.py**
    
    ```py
    from hata.ext.plugin_loader import PLUGIN_LOADER
    from datetime import datetime
    
    cake = 'cake'
    now = datetime.utcnow()
    
    PLUGIN_LOADER.add_default_variables(cake = cake, now = now)
    PLUGIN_LOADER.register_and_load('plugin')
    ```
    
    **plugin.py**
    
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
    >>> PLUGIN_LOADER.add_default_variables(cake = 'cakes taste good, and now is:')
    >>> PLUGIN_LOADER.reload_all()
    ```
    
    And a different text is printed out:
    
    ```
    cakes taste good, and now is: 2020-03-14 09:40:41.587673
    ```
    
    Now lets edit `plugin.py`.
    
    ```py
    cake = cake.split()
    print(*cake, now, sep = '\\n')
    ```
    
    And reload the plugin:
    
    ```py
    >>> PLUGIN_LOADER.reload_all()
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
    
    If you remove default variables and the plugin file still uses them, you get an ``PluginError``:
    
    ```py
    >>> PLUGIN_LOADER.remove_default_variables('cake')
    >>> PLUGIN_LOADER.reload_all()
    ```
    
    ```
    Traceback (most recent call last):
      File "<pyshell#13>", line 1, in <module>
        PLUGIN_LOADER.reload_all()
      File ".../hata/ext/plugin_loader/plugin_loader.py", line 652, in reload_all
        task.sync_wrap().wait()
      File ".../scarletio/core/traps/future_sync_wrapper.py", line 823, in wait
        return self.get_result()
      File ".../scarletio/core/traps/future_sync_wrapper.py", line 723, in result
        raise exception
      File ".../scarletio/core/traps/task.py", line 1602, in _step
        result = coroutine.throw(exception)
      File ".../hata/ext/plugin_loader/plugin_loader.py", line 670, in _reload_all_task
        raise PluginError(error_messages) from None
    hata.ext.plugin_loader.PluginError: PluginError (1):
    Exception occurred meanwhile loading a plugin: `plugin`.
    
    Traceback (most recent call last):
      File ".../plugin.py", line 1, in <module>
        cake = cake.split()
    NameError("name 'cake' is not defined")
    ```
    
    Adding Plugins
    -----------------
    Plugins can be register with the `.register` method.
    
    ```py
    PLUGIN_LOADER.register('cute_commands')
    ```
    
    Or more plugin can be added as well by passing an iterable:
    
    ```py
    PLUGIN_LOADER.register(['cute_commands', 'nice_commands'])
    ```
    
    If a plugin's file is not found, then `.register` will raise  `ModuleNotFoundError`. If the passed parameter
    is not `str` or not `iterable` of `str`, `TypeError` is raised.
    
    Loading
    -------
    Plugins can be loaded by their name:
    
    ```py
    PLUGIN_LOADER.load('cute_commands')
    ```
    
    All plugin can be loaded by using:
    
    ```py
    PLUGIN_LOADER.load_all()
    ```
    
    Or plugin can be added and loaded at the same time as well:
    
    ```py
    PLUGIN_LOADER.register_and_load('cute_commands')
    ```
    
    `.register_and_load` method supports all the keyword parameters as `.register`.
    
    ##### Passing variables to plugins
    
    You can pass variables to plugins with the `.add_default_variables` method:
    
    ```py
    PLUGIN_LOADER.add_default_variables(cake = cake, now = now)
    ```
    
    Adding or removing variables wont change the already loaded plugins' state, those needs to be reloaded to see
    them.
    
    Or pass variables to just specific plugins:
    
    ```py
    PLUGIN_LOADER.register('cute_commands', cake = cake, now = now)
    ```
    
    You can specify if the plugin should use just it's own variables and ignore the default ones too:
    
    ```py
    PLUGIN_LOADER.register('cute_commands', extend_default_variables = False, cake = cake, now = now)
    ```
    
    Every variable added is stored in an optionally weak value dictionary, but you are able remove the added variables
    as well:
    
    ```py
    PLUGIN_LOADER.remove_default_variables('cake', 'now')
    ```
    
    The plugins can be accessed by their name as well, then you can use their properties to modify them.
    
    ```py
    PLUGIN_LOADER.get_plugin('cute_commands').remove_default_variables('cake')
    ```
    
    Unloading And Exit Point
    ------------------------
    You can unload plugin on the same way as loading them.
    
    ```py
    PLUGIN_LOADER.unload('cute_commands')
    ```
    
    Or unload all:
    
    ```py
    PLUGIN_LOADER.unload_all()
    ```
    
    When unloading a plugin, the plugin loader will search a function at the plugin, what we call
    `exit_point` and will run it. By default it looks for a variable named `teardown`. `exit_point` acts on the same
    way as the `entry_point`, so it can be modified for looking for other name to defining and passing a callable
    (can be async again).
    
    Can be set almost on the same way as well:
    
    ```py
    PLUGIN_LOADER.default_exit_point = 'exit'
    ```
    
    Or:
    
    ```py
    PLUGIN_LOADER.register('cute_commands', exit_point = 'exit')
    ```
    
    There are also methods for reloading: `.reload(name)` and `.reload_all()`
    
    Removing Plugins
    -------------------
    
    Unloaded plugins can be removed from the plugin loader by using the `.remove` method:
    
    ```py
    PLUGIN_LOADER.remove('cute_commands')
    ```
    
    Or more plugin with an iterable:
    
    ```py
    PLUGIN_LOADER.remove(['cute_commands', 'nice_commands'])
    ```
    
    Removing loaded plugin will yield `RuntimeError`.
    
    Threading Model
    ---------------
    When you call the different methods of the plugin loader, they ll run on the ``Clients`` thread, what is named
    `KOKORO` internally.
    
    These methods are:
    - ``.register_and_load``
    - ``.load``
    - ``.load_all``
    - ``.unload``
    - ``.unload_all``
    - ``.reload``
    - ``.reload_all``
    
    Meanwhile loading and executing the plugin's code the thread is switched to an executor, so blocking tasks can
    be executed easily. The exception under this rule are the `entry_point`-s and the `exit_point`-s, which always run
    on the same thread as the clients, that is why they can be async as well.
    
    These methods also act differently depending from which thread they were called from. Whenever they are called from
    the client's thread, a ``Task`` is returned what can be `awaited`. If called from other ``EventThread``, then the
    task is async wrapped and that is returned. When calling from any other thread (like the main thread for example),
    the task is sync wrapped and the thread is blocked till the plugin's loading is finished.
    
    Attributes
    ----------
    _default_entry_point : `None`, `str`, `callable`
        Internal slot for the ``.default_entry_point`` property.
    _default_exit_point : `None`, `str`, `callable`
        Internal slot for the ``.default_exit_point`` property.
    _default_variables : `None`, `HybridValueDictionary` of (`str`, `object`) items
        An optionally weak value dictionary to store objects for assigning them to modules before loading them.
        If it would be set as empty, then it is set as `None` instead.
    _done_callbacks : `None`, `list` of `callable`
        Callbacks, which run when loading / unloading the plugins is done.
        
        > These callbacks are only called once, and then cleared out.
    _execute_counter : `int`
        Whether the plugin loader is executing a plugin.
    _loader_tasks : `dict` of (``Plugin``, ``Task``) items
        Active plugin loading tasks.
    _plugins_by_name : `dict` of (`str`, ``Plugin``) items
        A dictionary of the added plugins to the plugin loader in `plugin-name` - ``Plugin`` relation.
    _previously_failed_load_trees : `None`, `set` of ``PluginTree``
        Previously failed plugin trees on load (and syntax check).
    _unloader_tasks : `dict` of (``Plugin``, ``Task``) items
        Active plugin unloading tasks.
    
    Class Attributes
    ---------------
    _instance : `None`, ``PluginLoader``
        The already created instance of the ``PluginLoader`` if there is any.
    """
    __slots__ = (
        '_default_entry_point', '_default_exit_point', '_default_variables', '_done_callbacks', '_execute_counter',
        '_loader_tasks', '_plugins_by_name', '_previously_failed_load_trees', '_unloader_tasks'
    )
    
    _instance = None
    
    def __new__(cls):
        """
        Creates an ``PluginLoader``. If the `PluginLoader` was instanced already, then returns that
        instead.
        
        Returns
        -------
        self : ``PluginLoader``
        """
        self = cls._instance
        if self is not None:
            return self
        
        self = object.__new__(cls)
        
        self._default_entry_point = 'setup'
        self._default_exit_point = 'teardown'
        self._done_callbacks = None
        self._plugins_by_name = {}
        self._default_variables = HybridValueDictionary()
        self._execute_counter = 0
        self._loader_tasks = {}
        self._unloader_tasks = {}
        self._previously_failed_load_trees = None
        
        cls._instance = self
        return self
    
    
    @property
    def default_entry_point(self):
        """
        Get-set-del descriptor for modifying the plugin loader's default entry point.
        
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
        Get-set-del descriptor for modifying the plugin loader's default exit point.
        
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
        Adds default variables to the plugin loader.
        
        Parameters
        ----------
        **variables : Keyword Parameters
            Variables to assigned to a plugin's module before it is loaded.
        
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
        Removes the mentioned default variables of the plugin loader.
        
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
        Removes all the default variables of the plugin loader.
        """
        self._default_variables.clear()
    
    
    def register(self, name, *positional_parameters, **keyword_parameters):
        """
        Registers a plugin.
        
        If the plugin already exists, returns that one.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The plugin's name to load.
        *positional_parameters : Positional parameters
            Additional parameters to create the plugin with.
        **keyword_parameters : Keyword parameters
            Additional parameters to create the plugin with.
        
        Other Parameters
        ----------------
        entry_point : `None`, `str`, `callable`, Optional
            Plugin specific entry point, to use over the plugin loader's default.
        exit_point : `None`, `str`, `callable`, Optional
            Plugin specific exit point, to use over the plugin loader's default.
        locked : `bool`, Optional
            Whether the given plugin(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`, Optional
            Whether snapshot feature should be used.
        **variables : Keyword parameters
            Variables to assign to a plugin(s)'s module before they are loaded.
        
        Raises
        ------
        ModuleNotFoundError
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
        plugin_names_and_paths = PluginExtractor.from_strings(
            'name', name
        ).get_plugin_names_and_paths(
            register_directories_as_roots = True
        )
        
        entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables = \
            validate_plugin_parameters(*positional_parameters, **keyword_parameters)
        
        for plugin_name, plugin_path in plugin_names_and_paths:
            self._register(
                plugin_name, plugin_path, entry_point, exit_point, extend_default_variables, locked,
                take_snapshot_difference, default_variables
            )
    
    
    def _register(
        self,
        plugin_name,
        plugin_path,
        entry_point,
        exit_point,
        extend_default_variables,
        locked,
        take_snapshot_difference,
        default_variables,
    ):
        """
        Adds a plugin to the plugin loader.
        
        If the plugin already exists, returns that one.
        
        Parameters
        ----------
        plugin_name : `None`, `str`
            The plugin's name to add.
        plugin_path : `None`, `str`
            Path of the plugin to add.
        entry_point : `None`, `str`, `callable`
            Plugin specific entry point, to use over the plugin loader's default.
        exit_point : `None`, `str`, `callable`
            Plugin specific exit point, to use over the plugin loader's default.
        extend_default_variables : `bool`
            Whether the plugin should use the loader's default variables or just it's own.
        locked : `bool`
            Whether the given plugin(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`
            Whether snapshot feature should be used.
        default_variables : `None`, `HybridValueDictionary` of (`str`, `object`) items
            An optionally weak value dictionary to store objects for assigning them to modules before loading them.
            If would be empty, is set as `None` instead.
        
        Returns
        -------
        plugin : ``Plugin``
            The registered plugin.
        """
        plugin = Plugin(
            plugin_name, plugin_path, entry_point, exit_point, extend_default_variables,
            locked, take_snapshot_difference, default_variables
        )
        
        self._plugins_by_name[plugin.name] = plugin
        self._plugins_by_name[plugin.file_name] = plugin
        
        short_name = plugin.short_name
        if (short_name is not None):
            self._plugins_by_name.setdefault(plugin.short_name, plugin)
        
        return plugin
    
    
    def remove(self, name):
        """
        Removes one or more plugins from the plugin loader.
        
        If any of the plugins is not found, no errors will be raised.
        
        Parameters
        ----------
        name : `None`, `str`, ``Plugin``, ``PluginTree`` `iterable` of (`None`, `str`, ``Plugin``, ``PluginTree``)
            The plugin(s)'s name(s) to remove.
        
        Raises
        ------
        TypeError
            If `name` was not given as `str`, `iterable` of `str`.
        RuntimeError
            If a loaded plugin would be removed.
        """
        plugins = PluginExtractor('name', name).get_plugins(raise_if_cannot_resolve = False)
        
        for plugin in plugins:
            if plugin._state == PLUGIN_STATE_LOADED:
                raise RuntimeError(
                    f'Plugin `{plugin.name!r}` can not be removed meanwhile it is loaded.'
                )
        
        for plugin in plugins:
            plugin._unlink()
    
    
    def register_and_load(self, name, *parameters, blocking = True, **keyword_parameters):
        """
        Registers then loads the plugin.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The plugin's name to load.
        
        *parameters : Parameters
            Additional parameters to create the plugin with.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to create the plugin with.
        
        Other Parameters
        ----------------
        entry_point : `None`, `str`, `callable`, Optional
            Plugin specific entry point, to use over the plugin loader's default.
        exit_point : `None`, `str`, `callable`, Optional
            Plugin specific exit point, to use over the plugin loader's default.
        locked : `bool`, Optional
            Whether the given plugin(s) should not be affected by `.{}_all` methods.
        take_snapshot_difference : `bool`, Optional
            Whether snapshot feature should be used.
        **variables : Keyword parameters
            Variables to assign to a plugin(s)'s module before they are loaded.
        
        Returns
        -------
        task : `set` of ``Plugin``, ``Task`` -> ``Plugin``, ``FutureWrapperAsync`` -> ``Plugin``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
            
            When finished returns the loaded plugin.
        
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
        PluginError
            The plugin failed to load correctly.
        """
        return _run_maybe_blocking(self._load_plugin_task(name, parameters, keyword_parameters), blocking)
    
    
    async def _load_plugin_task(self, name, parameters, keyword_parameters):
        """
        Adds, then loads the plugin.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`
            The plugin's name.
        parameters : `tuple` of `object`
            Additional parameters to create the plugin with.
        keyword_parameters : `dict` of (`str`, `object`) items
            Additional parameters to create the plugin with.
        
        Returns
        -------
        plugin : ``Plugin``
            The loaded plugin.
        
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
        PluginError
            The plugin failed to load correctly.
        """
        plugin_name_and_path_pair = _get_plugin_name_and_path(name, False)
        if plugin_name_and_path_pair is None:
            raise ModuleNotFoundError(
                f'No plugin(s) found with the given name: {name!r}.'
            ) from None
        
        plugin_name, plugin_path = plugin_name_and_path_pair
        
        plugin = _try_get_plugin(plugin_name, plugin_path)
        
        entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables = \
            validate_plugin_parameters(*parameters, **keyword_parameters)
    
        if (plugin is None):
            plugin = self._register(
                plugin_name, plugin_path, entry_point, exit_point, extend_default_variables, locked,
                take_snapshot_difference, default_variables
            )
            
        else:
            if (default_variables is not None):
                plugin.add_default_variables(**default_variables)
            
            if plugin.is_loaded():
                return plugin
        
        plugin_error = await self._plugin_loader(plugin)
        if (plugin_error is not None):
            raise plugin_error
        
        return plugin
    
    
    def load(self, name, *, blocking = True, deep = True):
        """
        Loads the plugin with the given name. If the plugin is already loaded, will do nothing.
        
        Parameters
        ----------
        name : `None`, `str`, ``Plugin``, ``PluginTree`` `iterable` of (`None`, `str`, ``Plugin``, ``PluginTree``)
            The plugin's name.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        deep : `bool` = `True`, Optional (Keyword only)
            Whether the plugin with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        task : `list` of ``Plugin``, ``Task`` -> `list` of ``Plugin``,
                ``FutureWrapperAsync`` -> `list` of ``Plugin``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
            
            When finished returns the loaded plugin.
        
        Raises
        ------
        PluginError
            - No plugin is added with the given name.
            - Loading the plugin failed.
        """
        return _run_maybe_blocking(self._load_task(name, deep), blocking)
    
    
    async def _load_task(self, name, deep):
        """
        Loads the given plugins.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str'
            The plugin(s) name to load.
        deep : `bool`
            Whether the plugin with all of it's parent and with their child should be reloaded.

        Returns
        -------
        plugins : `list` of ``Plugin``
            The loaded plugins.
        
        Raises
        ------
        PluginError
            - No plugin is added with the given name.
            - Loading the plugin failed.
        """
        plugins = PluginExtractor('name', name).get_plugins()
        plugins, plugin_trees = self._pull_previously_failed_plugin_trees(plugins)
        plugin_trees = _build_and_sort_plugin_trees(plugins, plugin_trees, deep)
        await self._execute_actions_on_plugin_trees(
            plugin_trees,
            PLUGIN_ACTION_FLAG_LOAD | PLUGIN_ACTION_FLAG_SYNTAX_CHECK | PLUGIN_ACTION_FLAG_UNLINK,
        )
        return _unwrap_plugin_trees_into_plugins(plugin_trees)
    
    
    def unload(self, name, *, blocking = True, deep = True):
        """
        Unloads the plugin with the given name.
        
        Parameters
        ----------
        name : `None`, `str`, ``Plugin``, ``PluginTree`` `iterable` of (`None`, `str`, ``Plugin``, ``PluginTree``)
            The plugin's name.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        deep : `bool` = `True`, Optional (Keyword only)
            Whether the plugin with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        task : `list` of ``Plugin``, ``Task`` -> `list` of ``Plugin``,
                ``FutureWrapperAsync`` -> `list` of ``Plugin``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            unloading is done. However if called from a sync thread, will block till the unloading is done.
            
            When finished returns the unloaded plugin.
        
        Raises
        ------
        PluginError
            - No plugin is added with the given name.
            - Unloading the plugin failed.
        """
        return _run_maybe_blocking(self._unload_task(name, deep), blocking)
    
    
    async def _unload_task(self, name, deep):
        """
        Unloads the plugin with the given name.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The plugin's name.
        deep : `bool`
            Whether the plugin with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        plugins : `list` of ``Plugin``
            The unloaded plugins.
        
        Raises
        ------
        PluginError
            - No plugin is added with the given name.
            - Unloading the plugin failed.
        """
        plugins = PluginExtractor('name', name).get_plugins()
        plugins, plugin_trees = self._pull_previously_failed_plugin_trees(plugins)
        plugin_trees = _build_and_sort_plugin_trees(plugins, plugin_trees, deep)
        await self._execute_actions_on_plugin_trees(
            plugin_trees,
            PLUGIN_ACTION_FLAG_UNLOAD | PLUGIN_ACTION_FLAG_UNLINK,
        )
        return _unwrap_plugin_trees_into_plugins(plugin_trees)
    
    
    def reload(self, name, *, blocking = True, deep = True):
        """
        Reloads the plugin with the given name.
        
        Parameters
        ----------
        name : `None`, `str`, ``Plugin``, ``PluginTree`` `iterable` of (`None`, `str`, ``Plugin``, ``PluginTree``)
            The plugin's name.
        
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.

        deep : `bool` = `True`, Optional (Keyword only)
            Whether the plugin with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        task : `list` of ``Plugin``, ``Task`` -> `list` of ``Plugin``,
                ``FutureWrapperAsync`` -> `list` of ``Plugin``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            reloading is done. However if called from a sync thread, will block till the reloading is done.
            
            When finished returns the reloaded plugins.
        
        Raises
        ------
        PluginError
            - No plugin is added with the given name.
            - Reloading the plugin failed.
        """
        return _run_maybe_blocking(self._reload_task(name, deep), blocking)
    
    
    async def _reload_task(self, name, deep):
        """
        Reloads the plugin with the given name.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`, `iterable` of `str`
            The plugin's name.
        deep : `bool`
            Whether the plugin with all of it's parent and with their child should be reloaded.
        
        Returns
        -------
        plugins : `list` of ``Plugin``
            The reloaded plugins.
        
        Raises
        ------
        PluginError
            - No plugin is added with the given name.
            - Reloading the plugin failed.
        """
        plugins = PluginExtractor('name', name).get_plugins()
        plugins, plugin_trees = self._pull_previously_failed_plugin_trees(plugins)
        plugin_trees = _build_and_sort_plugin_trees(plugins, plugin_trees, deep)
        await self._execute_actions_on_plugin_trees(
            plugin_trees,
            (
                PLUGIN_ACTION_FLAG_LOAD | PLUGIN_ACTION_FLAG_UNLOAD | PLUGIN_ACTION_FLAG_SYNTAX_CHECK |
                PLUGIN_ACTION_FLAG_UNLINK
            ),
        )
        return _unwrap_plugin_trees_into_plugins(plugin_trees)
    
    
    def load_all(self, *, blocking = True):
        """
        Loads all the plugin of the plugin loader. If anything goes wrong, raises an ``PluginError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureWrapperAsync``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            loading is done. However if called from a sync thread, will block till the loading is done.
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Raises
        ------
        PluginError
            If any plugin failed to load correctly.
        """
        return _run_maybe_blocking(self._load_all_task(), blocking)
    
    
    async def _load_all_task(self):
        """
        Loads all the plugins of the plugin loader.
        
        Loads each plugin one after the other. The raised exceptions' messages are collected into one exception,
        what will be raised only at the end. If any of the plugins raises, will still try to unload the leftover
        ones.
        
        This method is a coroutine.
        
        Raises
        ------
        PluginError
            If any plugin failed to load correctly.
        """
        plugins = [plugin for plugin in PLUGINS.values() if not plugin._locked]
        plugins, plugin_trees = self._pull_previously_failed_plugin_trees(plugins)
        plugin_trees = _build_and_sort_plugin_trees(plugins, plugin_trees, False)
        
        await self._execute_actions_on_plugin_trees(
            plugin_trees,
            PLUGIN_ACTION_FLAG_LOAD | PLUGIN_ACTION_FLAG_SYNTAX_CHECK | PLUGIN_ACTION_FLAG_UNLINK,
        )
    
    
    def unload_all(self, *, blocking = True):
        """
        Unloads all the plugin of the plugin loader. If anything goes wrong, raises an ``PluginError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureWrapperAsync``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            unloading is done. However if called from a sync thread, will block till the unloading is done.
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Raises
        ------
        PluginError
            If any plugin failed to unload correctly.
        """
        return _run_maybe_blocking(self._unload_all_task(), blocking)
    
    
    async def _unload_all_task(self):
        """
        Unloads all the plugins of the plugin loader.
        
        Unloads each plugin one after the other. The raised exceptions' messages are collected into one exception,
        what will be raised only at the end. If any of the plugins raises, will still try to unload the leftover
        ones.
        
        This method is a coroutine.
        
        Raises
        ------
        PluginError
            If any plugin failed to unload correctly.
        """
        plugins = [plugin for plugin in PLUGINS.values() if not plugin._locked]
        plugins, plugin_trees = self._pull_previously_failed_plugin_trees(plugins)
        plugin_trees = _build_and_sort_plugin_trees(plugins, plugin_trees, False)
        
        await self._execute_actions_on_plugin_trees(
            plugin_trees,
            PLUGIN_ACTION_FLAG_UNLOAD | PLUGIN_ACTION_FLAG_UNLINK,
        )
    
    
    def reload_all(self, *, blocking = True):
        """
        Reloads all the plugin of the plugin loader. If anything goes wrong, raises an ``PluginError`` only
        at the end, with the exception(s).
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureWrapperAsync``
            If the method is called from an ``EventThread``, then returns an awaitable, what will yield when the
            reloading is done. However if called from a sync thread, will block till the reloading is done.
        blocking : `bool` = `True`, Optional (Keyword only)
            Whether the operation should be blocking when called from a non-async thread.
        
        Raises
        ------
        PluginError
            If any plugin failed to reload correctly.
        """
        return _run_maybe_blocking(self._reload_all_task(), blocking)
    
    
    async def _reload_all_task(self):
        """
        Reloads all the plugins of the plugin loader.
        
        If a plugin is not unloaded, will load it, if the plugin is loaded, will unload, then load it.
        Reloads each plugin one after the other. The raised exceptions' messages are collected into one exception,
        what will be raised at the end. If any of the plugins raises, will still try to reload the leftover ones.
        
        This method is a coroutine.
        
        Raises
        ------
        PluginError
            If any plugin failed to reload correctly.
        """
        plugins = [plugin for plugin in PLUGINS.values() if not plugin._locked]
        plugins, plugin_trees = self._pull_previously_failed_plugin_trees(plugins)
        plugin_trees = _build_and_sort_plugin_trees(plugins, plugin_trees, False)
        
        await self._execute_actions_on_plugin_trees(
            plugin_trees,
            (
                PLUGIN_ACTION_FLAG_LOAD | PLUGIN_ACTION_FLAG_UNLOAD | PLUGIN_ACTION_FLAG_SYNTAX_CHECK |
                PLUGIN_ACTION_FLAG_UNLINK
            ),
        )
    
    
    async def _execute_actions_on_plugin_trees(self, plugin_trees, actions):
        """
        Executes the actions on the given plugins.
        
        This method is a coroutine.
        
        Parameters
        ----------
        plugin_trees : `list` of ``PluginTree``
            The plugin trees to execute the actions on.
        actions : `int`
            Bitwise flags of the actions to executed.
        
        Raises
        ------
        PluginError
            If any plugin failed to load / reload correctly.
        """
        exceptions = None
        plugin_tree_iterators = None
        
        if (actions & PLUGIN_ACTION_FLAG_SYNTAX_CHECK) and plugin_trees:
            exceptions, plugin_tree_iterators = await self._execute_syntax_check_on_plugin_trees(
                plugin_trees, exceptions, plugin_tree_iterators
            )
            
            if (exceptions is not None) and (plugin_tree_iterators is not None):
                plugin_tree_iterator = plugin_tree_iterators[-1]
                plugin_trees = _sort_plugin_trees({*plugin_tree_iterator.iter_done_success()})
        
        if (actions & PLUGIN_ACTION_FLAG_UNLOAD) and plugin_trees:
            exceptions, plugin_tree_iterators = await self._execute_unload_on_plugin_trees(
                plugin_trees, exceptions, plugin_tree_iterators
            )
        
        if (actions & PLUGIN_ACTION_FLAG_UNLINK) and plugin_trees:
            plugin_trees, plugin_tree_iterators = self._execute_unlink_on_plugin_trees(
                plugin_trees, plugin_tree_iterators
            )
            
        if (actions & PLUGIN_ACTION_FLAG_LOAD) and plugin_trees:
            exceptions, plugin_tree_iterators = await self._execute_load_on_plugin_trees(
                plugin_trees, exceptions, plugin_tree_iterators
            )
        
        if (exceptions is not None):
            self._push_previously_failed_plugin_trees_from_iterators(plugin_tree_iterators)
            
            try:
                raise PluginError(
                    action = actions, cause = CauseGroup(*exceptions), plugin_tree_iterators = plugin_tree_iterators
                )
            finally:
                exceptions = None
    
    
    def _execute_unlink_on_plugin_trees(self, plugin_trees, plugin_tree_iterators):
        """
        Unlinks the deleted plugins from the plugin trees.
        
        Parameters
        ----------
        plugin_trees : `list` of ``PluginTree``
            The plugin trees to unload.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        
        Returns
        -------
        plugin_trees : `list` of ``PluginTree``
            The new plugin trees.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        """
        if plugin_tree_iterators is None:
            plugin_tree_iterators = []
        
        plugin_tree_iterator = PluginTreeIterator(plugin_trees, PLUGIN_ACTION_FLAG_UNLINK)
        plugin_tree_iterators.append(plugin_tree_iterator)
        
        to_unlink = None
        plugin_root_names = None
        
        for plugin in plugin_tree_iterator:
            if plugin._state == PLUGIN_STATE_LOADED or is_file(plugin.path):
                continue
            
            plugin_root_names = _add_plugin_name_to_plugin_root_names(plugin_root_names, plugin.name)
            
            if to_unlink is None:
                to_unlink = set()
            
            to_unlink.add(plugin)
            continue
        
        if (to_unlink is not None):
            # Collect additional plugins that are under in the tree than ours.
            for plugin in PLUGINS.values():
                if plugin in to_unlink:
                    continue
                    
                if not _is_plugin_name_in_plugin_root_names(plugin_root_names, plugin.name):
                    continue
                
                if plugin._state == PLUGIN_STATE_LOADED or is_file(plugin.path):
                    continue
                
                to_unlink.add(plugin)
                continue
            
            for plugin in to_unlink:
                plugin._unlink()
            
            plugin_trees = [
                plugin_tree for plugin_tree in
                (plugin_tree.copy_without(to_unlink) for plugin_tree in plugin_trees)
                if plugin_tree is not None
            ]
        
        return plugin_trees, plugin_tree_iterators
    
    
    async def _execute_load_on_plugin_trees(self, plugin_trees, exceptions, plugin_tree_iterators):
        """
        Executes load on the given plugins
        
        This method is a coroutine.
        
        Parameters
        ----------
        plugin_trees : `list` of ``PluginTree``
            The plugin trees to unload.
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        
        Returns
        -------
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        """
        if plugin_tree_iterators is None:
            plugin_tree_iterators = []
        
        plugin_tree_iterator = PluginTreeIterator(plugin_trees, PLUGIN_ACTION_FLAG_LOAD)
        plugin_tree_iterators.append(plugin_tree_iterator)
        
        for plugin in plugin_tree_iterator:
            exception = await self._plugin_loader(plugin)
            if (exception is not None):
                plugin_tree_iterator.fail_current_hard()
                plugin_tree_iterator.cancel_dependents_in_to_do(exception.get_plugins())
                if exceptions is None:
                    exceptions = []
                
                exceptions.append(exception)
        
        return exceptions, plugin_tree_iterators
    
    
    async def _execute_unload_on_plugin_trees(self, plugin_trees, exceptions, plugin_tree_iterators):
        """
        Executes unload on the given plugins
        
        This method is a coroutine.
        
        Parameters
        ----------
        plugin_trees : `list` of ``PluginTree``
            The plugin trees to unload.
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        
        Returns
        -------
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        """
        if plugin_tree_iterators is None:
            plugin_tree_iterators = []
        
        plugin_tree_iterator = PluginTreeIterator(plugin_trees, PLUGIN_ACTION_FLAG_UNLOAD)
        plugin_tree_iterators.append(plugin_tree_iterator)
        
        for plugin in plugin_tree_iterator:
            exception = await self._plugin_unloader(plugin)
            if (exception is not None):
                plugin_tree_iterator.fail_current_soft()
                
                if exceptions is None:
                    exceptions = []
                
                exceptions.append(exception)
        
        return exceptions, plugin_tree_iterators
    
    
    async def _plugin_loader(self, plugin):
        """
        Loads the given plugin. This method synchronises plugin loading.
        
        This method is a coroutine.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to unload.
        
        Returns
        -------
        exception : `None`, ``PluginError``
        """
        try:
            unloader_task = self._unloader_tasks[plugin]
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
            loader_task = self._loader_tasks[plugin]
        except KeyError:
            loader_task = Task(KOKORO, self._plugin_loader_task(plugin))
            loader_task.add_done_callback(partial_func(_pop_loader_task_callback, plugin))
            
            self._loader_tasks[plugin] = loader_task
        
        try:
            return await shield(loader_task, KOKORO)
        finally:
            loader_task = None
    
    
    async def _plugin_loader_task(self, plugin):
        """
        Loads the plugin. If the plugin is loaded, will do nothing.
        
        Loading an exception can be separated to 4 parts:
        
        - Assign the default variables.
        - Load the module.
        - Find the entry point (if needed).
        - Ensure the entry point (if found).
        
        If any of these fails, an ``PluginError`` will be raised. If step 1 raises, then a traceback will be
        included as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to load.
        
        Returns
        -------
        exception : `None`, ``PluginError``
        """
        self._execute_counter += 1
        try:
            try:
                # loading blocks, but unloading does not
                module = await KOKORO.run_in_executor(plugin._load)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                return PluginError(
                    f'Exception occurred meanwhile loading a plugin: `{plugin.name}`',
                    action = PLUGIN_ACTION_FLAG_LOAD,
                    cause = err,
                    plugin = plugin,
                )
            
            if module is None:
                return # already loaded
            
            entry_point = plugin._entry_point
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
                return PluginError(
                    (
                        f'Exception occurred meanwhile entering a plugin: `{plugin.name}`; '
                        f'At entry_point: {entry_point!r}.',
                    ),
                    cause = err,
                )
        
        
        finally:
            execute_counter = self._execute_counter - 1
            self._execute_counter = execute_counter
            if not execute_counter:
                self.call_done_callbacks()
    
    
    async def _plugin_unloader(self, plugin):
        """
        Unloads the given plugin. This method synchronises plugin unloading.
        
        This method is a coroutine.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to unload.
        
        Returns
        -------
        exception : `None`, ``PluginError``
        """
        try:
            loader_task = self._loader_tasks[plugin]
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
            unloader_task = self._unloader_tasks[plugin]
        except KeyError:
            unloader_task = Task(KOKORO, self._plugin_unloader_task(plugin))
            unloader_task.add_done_callback(partial_func(_pop_unloader_task_callback, plugin, ))
            
            self._unloader_tasks[plugin] = unloader_task
        
        try:
            return await shield(unloader_task, KOKORO)
        finally:
            unloader_task = None

    
    async def _plugin_unloader_task(self, plugin):
        """
        Unloads the plugin. If the plugin is not loaded, will do nothing.
        
        Loading an exception can be separated to 3 parts:
        
        - Find the exit point (if needed).
        - Ensure the exit point (if found).
        - Remove the default variables.
        
        If any of these fails, an ``PluginError`` will be raised. If step 2 raises, then a traceback will be
        included as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to unload.
        
        Returns
        -------
        exception : `None`, ``PluginError``
        """
        self._execute_counter += 1
        try:
            # loading blocks, but unloading does not
            module = plugin._unload()
            
            if module is None:
                return # not loaded
            
            try:
                exit_point = plugin._exit_point
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
                    return PluginError(
                        (
                            f'Exception occurred meanwhile unloading a plugin: `{plugin.name}`; '
                            f'At exit point: {exit_point!r},'
                        ),
                        action = PLUGIN_ACTION_FLAG_UNLOAD,
                        cause = err,
                        plugin = plugin,
                    )
            
            finally:
                plugin._unassign_variables()
                
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
        """Returns the plugin loader's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' plugin count: ',
            repr(len(PLUGINS)),
        ]
        
        entry_point = self._default_entry_point
        if (entry_point is not None):
            repr_parts.append(', default_entry_point = ')
            repr_parts.append(repr(entry_point))
        
        exit_point = self._default_exit_point
        if (exit_point is not None):
            repr_parts.append(', default_exit_point = ')
            repr_parts.append(repr(exit_point))
        
        default_variables = self._default_variables
        if default_variables:
            repr_parts.append(', default_variables = ')
            repr_parts.append(repr(default_variables))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def is_processing_plugin(self):
        """
        Returns whether the plugin loader is processing a plugin.
        
        Returns
        -------
        is_processing_plugin : `bool`
        """
        if self._execute_counter:
            is_processing_plugin = True
        else:
            is_processing_plugin = False
        
        return is_processing_plugin
    
    
    def get_plugin(self, name):
        """
        Returns the plugin with the given name. The plugin must be already registered.
        
        Parameters
        ----------
        name : `str`
            An plugin's name or path.
        
        Returns
        -------
        plugin : ``Plugin``, `None`.
            The matched plugin if any.
        """
        plugin_name_and_path_pair = _get_plugin_name_and_path(name, True)
        if (plugin_name_and_path_pair is not None):
            return _try_get_plugin(*plugin_name_and_path_pair)
    
    
    async def _execute_syntax_check_on_plugin_trees(self, plugin_trees, exceptions, plugin_tree_iterators):
        """
        Check syntax of the given plugin trees.
        
        This function is a coroutine.
        
        Parameters
        ----------
        plugin_trees : `list` of ``PluginTree``
            A list of plugin trees to check their syntax.
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        
        Returns
        -------
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        """
        return await KOKORO.run_in_executor(alchemy_incendiary(
            self._execute_syntax_check_on_plugin_trees_blocking, (plugin_trees, exceptions, plugin_tree_iterators)
        ))
    
    
    def _execute_syntax_check_on_plugin_trees_blocking(self, plugin_trees, exceptions, plugin_tree_iterators):
        """
        Checks whether the plugins can be reloaded.
        
        This method is blocking and ran inside of an executor by ``._execute_syntax_check_on_plugin_trees``.
        
        Parameters
        ----------
        plugin-trees : `list` of ``PluginTree``
            A list of plugin trees to check their syntax.
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        
        Returns
        -------
        exceptions : `None`, `list` of ``BaseException``
            Occurred exceptions.
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`
            Plugin tree iterators.
        """
        if plugin_tree_iterators is None:
            plugin_tree_iterators = []
        
        plugin_tree_iterator = PluginTreeIterator(plugin_trees, PLUGIN_ACTION_FLAG_SYNTAX_CHECK)
        plugin_tree_iterators.append(plugin_tree_iterator)
            
        for plugin in plugin_tree_iterator:
            exception = plugin._check_for_syntax()
            if (exception is not None):
                plugin_tree_iterator.fail_current_hard()
                plugin_tree_iterator.cancel_dependents_in_to_do(exception.get_plugins())
                if exceptions is None:
                    exceptions = []
                
                exceptions.append(exception)
        
        return exceptions, plugin_tree_iterators
    
    
    def add_done_callback(self, callback):
        """
        Adds a done callback to be called when the loading / unloading plugins is finished.
        
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
        Adds a done callback to be called when the loading / unloading plugins is finished.
        
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
        Calls done callbacks of the plugin loader.
        """
        done_callbacks = self._done_callbacks
        if (done_callbacks is not None):
            self._done_callbacks = done_callbacks
            
            for done_callback in done_callbacks:
                KOKORO.call_soon(done_callback)
    
    
    def _pull_previously_failed_plugin_trees(self, plugins):
        """
        Pulls previously failed plugin trees.
        
        Parameters
        ----------
        plugins : `list` of ``Plugins``
            Plugins to get failed trees for.
        
        Returns
        -------
        plugins : `list` of ``Plugin``
            Plugins excluding the matched ones.
        plugin_trees : `list` of ``PluginTree``
            The matched plugin trees.
        """
        plugin_trees = []
        
        previously_failed_load_trees = self._previously_failed_load_trees
        if previously_failed_load_trees is None:
            return plugins, plugin_trees
        
        found_plugins = set()
        
        for plugin_tree in previously_failed_load_trees:
            intersection = plugin_tree.get_intersection_with_plugins(plugins)
            if not intersection:
                continue
            
            found_plugins.update(intersection)
            plugin_trees.append(plugin_tree)
            continue
        
        if plugin_trees:
            for plugin_tree in plugin_trees:
                previously_failed_load_trees.discard(plugin_tree)
            
            if not previously_failed_load_trees:
                self._previously_failed_load_trees = None
            
            plugins = [plugin for plugin in plugins if plugin not in found_plugins]
        
        return plugins, plugin_trees
    
    
    def _push_previously_failed_plugin_trees_from_iterators(self, plugin_tree_iterators):
        """
        Pushes previous failed plugin trees from plugin tree iterators.
        
        Parameters
        ----------
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator``
            Plugin tree iterators to pull the failed plugin trees from.
        """
        if plugin_tree_iterators is None:
            return
        
        previously_failed_load_trees = self._previously_failed_load_trees
        for plugin_tree_iterator in plugin_tree_iterators:
            if not (plugin_tree_iterator.action & (PLUGIN_ACTION_FLAG_SYNTAX_CHECK | PLUGIN_ACTION_FLAG_LOAD)):
                continue
            
            for plugin_tree in chain(plugin_tree_iterator.iter_done_fail(), plugin_tree_iterator.iter_done_cancelled()):
                if previously_failed_load_trees is None:
                    previously_failed_load_trees = set()
                    self._previously_failed_load_trees = previously_failed_load_trees
                
                previously_failed_load_trees.add(plugin_tree)


PLUGIN_LOADER = PluginLoader()
export(PLUGIN_LOADER, 'PLUGIN_LOADER')
