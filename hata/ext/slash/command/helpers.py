__all__ = ()

def _checkout_auto_complete_parameter_name(parameter_name):
    """
    Checks out one parameter name to auto complete.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name to auto complete.
    
    Returns
    -------
    parameter_name : `str`
        The validated parameter name to autocomplete.
    
    Raises
    ------
    TypeError
        If `parameter_name` is not `str`.
    ValueError
        If `parameter_name` is an empty string.
    """
    if type(parameter_name) is str:
        pass
    elif isinstance(parameter_name, str):
        parameter_name = str(parameter_name)
    else:
        raise TypeError(
            f'`parameter_name` can be `str`, got '
            f'{parameter_name.__class__.__name__}; {parameter_name!r}.'
        )
    
    if not parameter_name:
        raise ValueError(
            f'`parameter_name` cannot be empty string.'
        )
    
    return parameter_name


def _build_auto_complete_parameter_names(parameter_name, parameter_names):
    """
    Builds a checks out parameter names.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name to auto complete.
    parameter_names : `tuple` of `str`
        Additional parameter to autocomplete.
    
    Returns
    -------
    processed_parameter_names : `list` of `str`
        The processed parameter names.
    
    Raises
    ------
    TypeError
        If `parameter_name` is not `str`.
    ValueError
        If `parameter_name` is an empty string.
    """
    processed_parameter_names = []
    
    parameter_name = _checkout_auto_complete_parameter_name(parameter_name)
    processed_parameter_names.append(parameter_name)
    
    if parameter_names:
        for iter_parameter_name in parameter_names:
            iter_parameter_name = _checkout_auto_complete_parameter_name(iter_parameter_name)
            processed_parameter_names.append(iter_parameter_name)
    
    return processed_parameter_names


def _register_auto_complete_function(parent, parameter_names, function):
    """
    Returned by `.autocomplete` decorators wrapped inside of `functools.partial` if `function` is not given.
    
    Parameters
    ----------
    parent : ``Slasher``, ``SlasherApplicationCommand``, ``SlasherApplicationCommandFunction``,
            ``SlasherApplicationCommandCategory``
        The parent entity to register the auto completer to.
    parameter_names : `list` of `str`
        The parameters' names.
    function : `async-callable`
        The function to register as auto completer.
    
    Returns
    -------
    auto_completer : ``SlasherApplicationCommandParameterAutoCompleter``
        The registered auto completer
    
    Raises
    ------
    RuntimeError
        - `function` cannot be `None`.
        - If the application command function has no parameter named, like `parameter_name`.
        - If the parameter cannot be auto completed.
    TypeError
        If `function` is not an asynchronous.
    """
    if (function is None):
        raise RuntimeError(
            f'`function` cannot be `None`.'
        )
    
    return parent._add_autocomplete_function(parameter_names, function)
