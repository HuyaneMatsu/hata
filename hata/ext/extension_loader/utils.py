__all__ = ()

from sys import path as route_paths
from os.path import join as join_path, isdir as is_directory, isfile as is_file
from os import listdir as list_directory

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
    TypeError
        If `name` is not `str` nor an `iterable` of `str` instances.
    """
    for name in _iter_name_maybe_iterable(name):
        yield from _iter_name_maybe_directory(name)


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


def _iter_name_maybe_directory(name):
    """
    Iterates over the extension's names if it is a directory.
    
    This method is a generator.
    
    Parameters
    ----------
    name : `str`
        An extension's name.
    
    Yields
    ------
    name : `str`
        Extension names.
    """
    path_end = join_path(*name.split('.'))
    for base_path in route_paths:
        path = join_path(base_path, path_end)
        if is_directory(path) and (not is_file(join_path(path, '__init__.py'))):
            for file_name in list_directory(path):
                file_path = join_path(path, file_name)
                if is_directory(file_path):
                    if is_file(join_path(path, '__init__.py')):
                        yield f'{name}.{file_name}'
                    continue
                
                if is_file(file_path):
                    if file_name.endswith('.py'):
                        yield f'{name}.{file_name[:-3]}'
                    continue
            return
    
    yield name
