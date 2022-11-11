__all__ = ()

from .....discord.guild import Guild
from .....discord.application_command.application_command import _assert__application_command__nsfw
from .....discord.application_command.constants import (
    APPLICATION_COMMAND_NAME_LENGTH_MAX, APPLICATION_COMMAND_NAME_LENGTH_MIN
)
from .....discord.permission import Permission
from .....discord.preconverters import preconvert_bool, preconvert_flag, preconvert_snowflake

from ...utils import UNLOADING_BEHAVIOUR_DELETE, UNLOADING_BEHAVIOUR_INHERIT, UNLOADING_BEHAVIOUR_KEEP


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
    delete_on_unload : `None`, `bool`
        The `delete_on_unload` value to validate.
    
    Returns
    -------
    unloading_behaviour : `int`
        The validated `delete_on_unload` value.
    
    Raises
    ------
    TypeError
        If `delete_on_unload` was not given as `None` nor as `bool`.
    """
    if delete_on_unload is None:
        unloading_behaviour = UNLOADING_BEHAVIOUR_INHERIT
    else:
        delete_on_unload = preconvert_bool(delete_on_unload, 'delete_on_unload')
        if delete_on_unload:
            unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
    
    return unloading_behaviour


def _validate_allow_by_default(allow_by_default):
    """
    Validates the given `allow_by_default` value.
    
    Parameters
    ----------
    allow_by_default : `None`, `bool`
        The `allow_by_default` value to validate.
    
    Returns
    -------
    allow_by_default : `None`, `bool`
        The validated `allow_by_default` value.
    
    Raises
    ------
    TypeError
        If `allow_by_default` was not given as `None`, `bool`.
    """
    if (allow_by_default is not None):
        allow_by_default = preconvert_bool(allow_by_default, 'allow_by_default')
    
    return allow_by_default


def _validate_allow_in_dm(allow_in_dm):
    """
    Validates the given `allow_in_dm` value.
    
    Parameters
    ----------
    allow_in_dm : `None`, `bool`
        The `allow_in_dm` value to validate.
    
    Returns
    -------
    allow_in_dm : `None`, `bool`
        The validated `allow_in_dm` value.
    
    Raises
    ------
    TypeError
        If `allow_in_dm` was not given as `None`, `bool`.
    """
    if (allow_in_dm is not None):
        allow_in_dm = preconvert_bool(allow_in_dm, 'allow_in_dm')
    
    return allow_in_dm


def _validate_is_global(is_global):
    """
    Validates the given `is_global` value.
    
    Parameters
    ----------
    is_global : `None`, `bool`
        The `is_global` value to validate.
    
    Returns
    -------
    is_global : `bool`
        The validated `is_global` value.
    
    Raises
    ------
    TypeError
        If `is_global` was not given as `None` nor as `bool`.
    """
    if is_global is None:
        is_global = False
    else:
        is_global = preconvert_bool(is_global, 'is_global')
    
    return is_global


def _validate_1_guild(guild):
    """
    Validates 1 guild value.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild value to validate.
    
    Returns
    -------
    guild_id : `int`
        Validated guild value converted to `int`.
    
    Raises
    ------
    TypeError
        If `guild` was not given neither as ``Guild`` nor `int`.
    ValueError
        If `guild` is an integer out of uint64 value range.
    """
    if isinstance(guild, Guild):
        guild_id = guild.id
    elif isinstance(guild, (int, str)):
        guild_id = preconvert_snowflake(guild, 'guild')
    else:
        raise TypeError(
            f'`guild`can be `{Guild.__class__.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
        )
    
    return guild_id


def _validate_guild(guild):
    """
    Validates the given `guild` value.
    
    Parameters
    ----------
    guild : `None`, `int`, ``Guild``, (`list`, `set`) of (`int`, ``Guild``
        The `is_global` value to validate.
    
    Returns
    -------
    guild_ids : `None`, `set` of `int`
        The validated `guild` value.
    
    Raises
    ------
    TypeError
        If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
    ValueError
        - If `guild` is given as an empty container.
        - If `guild` is or contains an integer out of uint64 value range.
    """
    if guild is None:
        guild_ids = None
    else:
        guild_ids = set()
        if isinstance(guild, (list, set)):
            for guild_value in guild:
                guild_id = _validate_1_guild(guild_value)
                guild_ids.add(guild_id)
        else:
            guild_id = _validate_1_guild(guild)
            guild_ids.add(guild_id)
        
        if not guild_ids:
            raise ValueError(
                f'`guild` cannot be empty container, got {guild!r}.'
            )
    
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
        name_type = name.__class__
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


def _validate_nsfw(nsfw):
    """
    Validates the given `nsfw` value.
    
    Parameters
    ----------
    nsfw : `None`, `bool`
        The `nsfw` value to validate.
    
    Returns
    -------
    nsfw : `None`, `bool`
        The validated `nsfw` value.
    
    Raises
    ------
    TypeError
        If `nsfw` was not given as `None`, `bool`.
    """
    try:
        _assert__application_command__nsfw(nsfw)
    except AssertionError as err:
        raise TypeError(*err.args) from err
    
    return nsfw


def _validate_required_permissions(required_permissions):
    """
    Validates the given `required_permissions` value.
    
    Parameters
    ----------
    required_permissions : `None`, `int`, ``Permission``
        The `required_permissions` value to validate.
    
    Returns
    -------
    required_permissions : `None`, ``Permission``
        The validated `required_permissions` value.
    
    Raises
    ------
    TypeError
        If `required_permissions` was not given as `None`, ``Permission``, `int`.
    """
    if (required_permissions is not None):
        required_permissions = preconvert_flag(required_permissions, 'required_permissions', Permission)
    
    return required_permissions
