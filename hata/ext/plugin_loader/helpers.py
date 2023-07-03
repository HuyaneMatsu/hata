__all__ = ()

import sys
from os import listdir as list_directory, sep as PATH_SEPARATOR
from os.path import (
    basename as base_name, dirname as get_parent_directory_path, exists, isabs as is_absolute_path,
    isdir as is_directory, isfile as is_file, join as join_paths
)

from scarletio import CallableAnalyzer, HybridValueDictionary, include

from .constants import ABSOLUTE_PATH_PLUGIN_NAME_PREFIX, PLUGIN_ROOTS
from .plugin_root import is_tuple_starting_with, register_plugin_root


PLUGIN_LOADER = include('PLUGIN_LOADER')


def _validate_entry_or_exit(point):
    """
    Validates the given entry or exit point, returning `True`, if they passed.
    
    Parameters
    ----------
    point : `None`, `str`, `callable`
        The point to validate.
    
    Raises
    ------
    TypeError
        If `point` was given as `callable`, but accepts less or more positional parameters, as would be given.
    """
    if point is None:
        return True
    
    if isinstance(point, str):
        return True
    
    if callable(point):
        analyzer = CallableAnalyzer(point)
        min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
        if min_ > 1:
            raise TypeError(
                f'`{point!r}` excepts at least `{min_!r}` non reserved parameters, meanwhile the event '
                f'expects to pass `1`, got {point!r}'
            )
        
        if min_ == 1:
            return True
        
        #min<expected
        if max_ >= 1:
            return True
        
        if analyzer.accepts_args():
            return True
        
        raise TypeError(
            f'`{point!r}` expects maximum `{max_!r}` non reserved parameters  meanwhile the event expects '
            f'to pass `1`., got {point!r}'
        )
    
    return False


def validate_plugin_parameters(
    entry_point = None,
    exit_point = None,
    extend_default_variables = True,
    locked = False,
    take_snapshot_difference = True,
    **variables,
):
    """
    Validates plugin parameters.
    
    Parameters
    ----------
    entry_point : `None`, `str`, `callable`, = `None` Optional
        Plugin specific entry point, to use over the plugin loader's default.
    exit_point : `None`, `str`, `callable` = `None`, Optional
        Plugin specific exit point, to use over the plugin loader's default.
    extend_default_variables : `bool` = `True`, Optional
        Whether the plugin should use the loader's default variables or just it's own.
    locked : `bool` = `False`, Optional
        Whether the given plugin(s) should not be affected by `.{}_all` methods.
    take_snapshot_difference : `bool` = `True`, Optional
        Whether snapshot feature should be used.
    **variables : Keyword parameters
        Variables to assign to an plugin(s)'s module before they are loaded.
    
    Raises
    ------
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
    
    Returns
    -------
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
    default_variables : `None`, `HybridValueDictionary` of (`str`, `Any`) items
        An optionally weak value dictionary to store objects for assigning them to modules before loading them.
        If would be empty, is set as `None` instead.
    """
    if not _validate_entry_or_exit(entry_point):
        raise TypeError(
            f'`validate_plugin_parameters` expected `None`, `str` or a `callable` as `entry_point`, got '
            f'{entry_point.__class__.__name__}; {entry_point!r}.'
        )
    
    if not _validate_entry_or_exit(exit_point):
        raise TypeError(
            f'`validate_plugin_parameters` expected `None`, `str` or a `callable` as `exit_point`, got '
            f'{exit_point.__class__.__name__}; {exit_point!r}.'
        )
    
    if variables:
        default_variables = HybridValueDictionary(variables)
        for key, value in variables.items():
            if key in PROTECTED_NAMES:
                raise ValueError(
                    f'The passed {key!r} is a protected variable name of module type.'
                )
            default_variables[key] = value
    else:
        default_variables = None
    
    extend_default_variables_type = extend_default_variables.__class__
    if extend_default_variables_type is bool:
        pass
    elif issubclass(extend_default_variables_type, int):
        extend_default_variables = bool(extend_default_variables)
    else:
        raise TypeError(
            f'`extend_default_variables` can be `bool`, got {extend_default_variables_type.__name__}; '
            f'{extend_default_variables!r}.'
        )
    
    locked_type = type(locked)
    if locked_type is bool:
        pass
    elif issubclass(locked_type, int):
        locked = bool(locked)
    else:
        raise TypeError(
            f'`locked` can be `bool`, got {locked_type.__name__}; {locked!r}.'
        )
    
    return entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables


PROTECTED_NAMES = frozenset((
    '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
    '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    '__weakref__', '_cached', '_set_fileattr', 'cached', 'has_location', 'loader', 'loader_state', 'name', 'origin',
    'parent', 'submodule_search_locations', '__path__', '__spec__'
))



PYTHON_FILE_POSTFIX_NAMES = frozenset(('.py', '.pyd', '.pyc', '.so'))


def _try_get_plugin(plugin_name, plugin_path):
    """
    Tries to get plugin for the given name or path.
    
    Parameters
    ----------
    plugin_name : `None`, `str`
        Plugin's  name.
    plugin_path : `str`
        Path of the plugin file.
    
    Returns
    -------
    plugin : `None`, ``Plugin``
        The found plugin if any.
    """
    try:
        return PLUGIN_LOADER._plugins_by_name[plugin_path]
    except KeyError:
        pass
    
    if plugin_name is None:
        plugin_name = _get_path_plugin_name(plugin_path)
    
    try:
        return PLUGIN_LOADER._plugins_by_name[plugin_name]
    except KeyError:
        pass


def _get_plugin_name_and_path(name, allow_non_existent):
    """
    fetches the name and the path of the first matched plugin. If non is matched raised `ImportError`.
    
    Parameters
    ----------
    name : `str`
        The name to fetch.
    allow_non_existent : `bool`
        Whether non-existent files are allowed.
    
    Raises
    ------
    plugin_name_and_path_pair : `None`, `tuple` (`None`, `str` `str`)
        Plugin's name and path pair.
    
    Raises
    -----
    TypeError
        - If `name` is not `str` nor an `iterable` of `str`.
    """
    if not isinstance(name, str):
        raise TypeError(
            f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
        )
    
    # Return first match
    for plugin_name_and_path_pair in _iter_lookup_plugin_names_and_paths(name, False, True):
        return plugin_name_and_path_pair


def _iter_lookup_plugin_names_and_paths(name, register_directories_as_roots, allow_non_existent):
    """
    Fetches the names and the paths of the given plugin.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        The name to fetch.
    register_directories_as_roots : `bool`
        Whether directory roots should be registered.
    allow_non_existent : `bool`
        Whether non-existent files are allowed.
    
    Yields
    ------
    plugin_name : `None`, `str`
        Plugin's  name.
    plugin_path : `str`
        Path of the plugin file.
    
    Raises
    ------
    ModuleNotFoundError
        - If `name` could not be detected as an plugin.
    """
    if name.startswith(ABSOLUTE_PATH_PLUGIN_NAME_PREFIX):
        yield None, name
        return
    
    yield from _iter_lookup_path(name, register_directories_as_roots, allow_non_existent)


def _iter_lookup_path(import_name_or_path, register_directories_as_roots, allow_non_existent):
    """
    Detects the root of the given name.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    import_name_or_path : `str`
        An plugin's import name, or it's absolute path.
    register_directories_as_roots : `bool`
        Whether directory roots should be registered.
    allow_non_existent : `bool`
        Whether non-existent files are allowed.
    
    Yields
    ------
    plugin_name : `None`, `str`
        Import name to an plugin file.
    plugin_path : `str`
        Path of the file.
    
    Raise
    -----
    ModuleNotFoundError
        If `import_name_or_path` name could not be detected as a plugin.
    """
    if is_absolute_path(import_name_or_path):
        if exists(import_name_or_path):
            if is_directory(import_name_or_path):
                yield from _iter_lookup_directory(None, import_name_or_path)
                return
            
            if is_file(import_name_or_path):
                yield None, import_name_or_path
                return
        
        if allow_non_existent:
            yield None, import_name_or_path
            return
    
    else:
        path_end = join_paths(*import_name_or_path.split('.'))
        for base_path in sys.path:
            path = join_paths(base_path, path_end)
            if exists(path) and is_directory(path):
                if register_directories_as_roots:
                    register_plugin_root(import_name_or_path)
                yield from _iter_lookup_directory(import_name_or_path, path)
                return
            
            for python_file_postfix_name in PYTHON_FILE_POSTFIX_NAMES:
                file_path = path + python_file_postfix_name
                if exists(file_path) and is_file(file_path):
                    yield import_name_or_path, file_path
                    return
    
    raise ModuleNotFoundError(
        f'The given `import_name_or_path` could not be detected as an plugin nor an absolute path, '
        f'got {import_name_or_path!r}.'
    )


