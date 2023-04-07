"""
Hata extensions come into this directory.

If a hata library extension is imported, it should register itself with the ``register_library_extension``, so if an
other library extension is imported, it can register a hook to run only if both are imported.

Hook registrations can be done with the ``add_library_extension_hook`` function.
"""
__all__ = ()

import warnings
from importlib.util import find_spec
from importlib import import_module


def __getattr__(attribute_name):
    """Gets the extension from name if not yet imported."""
    
    spec = find_spec(f'{__name__}.{attribute_name}')
    if (spec is not None):
        try:
            module = import_module(spec.name)
        except ImportError:
            raise
        
        except BaseException as err:
            raise ImportError from err
        
        else:
            return module
    
    raise AttributeError(attribute_name)


from scarletio.ext import (
    add_library_extension_hook, register_library_extension
)


EXTENSION_SETUP_FUNCTIONS = {}


class SetupFunction:
    """
    Describes a setup function.
    
    Attributes
    ----------
    extension_name : `str`
        The represented extension's full name.
    extension_short_name : `str`
        The represented extension's short name.
    optional_parameters : `None`, `tuple` of `str`
        Optional parameters of the `setup_function`.
    required_parameters : `None`, `tuple` of `str`
        Required parameters by the `setup_function`.
    setup_function : ``FunctionType``
        The setup function itself.
    """
    __slots__ = (
        'extension_name', 'extension_short_name', 'optional_parameters', 'required_parameters', 'setup_function'
    )
    
    def __new__(cls, extension_name, setup_function, required_parameters, optional_parameters):
        """
        Creates a new ``SetupFunction`` from the given parameters.
        
        Parameters
        ----------
        extension_name : `str`
            The represented extension's full name.
        setup_function : ``FunctionType``
            The setup function itself.
        required_parameters : `None`, `tuple` of `str`
            Required parameters by the `setup_function`.
        optional_parameters : `None`, `tuple` of `str`
            Optional parameters of the `setup_function`.
        """
        dot_index = extension_name.find('.')
        if dot_index != -1:
            extension_short_name = extension_name[dot_index + 1:]
        else:
            extension_short_name = extension_name
        
        self = object.__new__(cls)
        self.setup_function = setup_function
        self.required_parameters = required_parameters
        self.optional_parameters = optional_parameters
        self.extension_name = extension_name
        self.extension_short_name = extension_short_name
        return self
    
    
    def __call__(self, client, input_keyword_parameters):
        """
        Calls the internal ``setup_function``.
        
        Parameters
        ----------
        client : ``Client``
            The client on who the extension should be setupped.
        input_keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters to get the extension's parameters from.
        """
        positional_parameters = []
        required_parameters = self.required_parameters
        if (required_parameters is not None):
            for required_parameter in required_parameters:
                positional_parameters.append(input_keyword_parameters[required_parameter])
        
        keyword_parameters = {}
        optional_parameters = self.optional_parameters
        if (optional_parameters is not None):
            for optional_parameter in optional_parameters:
                try:
                    parameter_value = input_keyword_parameters[optional_parameter]
                except KeyError:
                    pass
                else:
                    keyword_parameters[optional_parameter] = parameter_value
        
        self.setup_function(client, *positional_parameters, **keyword_parameters)


def register_setup_function(extension_name, setup_function, required_parameters, optional_parameters):
    """
    Registers an extension setup function.
    
    Parameters
    ----------
    extension_name : `str`
        The extension's system name.
    setup_function : `FunctionType``
        The setup function of the extension.
    required_parameters : `None`, `tuple` of `str`
        Required parameters by the `setup_function`.
    optional_parameters : `None`, `tuple` of `str`
        Optional parameters of the `setup_function`.
    """
    setup_function = SetupFunction(extension_name, setup_function, required_parameters, optional_parameters)
    
    EXTENSION_SETUP_FUNCTIONS[extension_name] = setup_function
    EXTENSION_SETUP_FUNCTIONS.setdefault(setup_function.extension_short_name, setup_function)


