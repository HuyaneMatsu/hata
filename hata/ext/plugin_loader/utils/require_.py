__all__ = ('require', )

from scarletio import get_last_module_frame

from ..exceptions import DoNotLoadPlugin


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
    module_frame = get_last_module_frame()
    if (module_frame is None):
        return
    
    module_globals = module_frame.f_globals
    
    for variable_name in args:
        if variable_name not in module_globals:
            raise DoNotLoadPlugin(variable_name)
    
    for variable_name, expected_value in kwargs.items():
        try:
            variable_value = module_globals[variable_name]
        except KeyError:
            raise DoNotLoadPlugin(variable_name) from None
        
        if variable_value is expected_value:
            continue
        
        if isinstance(expected_value, type) and isinstance(variable_value, expected_value):
            continue
        
        raise DoNotLoadPlugin(variable_name, variable_value, expected_value)
