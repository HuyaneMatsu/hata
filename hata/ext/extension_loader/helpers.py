__all__ = ()

from os import listdir as list_directory
from os.path import (
    basename as base_name, exists, isabs as is_absolute_path_name, isdir as is_directory, isfile as is_file,
    join as join_paths
)
from sys import path as route_paths

from scarletio import CallableAnalyzer, HybridValueDictionary

from .constants import ABSOLUTE_PATH_EXTENSION_NAME_PREFIX
from .extension_root import register_extension_root


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


def validate_extension_parameters(entry_point=None, exit_point=None, extend_default_variables=True, locked=False,
        take_snapshot_difference=True, **variables):
    """
    Validates extension parameters.
    
    Parameters
    ----------
    entry_point : `None`, `str`, `callable`, = `None` Optional
        Extension specific entry point, to use over the extension loader's default.
    exit_point : `None`, `str`, `callable` = `None`, Optional
        Extension specific exit point, to use over the extension loader's default.
    extend_default_variables : `bool` = `True`, Optional
        Whether the extension should use the loader's default variables or just it's own.
    locked : `bool` = `False`, Optional
        Whether the given extension(s) should not be affected by `.{}_all` methods.
    take_snapshot_difference : `bool` = `True`, Optional
        Whether snapshot feature should be used.
    **variables : Keyword parameters
        Variables to assign to an extension(s)'s module before they are loaded.
    
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
    """
    if not _validate_entry_or_exit(entry_point):
        raise TypeError(
            f'`validate_extension_parameters` expected `None`, `str` or a `callable` as `entry_point`, got '
            f'{entry_point.__class__.__name__}; {entry_point!r}.'
        )
    
    if not _validate_entry_or_exit(exit_point):
        raise TypeError(
            f'`validate_extension_parameters` expected `None`, `str` or a `callable` as `exit_point`, got '
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



PYTHON_EXTENSION_NAMES = frozenset(('.py', '.pyd', '.pyc', '.so'))


def _get_extension_name_and_path(name):
    """
    fetches the name and the path of the first matched extension. If non is matched raised `ImportError`.
    
    Parameters
    ----------
    name : `str`
        The name to fetch.
    
    Raises
    ------
    extension_name : `None`, `str`
        Extension's  name.
    extension_path : `str`
        Path of the extension file.
    
    Raises
    ------
    ImportError
        - Could not resolve the given `name`.
    ImportError
        - If `name` could not be detected as an extension.
    TypeError
        - If `name` is not `str` nor an `iterable` of `str`.
    """
    if not isinstance(name, str):
        raise TypeError(
            f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
        )
    
    generator = _iter_extension_names_and_paths(name)
    try:
        extension_pair = generator.send(None)
    except StopIteration:
        raise ImportError(
            f'No extensions found with the given name: {name!r}.'
        ) from None
    
    else:
        generator.close()
    
    return extension_pair


def _iter_extension_names_and_paths(name, *, register_directories_as_roots=False):
    """
    Fetches the names and the paths of the given extension.
    
    This function is a generator.
    
    Parameters
    ----------
    name : `str`, `iterable` of `str`
        The name(s) to fetch.
    register_directories_as_roots : `bool` = `False`, Optional (Keyword only)
        Whether directory roots should be registered.
    
    Yields
    ------
    extension_name : `None`, `str`
        Extension's  name.
    extension_path : `str`
        Path of the extension file.
    
    Raises
    ------
    ImportError
        - Could not resolve the given `name`.
    ImportError
        - If `name` could not be detected as an extension.
    TypeError
        - If `name` is not `str` nor an `iterable` of `str`.
    """
    for name in _iter_name_maybe_iterable(name):
        if name.startswith(ABSOLUTE_PATH_EXTENSION_NAME_PREFIX):
            yield name
            return
        
        yield from _lookup_path(name, register_directories_as_roots)


def _iter_name_maybe_iterable(name):
    """
    Fetches the given name.
    
    This function is a generator.
    
    Parameters
    ----------
    name : `str`, `iterable` of `str`
        The name to fetch to single strings.
    
    Yields
    ------
    extension_name : `None`, `str`
        The extension's name.
    extension_path : `str`
        Path of the extension file.
    
    Raises
    ------
    ImportError
        - Could not resolve the given `name`.
    TypeError
        - If `name` is not `str` nor an `iterable` of `str`.
    """
    name_type = type(name)
    if name_type is str:
        yield name
    
    elif issubclass(name_type, str):
        yield str(name)
    
    elif hasattr(name_type, '__iter__'):
        for sub_name in name:
            sub_name_type = type(sub_name)
            if sub_name_type is str:
                yield sub_name
            
            elif issubclass(sub_name_type, str):
                yield str(sub_name)
            
            else:
                raise TypeError(
                    f'`name` contains a non `str` element, got {sub_name_type.__name__}; {sub_name!r}; name={name!r}.'
                )
    
    else:
        raise TypeError(
            f'`name` can be `str`, `iterable` of `str`, got {name_type.__name__}; {name!r}.'
        )


def _lookup_path(import_name_or_path, register_directories_as_roots):
    """
    Detects the root of the given name.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    import_name_or_path : `str`
        An extension's import name, or it's absolute path.
    register_directories_as_roots : `bool`
        Whether directory roots should be registered.
    
    Yields
    ------
    extension_name : `None`, `str`
        Import name to an extension file.
    extension_path : `str`
        Path of the file.
    
    Raise
    -----
    ImportError
        If `import_name_or_path` name could not be detected as en extension.
    """
    if is_absolute_path_name(import_name_or_path):
        if exists(import_name_or_path):
            if is_directory(import_name_or_path):
                yield from _iter_directory(None, import_name_or_path)
                return
            
            if is_file(import_name_or_path):
                yield None, import_name_or_path
                return
    else:
        path_end = join_paths(*import_name_or_path.split('.'))
        for base_path in route_paths:
            path = join_paths(base_path, path_end)
            if exists(path) and is_directory(path):
                if register_directories_as_roots:
                    register_extension_root(import_name_or_path)
                yield from _iter_directory(import_name_or_path, path)
                return
            
            for python_extension_name in PYTHON_EXTENSION_NAMES:
                file_path = path + python_extension_name
                if exists(file_path) and is_file(file_path):
                    yield import_name_or_path, file_path
                    return
    
    raise ImportError(
        f'The given `import_name_or_path` could not be detected as an extension nor an absolute path, '
        f'got {import_name_or_path!r}.'
    )


def _iter_directory(import_name, directory_path):
    """
    Iterates over a directory's import names.
    
    Parameters
    ----------
    import_name : `None`, `str`
        The name of the extension if we would import it.
    directory_path : `str`
        Path to the directory
    
    Yields
    ------
    extension_name : `None`, `str`
        Detected import names for each applicable file in the directory.
    extension_path : `str`
        Path of the file.
    """
    for python_extension_name in PYTHON_EXTENSION_NAMES:
        file_path = join_paths(directory_path, f'__init__{python_extension_name}')
        if exists(file_path) and is_file(file_path):
            yield import_name, file_path
            return
    
    for file_name in list_directory(directory_path):
        if file_name.startswith('.') or (file_name == '__pycache__'):
            continue
        
        path = join_paths(directory_path, file_name)
        
        if is_file(path):
            for python_extension_name in PYTHON_EXTENSION_NAMES:
                if file_name.endswith(python_extension_name):
                    if import_name is None:
                        import_name_value = None
                    else:
                        import_name_value = f'{import_name}.{file_name[:-len(python_extension_name)]}'
                    yield import_name_value, path
                    break
            
            continue
        
        if is_directory(path):
            if import_name is None:
                import_name_value = None
            else:
                import_name_value = f'{import_name}.{file_name}'
            yield from _iter_directory(import_name_value, path)
            continue
        
        # no more cases
        continue


def _get_path_extension_name(path):
    """
    Creates extension name from the given path.
    
    Parameter
    ---------
    path : `str`
        Path to a file.
    
    Returns
    -------
    extension_name : `str`
    """
    file_name = base_name(path)
    dot_index = file_name.rfind('.')
    if dot_index != -1:
        file_name = file_name[:dot_index]
    
    return ABSOLUTE_PATH_EXTENSION_NAME_PREFIX + file_name


def _build_extension_tree(extensions, deep):
    """
    Builds a tree of extensions.
    
    Parameters
    ----------
    extensions : `list` of ``Extension``
        A list of extension to build the tree form.
    deep : `bool`
        Whether the extension with all of it's parent and with their child should be returned.
    
    Returns
    -------
    extensions : `list` of ``Extension``
    """
    extensions_to_unwrap = [*extensions]
    unwrapped_extensions = set()
    
    while extensions_to_unwrap:
        extension = extensions_to_unwrap.pop()
        
        if deep:
            for child_extension in extension.iter_child_extensions():
                if child_extension not in unwrapped_extensions:
                    extensions_to_unwrap.append(child_extension)
            
            for parent_extension in extension.iter_parent_extensions():
                if parent_extension not in unwrapped_extensions:
                    extensions_to_unwrap.append(parent_extension)
        
        unwrapped_extensions.add(extension)
    
    
    extensions_to_check_ordered = sorted(unwrapped_extensions, reverse=True)
    
    extensions_satisfied = set()
    extensions_satisfied_ordered = []
    
    while extensions_to_check_ordered:
        for index in reversed(range(len(extensions_to_check_ordered))):
            extension = extensions_to_check_ordered[index]
            
            if not extension.are_child_extensions_present_in(extensions_satisfied):
                continue
            
            extensions_satisfied.add(extension)
            extensions_satisfied_ordered.append(extension)
            del extensions_to_check_ordered[index]
            break

        else:
            raise RuntimeError(
                f'Extensions with circular satisfaction: {extensions_to_check_ordered!r}'
            )
    
    return extensions_satisfied_ordered
