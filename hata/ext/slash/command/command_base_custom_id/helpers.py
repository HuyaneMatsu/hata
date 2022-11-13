__all__ = ()

from .....discord.component.shared_constants import CUSTOM_ID_LENGTH_MAX

from ...converters import (
    RegexMatcher, check_component_converters_satisfy_regex, check_component_converters_satisfy_string
)

try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern


def _validate_custom_id(custom_id):
    """
    Validates a `custom_id` value.
    
    Parameters
    ----------
    custom_id : `str`, `re.Pattern`
        The `custom_id` to validate.
    
    Returns
    -------
    custom_id : `str`, `re.Pattern`
        The validated custom_id.
    
    Raises
    ------
    ValueError
        If `custom_id`'s length is out of the expected range.
    """
    if isinstance(custom_id, str):
        if type(custom_id) is not str:
            custom_id = str(custom_id)
        
        custom_id_length = len(custom_id)
        if (custom_id_length < 1) or (custom_id_length > CUSTOM_ID_LENGTH_MAX):
            raise ValueError(
                f'`custom_id` length can be in range [1:{CUSTOM_ID_LENGTH_MAX}], got '
                f'{custom_id_length}; {custom_id!r}.'
            )
    
    return custom_id


def _validate_custom_ids(custom_id):
    """
    Validates one or more `custom_id` values.
    
    Parameters
    ----------
    custom_id : `str`, (`list`, `set`) of `str`.
        The `custom_id` to validate.
    
    Returns
    -------
    custom_id : `set` of (`str`, `re.Pattern`)
        The non-duped custom-ids.
    
    Raises
    ------
    TypeError
        If `custom_id`'s type is incorrect.
    ValueError
        If a `custom_id`'s length is out of the expected range.
    """
    custom_ids = set()
    if isinstance(custom_id, (str, Pattern)):
        custom_id = _validate_custom_id(custom_id)
        custom_ids.add(custom_id)
    
    elif isinstance(custom_id, (list, set)):
        
        if not custom_id:
            raise ValueError(
                f'`custom_id` received as empty {custom_id.__class__.__name__}.'
            )
        
        for sub_custom_id in custom_id:
            if isinstance(sub_custom_id, (str, Pattern)):
                sub_custom_id = _validate_custom_id(sub_custom_id)
                custom_ids.add(sub_custom_id)
                continue
            
            raise TypeError(
                f'`custom_id` contains a non `str` element, got: '
                f'{sub_custom_id.__class__.__name__}; {sub_custom_id!r}; custom_id = {custom_id!r}.'
            )
    
    else:
        raise TypeError(
            f'`custom_id` can be `str`, (`list`, `set`) of `str`, got '
            f'{custom_id.__class__.__name__}; {custom_id!r}.'
        )
    
    return custom_ids


def _validate_name(name):
    """
    Validates the given name.
    
    Parameters
    ----------
    name : `None`, `str`
        A command's respective name.
    
    Returns
    -------
    name : `None`, `str`
        The validated name.
    
    Raises
    ------
    TypeError
        If `name` is not given as `None` neither as `str`.
    """
    if name is not None:
        name_type = name.__class__
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(
                f'`name` can be `None`, `str`, got {name_type.__name__}; {name!r}.'
            )
    
    return name


def split_and_check_satisfaction(custom_ids, parameter_converters):
    """
    Splits custom id-s to `str` and to `re.Pattern`-s and validates them.
    
    Parameters
    ----------
    custom_ids : `set` of (`str`, `re.Pattern`)
        The custom-ids to split and validate.
    parameter_converters : `tuple` of ``ParameterConverter``
        The parameter converters generated from a component command.
    
    Returns
    -------
    string_custom_ids : `None`, `tuple` of `str`
        String custom ids.
    regex_custom_ids : `None`, `tuple` of ``RegexMatcher``
        Regex custom ids.
    
    Raises
    ------
    ValueError
        A string or regex pattern is not satisfied.
    """
    # Build
    string_custom_ids = None
    regex_custom_ids = None
    for custom_id in custom_ids:
        if isinstance(custom_id, str):
            if string_custom_ids is None:
                string_custom_ids = []
            
            string_custom_ids.append(custom_id)
        else:
            if regex_custom_ids is None:
                regex_custom_ids = []
            
            regex_custom_ids.append(custom_id)
    
    # Convert
    if (string_custom_ids is not None):
        string_custom_ids = tuple(string_custom_ids)
    
    if (regex_custom_ids is not None):
        regex_custom_ids = tuple(RegexMatcher(regex_custom_id) for regex_custom_id in regex_custom_ids)
    
    # Check
    if (string_custom_ids is not None):
        check_component_converters_satisfy_string(parameter_converters)
    
    if (regex_custom_ids is not None):
        for regex_custom_id in regex_custom_ids:
            check_component_converters_satisfy_regex(parameter_converters, regex_custom_id)
    
    # Good
    return string_custom_ids, regex_custom_ids