def _iter_lookup_directory(import_name, directory_path):
    """
    Iterates over a directory's import names.
    
    this function is an iterable generator.
    
    Parameters
    ----------
    import_name : `None`, `str`
        The name of the plugin if we would import it.
    directory_path : `str`
        Path to the directory
    
    Yields
    ------
    plugin_name : `None`, `str`
        Detected import names for each applicable file in the directory.
    plugin_path : `str`
        Path of the file.
    """
    for python_file_postfix_name in PYTHON_FILE_POSTFIX_NAMES:
        file_path = join_paths(directory_path, f'__init__{python_file_postfix_name}')
        if exists(file_path) and is_file(file_path):
            yield import_name, file_path
            return
    
    for file_name in list_directory(directory_path):
        if file_name.startswith('.') or (file_name == '__pycache__') or ('tests' in file_name):
            continue
        
        path = join_paths(directory_path, file_name)
        
        if is_file(path):
            for python_file_postfix_name in PYTHON_FILE_POSTFIX_NAMES:
                if file_name.endswith(python_file_postfix_name):
                    if import_name is None:
                        import_name_value = None
                    else:
                        import_name_value = f'{import_name}.{file_name[:-len(python_file_postfix_name)]}'
                    yield import_name_value, path
                    break
            
            continue
        
        if is_directory(path):
            if import_name is None:
                import_name_value = None
            else:
                import_name_value = f'{import_name}.{file_name}'
            yield from _iter_lookup_directory(import_name_value, path)
            continue
        
        # no more cases
        continue


def _get_path_plugin_name(path):
    """
    Creates plugin name from the given path.
    
    Parameter
    ---------
    path : `str`
        Path to a file.
    
    Returns
    -------
    plugin_name : `str`
    """
    file_name = base_name(path)
    if file_name == '__init__.py':
        path = get_parent_directory_path(path)
    else:
        dot_index = file_name.rfind('.')
        if dot_index != -1:
            path = file_name[:dot_index - len(file_name)]
    
    for sys_path in sys.path:
        if path.startswith(sys_path + PATH_SEPARATOR):
            parts = (*path[len(sys_path) + 1:].split(PATH_SEPARATOR),)
            for plugin_root in PLUGIN_ROOTS:
                if is_tuple_starting_with(parts, plugin_root):
                    return '.'.join(parts)
    
    return ABSOLUTE_PATH_PLUGIN_NAME_PREFIX + file_name


def _add_plugin_name_to_plugin_root_names(plugin_root_names, plugin_name):
    """
    Adds the plugin name to the plugin base names.
    
    Parameters
    ----------
    plugin_root_names : `None`, `set` of `str`
        Plugin root names.
    plugin_name : `str`
        The plugin's name.
    
    Returns
    ----------
    plugin_root_names : `set` of `str`
    """
    if plugin_root_names is None:
        plugin_root_names = {plugin_name}
    
    else:
        cut_name = plugin_name
        while True:
            dot_index = cut_name.rfind('.')
            if dot_index == -1:
                plugin_root_names.add(plugin_name)
                break
            
            cut_name = cut_name[:dot_index]
            if cut_name in plugin_root_names:
                break
            
            continue
    
    return plugin_root_names


def _is_plugin_name_in_plugin_root_names(plugin_root_names, plugin_name):
    """
    Returns whether the plugin name is in the given plugin root names.
    
    Parameters
    ----------
    plugin_root_names : `None`, `set` of `str`
        Plugin root names.
    plugin_name : `str`
        The plugin's name.
    
    Returns
    -------
    is_in : `bool`
    """
    if plugin_root_names is None:
        return False
    
    plugin_name_length = len(plugin_name)
    
    for plugin_root_name in plugin_root_names:
        if not plugin_name.startswith(plugin_root_name):
            continue
        
        plugin_root_name_length = len(plugin_root_name)
        if plugin_name_length == plugin_root_name_length:
            return True
        
        if plugin_root_name_length > plugin_name_length and plugin_root_name[plugin_name_length] == '.':
            return True
    
    return False
