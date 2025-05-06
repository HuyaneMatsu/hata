__all__ = ()

from .....discord.application import ApplicationIntegrationType
from .....discord.guild import Guild
from .....discord.application_command.application_command.constants import (
    NAME_LENGTH_MAX as APPLICATION_COMMAND_NAME_LENGTH_MAX,
    NAME_LENGTH_MIN as APPLICATION_COMMAND_NAME_LENGTH_MIN
)
from .....discord.application_command.application_command.preinstanced import (
    ApplicationCommandIntegrationContextType,
)
from .....discord.permission import Permission
from .....discord.preconverters import preconvert_bool, preconvert_flag, preconvert_snowflake



def _reset_application_command_schema(entity):
    """
    Resets the slasher application commands schema.
    
    Parameters
    ----------
    entity : ``CommandBaseApplicationCommand``
        The command to reset's its schema if applicable.
    """
    schema = entity._schema
    if (schema is not None):
        entity._schema = None
        
        parent_reference = entity._parent_reference
        if (parent_reference is not None):
            slasher = parent_reference()
            
            if (slasher is not None):
                slasher._schema_reset(entity)


def _validate_delete_on_unload(delete_on_unload):
    """
    Validates the given `delete_on_unload` value.
    
    Parameters
    ----------
    delete_on_unload : `bool`
        The value to validate.
    
    Returns
    -------
    delete_on_unload : `bool`
    
    Raises
    ------
    TypeError
        If `delete_on_unload` type is incorrect.
    """
    return preconvert_bool(delete_on_unload, 'delete_on_unload')


def _validate_nsfw(nsfw):
    """
    Validates the given `nsfw` value.
    
    Parameters
    ----------
    nsfw : `bool`
        The value to validate.
    
    Returns
    -------
    nsfw : `bool`
    
    Raises
    ------
    TypeError
        If `nsfw` type is incorrect.
    """
    return preconvert_bool(nsfw, 'nsfw')


def _validate_is_global(is_global):
    """
    Validates the given `is_global` value.
    
    Parameters
    ----------
    is_global : `bool`
        The value to validate.
    
    Returns
    -------
    is_global : `bool`
    
    Raises
    ------
    TypeError
        If `is_global` type is incorrect.
    """
    return preconvert_bool(is_global, 'is_global')


def _validate_1_guild(guild):
    """
    Validates 1 guild value.
    
    Parameters
    ----------
    guild : `Guild | int`
        The guild value to validate.
    
    Returns
    -------
    guild_id : `int`
    
    Raises
    ------
    TypeError
        If `guild`'s type is incorrect.
    ValueError
        If `guild`'s value is incorrect.
    """
    if isinstance(guild, Guild):
        guild_id = guild.id
    elif isinstance(guild, (int, str)):
        guild_id = preconvert_snowflake(guild, 'guild')
    else:
        raise TypeError(
            f'`guild` can be `{type(Guild).__name__}`, `int`, got {type(guild).__name__}; {guild!r}.'
        )
    
    return guild_id


