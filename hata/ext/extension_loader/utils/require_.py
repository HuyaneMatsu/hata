__all__ = ('require', )

from sys import _getframe as get_frame

from ..exceptions import DoNotLoadExtension


def require(*args, **kwargs):
    """
    Requires the given parameters.
    
    Parameters
    ----------
    *args : Parameters
        Required variable names.
    **kwargs : Keyword parameters
        Variables and their expected value / type.
    """
    module_globals = get_frame().f_back.f_globals
    
    for variable_name in args:
        if variable_name not in module_globals:
            raise DoNotLoadExtension(variable_name)
    
    for variable_name, expected_value in kwargs.items():
        try:
            variable_value = module_globals[variable_name]
        except KeyError:
            raise DoNotLoadExtension(variable_name) from None
        
        if variable_value is expected_value:
            continue
        
        if isinstance(expected_value, type) and isinstance(variable_value, expected_value):
            continue
        
        raise DoNotLoadExtension(variable_name, variable_value, expected_value)