def _try_get_setup_function(extension_name, extension_short_name):
    """
    Tries to get setup function for the given extension name.
    
    Parameters
    ----------
    extension_name : `str`
        The extension's name.
    
    Returns
    -------
    setup_function : `None`, ``SetupFunction``
        A function to setup the respective extension on a client.
    """
    try:
        setup_function = EXTENSION_SETUP_FUNCTIONS[extension_name]
    except KeyError:
        if (extension_short_name is None):
            setup_function = None
        else:
            setup_function = EXTENSION_SETUP_FUNCTIONS.get(extension_short_name)
    
    return setup_function


def _get_setup_function(extension_name):
    """
    Gets extension setup function for the given extension name.
    
    Parameters
    ----------
    extension_name : `str`
        The extension's name.
    
    Returns
    -------
    setup_function : ``SetupFunction``
        A function to setup the respective extension on a client.
    
    Raises
    ------
    ImportError
        if importing the extension failed.
    ModuleNotFoundError
        If the extension not found.
    RuntimeError
        If the extension has no setup function.
    """
    dot_index = extension_name.find('.')
    if dot_index == -1:
        short_name = None
    else:
        short_name = extension_name[dot_index + 1:]
    
    setup_function = _try_get_setup_function(extension_name, short_name)
    if (setup_function is not None):
        return setup_function
    
    # Use goto
    while True:
        spec = find_spec(f'{__name__}.{extension_name}')
        if (spec is not None):
            break
        
        if (short_name is not None):
            spec = find_spec(f'{__name__}.{short_name}')
            if (spec is not None):
                break
        
        raise ModuleNotFoundError(extension_name)
    
    try:
        import_module(spec.name)
    except ImportError:
        raise
    except BaseException as err:
        raise ImportError from err
    
    setup_function = _try_get_setup_function(extension_name, short_name)
    if (setup_function is None):
        raise RuntimeError(f'`Extension: {extension_name!r} has no setup function.')
    
    return setup_function


def get_setup_functions(extensions, keyword_parameters):
    """
    Gets and validates setup function parameters.
    
    Parameters
    ----------
    extensions : `None`, `set` of `str`
        The extension(s)'s name to setup on a client.
    keyword_parameters : `dict` of (`str`, `object`)
        Additional parameters to pass to extensions.
    
    Returns
    -------
    setup_functions : `None`, `set` of ``SetupFunction``
        Setup functions to setup on a client.
    
    Raises
    ------
    ImportError
        If importing an extension failed.
    ModuleNotFoundError
        If an extension not found.
    RuntimeError
        - If `keyword_parameters` not contains any required parameter.
        - The an extension has no setup function.
    
    Notes
    -----
    If `keyword_parameters` contains any extra parameters, `RuntimeWarning` is dropped.
    
    > The function may block if new extension is imported, so please consider avoiding production time calls.
    """
    setup_functions = None
    
    if (extensions is not None):
        for extension_name in extensions:
            setup_function = _get_setup_function(extension_name)
            
            if setup_functions is None:
                setup_functions = set()
            
            setup_functions.add(setup_function)
    
    exhaustible_parameters = set(keyword_parameters.keys())
    
    if (setup_functions is not None):
        for setup_function in setup_functions:
            required_parameters = setup_function.required_parameters
            if (required_parameters is not None):
                exhaustible_parameters.difference_update(required_parameters)
                
                for required_parameter in required_parameters:
                    if required_parameter not in keyword_parameters:
                        raise RuntimeError(
                            f'`{required_parameter}` parameter is required by '
                            f'`{setup_function.extension_short_name}`.'
                        )
            
            optional_parameters = setup_function.optional_parameters
            if (optional_parameters is not None):
                exhaustible_parameters.difference_update(optional_parameters)
    
    if exhaustible_parameters:
        warnings.warn(
            (
                f'`get_setup_functions` received unused parameters: '
                f'{", ".join(f"{name} = {keyword_parameters[name]!r}" for name in exhaustible_parameters)}.'
            ),
            RuntimeWarning,
            stacklevel = 3,
        )
    
    return setup_functions


def run_setup_functions(client, setup_functions, keyword_parameters):
    """
    Setups the given extensions on the client.
    
    Parameters
    ----------
    client : ``Client``
        The client on who the extensions should be setupped.
    setup_functions : `None`, `set` of ``SetupFunction``
        The setup functions to run with the client.
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters to get the extensions's parameters from.
    """
    if (setup_functions is not None):
        for setup_function in setup_functions:
            setup_function(client, keyword_parameters)
