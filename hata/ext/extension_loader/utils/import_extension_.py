__all__ = ('import_extension',)

from os.path import basename as get_file_name, splitext as split_file_name_and_extension

from scarletio import export, get_last_module_frame

from ..extension import EXTENSIONS
from ..extension_loader import EXTENSION_LOADER


@export
def import_extension(extension_name, *variable_names, **keyword_parameters):
    """
    Imports from the given extension.
    
    Parameters
    ----------
    extension_name : `str`
        the extension's name to import.
    
    *variable_names : `str`
        Variables to load from the extension.
        
        > If no variable is defined, the module is returned instead.

    **keyword_parameters : Keyword parameters
        Additional parameters to create the extension with.
    
    Returns
    -------
    imported_variables : `Any`, `list` of `Any`
        The imported variable(s).
    
    Raises
    ------
    ImportError
        - Cannot find the designated extension.
    RuntimeError
        - If called from non extension file.
    TypeError
        - If `extension_name` is not a string.
        - If `variables_to_import` contains a non string.
    ValueError
        - If `extension_name`'s syntax is incorrect.
        - If `variable_names` contains a non identifier.
    ExtensionError
        - Any exception raised by the other extension is funneled.
    """
    # Validate input types
    if not isinstance(extension_name, str):
        raise TypeError(
            f'extension_name` can be `str`, got {extension_name.__class__.__name__}; {extension_name!r}.'
        )
    
    for variable_name in variable_names:
        if not isinstance(variable_name, str):
            raise TypeError(
                f'`variable_names` can contain only `str`, got {extension_name.__class__.__name__}; '
                f'{extension_name!r}; variable_names={variable_names!r}.'
            )
        
        if not variable_name.isidentifier():
            raise ValueError
        
    
    # Validate `extension_name` syntax.
    if not extension_name:
        raise ValueError(
            f'`extension_name`\s syntax is incorrect; Cannot be empty string.'
        )
    
    extension_name_parts = extension_name.split('.')
    expects_only_identifiers = False
    
    for extension_name_part in extension_name_parts:
        if not expects_only_identifiers:
            if not extension_name_part:
                continue
            
            expects_only_identifiers = True
        
        if not extension_name_part:
            raise ValueError(
                f'`extension_name`\s syntax is incorrect; two dot character cannot follow an identifier; got: '
                f'{extension_name!r}.'
            )
        
        if not extension_name_part.isidentifier():
            raise ValueError(
                f'`extension_name`\s syntax is incorrect; {extension_name_part!r} is not an identifier; got: '
                f'{extension_name!r}.'
            )
    
    if not extension_name_parts[-1]:
        raise ValueError(
            f'`extension_name`\s syntax is incorrect; Cannot end with dot character; got: {extension_name!r}.'
        )
    
    
    frame = get_last_module_frame()
    if (frame is None):
        spec = None
    else:
        spec = frame.f_globals.get('__spec__', None)
    
    if spec is None:
        raise RuntimeError(
            f'`import_extension` can only be called from an extension.'
        )
    
    local_name = spec.name
    
    is_init_file = (split_file_name_and_extension(get_file_name(spec.origin))[0] == '__init__')
    
    empty_count = 0
    for extension_name_part in extension_name_parts:
        if extension_name_part:
            break
        
        empty_count += 1
        continue
    
    if empty_count:
        local_name_parts = local_name.split('.')
        
        if len(local_name_parts) < empty_count:
            raise ImportError(
                f'`{extension_name!r}`\'s scope out of parent root\'s scope.'
            )
        
        extension_name_parts = extension_name_parts[empty_count:]
        
        empty_count = empty_count - is_init_file
        if empty_count:
            local_name_parts = local_name_parts[:-empty_count]
        
        built_name = '.'.join(local_name_parts+extension_name_parts)
        
    else:
        built_name = extension_name
    
    extension = EXTENSION_LOADER.load_extension(built_name, **keyword_parameters)
    
    current_extension = EXTENSIONS.get(local_name, None)
    if (current_extension is not None):
        extension.add_child_extension(current_extension)
        current_extension.add_parent_extension(extension)
    
    variable_names_length = len(variable_names)
    module = extension._spec.get_module_proxy()
    if variable_names_length == 0:
        return module
    
    variables = []
    
    for variable_name in variable_names:
        try:
            variable = getattr(module, variable_name)
        except AttributeError:
            raise ImportError(
                f'Cannot import `{variable_name}` from `{extension.name}`.'
            ) from None
        
        variables.append(variable)
    
    if variable_names_length == 1:
        return variables[0]
    
    return variables