def _validate_guild(guild):
    """
    Validates the given `guild` value.
    
    Parameters
    ----------
    guild : `Guild | int | (list | set)<Guild | int>`
        The `is_global` value to validate.
    
    Returns
    -------
    guild_ids : `set<int>`
        The validated `guild` value.
    
    Raises
    ------
    TypeError
        If `guild`'s type is incorrect.
    ValueError
        If `guild`'s value is incorrect.
    """
    guild_ids = set()
    
    if isinstance(guild, (list, set)):
        for guild_value in guild:
            guild_id = _validate_1_guild(guild_value)
            guild_ids.add(guild_id)
        
        if not guild_ids:
            raise ValueError(
                f'`guild` cannot be empty, got {guild!r}.'
            )
    else:
        guild_id = _validate_1_guild(guild)
        guild_ids.add(guild_id)
    
    return guild_ids


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
    ValueError
        If `name` length is out of the expected range [1:32].
    """
    if name is not None:
        name_type = type(name)
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(
                f'`name` can be `None`, `str`, got {name_type.__name__}; {name!r}.'
            )
        
        name_length = len(name)
        if (
            name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or
            name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX
        ):
            raise ValueError(
                f'`name` length is out of the expected range '
                f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:'
                f'{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got {name_length!r}; {name!r}.'
            )
    
    return name


def _validate_required_permissions(required_permissions):
    """
    Validates the given `required_permissions` value.
    
    Parameters
    ----------
    required_permissions : `int | Permission`
        The `required_permissions` value to validate.
    
    Returns
    -------
    required_permissions : ``Permission``
    
    Raises
    ------
    TypeError
        If `required_permissions`'s type is incorrect.
    """
    return preconvert_flag(required_permissions, 'required_permissions', Permission)


APPLICATION_COMMAND_INTEGRATION_CONTEXT_TYPES_BY_ATTRIBUTE_NAME = {
    integration_context_type.name.replace(' ', '_'): integration_context_type
    for integration_context_type
    in ApplicationCommandIntegrationContextType.INSTANCES.values()
}


APPLICATION_INTEGRATION_TYPES_BY_ATTRIBUTE_NAME = {
    integration_type.name.replace(' ', '_'): integration_type
    for integration_type
    in ApplicationIntegrationType.INSTANCES.values()
    
}


def _fail_preinstanced_array_validation_single(field_name, preinstanced_type, string_resolution_table, value):
    """
    Fails preinstanced array validation when checking for a single instance.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    preinstanced_type : `type<PreinstancedBase>`
        The preinstanced type we are validating for.
    string_resolution_table : `dict<str, PreinstancedBase>`
        String resolution table for the preinstanced type.
    value : `object`
        The value that failed on validation.
    
    Raises
    ------
    TypeError
    """
    allowed_strings_string = ', '.join(sorted(repr(string) for string in string_resolution_table.keys()))
    
    raise TypeError(
        f'`{field_name}` can be `None`, `{preinstanced_type.__name__}`, `int`, '
        f'`str` (any of: {allowed_strings_string!s}), or `iterable`, got '
        f'{type(value).__name__}; {value!r}.'
    )


def _fail_preinstanced_array_validation_element(
    field_name, preinstanced_type, string_resolution_table, preinstanced_array, value
):
    """
    Fails preinstanced array validation when checking for an element.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    preinstanced_type : `type<PreinstancedBase>`
        The preinstanced type we are validating for.
    string_resolution_table : `dict<str, PreinstancedBase>`
        String resolution table for the preinstanced type.
    preinstanced_array : `object`
        The given value to validate.
    value : `object`
        The value that failed on validation.
    
    Raises
    ------
    TypeError
    """
    allowed_strings_string = ', '.join(sorted(repr(string) for string in string_resolution_table.keys()))
    
    raise TypeError(
        f'`{field_name}` elements can be `{preinstanced_type.__name__}`, `int`, '
        f'`str` (any of: {allowed_strings_string!s}), or `iterable`, got '
        f'got {type(value).__name__}; {value!r}; preinstanced_array = {preinstanced_array!r}'
    )


def _pre_validate_preinstanced_array(field_name, preinstanced_type, string_resolution_table, preinstanced_array):
    """
    Validates the given preinstanced array.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    preinstanced_type : `type<PreinstancedBase>`
        The preinstanced type we are validating for.
    string_resolution_table : `dict<str, preinstanced_type>`
        String resolution table for the preinstanced type.
    preinstanced_array : `object`
        The given value to validate.
    
    Returns
    -------
    preinstanced_array : `None | tuple<preinstanced_type>`
    
    Raises
    ------
    TypeError
    """
    if preinstanced_array is None:
        return None
    
    if isinstance(preinstanced_array, preinstanced_type):
        return (preinstanced_array,)
    
    if isinstance(preinstanced_array, str):
        preinstanced = string_resolution_table.get(preinstanced_array, None)
        if preinstanced is None:
            _fail_preinstanced_array_validation_single(
                field_name, preinstanced_type, string_resolution_table, preinstanced_array
            )
        
        return (preinstanced,)
    
    if isinstance(preinstanced_array, int):
        return (ApplicationCommandIntegrationContextType(preinstanced_array),)
    
    if getattr(preinstanced_array, '__iter__', None) is None:
        _fail_preinstanced_array_validation_single(
            field_name, preinstanced_type, string_resolution_table, preinstanced_array
        )
    
    unique_elements = None
    
    for preinstanced in preinstanced_array:
        if isinstance(preinstanced, preinstanced_type):
            pass
        
        elif isinstance(preinstanced, str):
            preinstanced = string_resolution_table.get(preinstanced, None)
            if preinstanced is None:
                _fail_preinstanced_array_validation_element(
                    field_name, preinstanced_type, string_resolution_table, preinstanced_array, preinstanced
                )
            
        elif isinstance(preinstanced, int):
            preinstanced = preinstanced_type(preinstanced)
        
        else:
            _fail_preinstanced_array_validation_element(
                field_name, preinstanced_type, string_resolution_table, preinstanced_array, preinstanced
            )
        
        if unique_elements is None:
            unique_elements = set()
        
        unique_elements.add(preinstanced)
    
    if unique_elements is None:
        return None
    
    return tuple(sorted(unique_elements))


def _validate_integration_context_types(integration_context_types):
    """
    Validates the given `integration_context_types` value.
    
    Parameters
    ----------
    integration_context_types : `None`, ``ApplicationCommandIntegrationContextType``, `int`, `str`, \
            `iterable<ApplicationCommandIntegrationContextType | int | str>`
        The places where the application command shows up.
    
    Returns
    -------
    integration_context_types : `None | tuple<ApplicationCommandIntegrationContextType>`
    
    Raises
    ------
    TypeError
    """
    return _pre_validate_preinstanced_array(
        'integration_context_types',
        ApplicationCommandIntegrationContextType,
        APPLICATION_COMMAND_INTEGRATION_CONTEXT_TYPES_BY_ATTRIBUTE_NAME,
        integration_context_types,
    )


def _validate_integration_types(integration_types):
    """
    Validates the given `integration_types` value.
    
    Parameters
    ----------
    integration_types : `None`, ``ApplicationIntegrationType``, `int`, `str`, \
            `iterable<ApplicationIntegrationType | int | str>`
        The options where the application command can be integrated to.
    
    Returns
    -------
    integration_types : `None | tuple<ApplicationIntegrationType>`
    
    Raises
    ------
    TypeError
    """
    integration_types = _pre_validate_preinstanced_array(
        'integration_types',
        ApplicationIntegrationType,
        APPLICATION_INTEGRATION_TYPES_BY_ATTRIBUTE_NAME,
        integration_types,
    )
    if (integration_types is None):
        integration_types = (ApplicationIntegrationType.guild_install,)
    
    return integration_types
