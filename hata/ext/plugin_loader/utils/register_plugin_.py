__all__ = ('register_plugin',)

from ..plugin_loader import PLUGIN_LOADER


def register_plugin(name, *args, **kwargs):
    """
    Registers a plugin.
    
    If the plugin already exists, returns that one.
    
    Parameters
    ----------
    name : `str`, `iterable` of `str`
        The plugin's name to load.
    *args : Parameters
        Additional parameters to create the plugin with.
    **kwargs : Keyword parameters
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
        Variables to assign to an plugin(s)'s module before they are loaded.
        
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
    """
    return PLUGIN_LOADER.add(name, *args, **kwargs)
