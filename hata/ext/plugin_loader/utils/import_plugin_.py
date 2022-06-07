__all__ = ('import_plugin',)

from os.path import basename as get_file_name, splitext as split_file_name_and_extension

from scarletio import export, get_last_module_frame

from ..plugin import PLUGINS
from ..plugin_loader import PLUGIN_LOADER


@export
def import_plugin(plugin_name, *variable_names, **keyword_parameters):
    """
    Imports from the given plugin.
    
    Parameters
    ----------
    plugin_name : `str`
        the plugin's name to import.
    
    *variable_names : `str`
        Variables to load from the plugin.
        
        > If no variable is defined, the module is returned instead.

    **keyword_parameters : Keyword parameters
        Additional parameters to create the plugin with.
    
    Returns
    -------
    imported_variables : `Any`, `list` of `Any`
        The imported variable(s).
    
    Raises
    ------
    ImportError
        - Cannot find the designated plugin.
    RuntimeError
        - If called from non plugin file.
    TypeError
        - If `plugin_name` is not a string.
        - If `variables_to_import` contains a non string.
    ValueError
        - If `plugin_name`'s syntax is incorrect.
        - If `variable_names` contains a non identifier.
    PluginError
        - Any exception raised by the other plugin is funneled.
    """
    # Validate input types
    if not isinstance(plugin_name, str):
        raise TypeError(
            f'plugin_name` can be `str`, got {plugin_name.__class__.__name__}; {plugin_name!r}.'
        )
    
    for variable_name in variable_names:
        if not isinstance(variable_name, str):
            raise TypeError(
                f'`variable_names` can contain only `str`, got {plugin_name.__class__.__name__}; '
                f'{plugin_name!r}; variable_names={variable_names!r}.'
            )
        
        if not variable_name.isidentifier():
            raise ValueError
        
    
    # Validate `plugin_name` syntax.
    if not plugin_name:
        raise ValueError(
            f'`plugin_name`\s syntax is incorrect; Cannot be empty string.'
        )
    
    plugin_name_parts = plugin_name.split('.')
    expects_only_identifiers = False
    
    for plugin_name_part in plugin_name_parts:
        if not expects_only_identifiers:
            if not plugin_name_part:
                continue
            
            expects_only_identifiers = True
        
        if not plugin_name_part:
            raise ValueError(
                f'`plugin_name`\s syntax is incorrect; two dot character cannot follow an identifier; got: '
                f'{plugin_name!r}.'
            )
        
        if not plugin_name_part.isidentifier():
            raise ValueError(
                f'`plugin_name`\s syntax is incorrect; {plugin_name_part!r} is not an identifier; got: '
                f'{plugin_name!r}.'
            )
    
    if not plugin_name_parts[-1]:
        raise ValueError(
            f'`plugin_name`\s syntax is incorrect; Cannot end with dot character; got: {plugin_name!r}.'
        )
    
    
    frame = get_last_module_frame()
    if (frame is None):
        spec = None
    else:
        spec = frame.f_globals.get('__spec__', None)
    
    if spec is None:
        raise RuntimeError(
            f'`import_plugin` can only be called from an plugin.'
        )
    
    local_name = spec.name
    
    is_init_file = (split_file_name_and_extension(get_file_name(spec.origin))[0] == '__init__')
    
    empty_count = 0
    for plugin_name_part in plugin_name_parts:
        if plugin_name_part:
            break
        
        empty_count += 1
        continue
    
    if empty_count:
        local_name_parts = local_name.split('.')
        
        if len(local_name_parts) < empty_count:
            raise ImportError(
                f'`{plugin_name!r}`\'s scope out of parent root\'s scope.'
            )
        
        plugin_name_parts = plugin_name_parts[empty_count:]
        
        empty_count = empty_count - is_init_file
        if empty_count:
            local_name_parts = local_name_parts[:-empty_count]
        
        built_name = '.'.join(local_name_parts+plugin_name_parts)
        
    else:
        built_name = plugin_name
    
    plugin = PLUGIN_LOADER.register_and_load(built_name, **keyword_parameters)
    
    current_plugin = PLUGINS.get(local_name, None)
    if (current_plugin is not None):
        if current_plugin.is_directory():
            current_plugin.add_sub_module_plugin(plugin)
        else:
            current_plugin.add_child_plugin(plugin)
            plugin.add_parent_plugin(current_plugin)
        
    variable_names_length = len(variable_names)
    module = plugin._spec.get_module_proxy()
    if variable_names_length == 0:
        return module
    
    variables = []
    
    for variable_name in variable_names:
        try:
            variable = getattr(module, variable_name)
        except AttributeError:
            raise ImportError(
                f'Cannot import `{variable_name}` from `{plugin.name}`.'
            ) from None
        
        variables.append(variable)
    
    if variable_names_length == 1:
        return variables[0]
    
    return variables
