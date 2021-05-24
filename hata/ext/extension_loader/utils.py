__all__ = ()

from sys import path as route_paths
from os.path import join as join_path, isdir as is_folder, isfile as is_file, exists
from os import listdir as list_directory

from ...backend.utils import HybridValueDictionary
from ...backend.analyzer import CallableAnalyzer


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

def validate_extension_parameters(entry_point=None, exit_point=None, extend_default_variables=True, locked=False,
        take_snapshot_difference=True, **variables):
    """
    Validates extension parameters.
    
    Parameters
    ----------
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
    
    Returns
    -------
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
    if not _validate_entry_or_exit(entry_point):
        raise TypeError(f'`validate_extension_parameters` expected `None`, `str` or a `callable` as '
            f'`entry_point`, got {entry_point.__class__.__name__}.')
    
    if not _validate_entry_or_exit(exit_point):
        raise TypeError(f'`validate_extension_parameters` expected `None`, `str` or a `callable` as `exit_point`, '
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
    
    locked_type = type(locked)
    if locked_type is bool:
        pass
    elif issubclass(locked_type, int):
        locked = bool(locked)
    else:
        raise TypeError(f'`locked` should have been passed as `bool`, got: {locked_type.__name__}.')
    
    return entry_point, exit_point, extend_default_variables, locked, take_snapshot_difference, default_variables


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



PYTHON_EXTENSION_NAMES = (
    '.py',
    '.pyd',
    '.pyc',
    '.so',
)


def _iter_extension_names(name):
    """
    Fetches the names
    
    This function is a generator.
    
    Parameters
    ----------
    name : `str` or `iterable` of `str`
        The name to fetch to single strings.
    
    Yields
    ------
    name : `str`
        Extension names.
    
    Raises
    ------
    ImportError
        If a name could not be detected as an extension.
    TypeError
        If `name` is not `str` nor an `iterable` of `str` instances.
    """
    for name in _iter_name_maybe_iterable(name):
        yield from _lookup_path(name)


def _iter_name_maybe_iterable(name):
    """
    Fetches the given name.
    
    This function is a generator.
    
    Parameters
    ----------
    name : `str` or `iterable` of `str`
        The name to fetch to single strings.
    
    Yields
    ------
    name : `str`
        Extension names.
    
    Raises
    ------
    TypeError
        If `name` is not `str` nor an `iterable` of `str` instances.
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
                raise TypeError(f'`name` can be given as an `str` or as `iterable` of `str`, got an `iterable`, which '
                    f'contains an: {sub_name_type.__name__} element.')
    else:
        raise TypeError(f'`name` can be given as an `str` or as `iterable` of `str`, got an `iterable`, got '
            f'{name_type.__name__}.')


def _lookup_path(import_name):
    """
    Detects the root of the given name.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    import_name : `str`
        An extension's import name.
    
    Yields
    ------
    import_name : `str`
        Import name to an extension file.
    
    Raise
    -----
    ImportError
        If `name` name could not be detected as en extension.
    """
    path_end = join_path(*import_name.split('.'))
    for base_path in route_paths:
        path = join_path(base_path, path_end)
        if exists(path) and is_folder(path):
            yield from _iter_folder(import_name, path)
            return
        
        for python_extension_name in PYTHON_EXTENSION_NAMES:
            file_path = path+python_extension_name
            if exists(file_path) and is_file(file_path):
                yield import_name
                return
    
    raise TypeError(f'The given `import_name` could not be detected as an extension, got {import_name!r}.')


def _iter_folder(import_name, folder_path):
    """
    Iterates over a folder's import names.
    Parameters
    ----------
    import_name : `str`
        The name of the extension if we would import it.
    folder_path : `str`
        Path to the folder
    
    Yields
    ------
    import_name : `str`
        Detected import names for each applicable file in the folder.
    """
    for python_extension_name in PYTHON_EXTENSION_NAMES:
        file_path = join_path(folder_path, f'__init__{python_extension_name}')
        if exists(file_path) and is_file(file_path):
            yield import_name
            return
    
    for file_name in list_directory(folder_path):
        if file_name.startswith('.') or (file_name == '__pycache__'):
            continue
        
        path = join_path(folder_path, file_name)
        
        if is_file(path):
            for python_extension_name in PYTHON_EXTENSION_NAMES:
                if file_name.endswith(python_extension_name):
                    value = f'{import_name}.{file_name[:-len(python_extension_name)]}'
                    yield value
                    break
            
            continue
        
        if is_folder(path):
            yield from _iter_folder(f'{import_name}.{file_name}', path)
            continue
        
        # no more cases
        continue
