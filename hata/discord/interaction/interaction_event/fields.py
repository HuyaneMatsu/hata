__all__ = ()

from ...application import Application
from ...channel import Channel, ChannelType, create_partial_channel_from_id
from ...field_parsers import (
    default_entity_parser_factory, entity_id_parser_factory, flag_parser_factory, force_string_parser_factory,
    nullable_entity_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_optional_putter_factory, entity_id_putter_factory, entity_putter_factory, force_string_putter_factory,
    preinstanced_putter_factory, string_flag_putter_factory
)
from ...field_validators import (
    default_entity_validator, entity_id_validator_factory, flag_validator_factory, force_string_validator_factory,
    nullable_entity_validator_factory, preinstanced_validator_factory
)
from ...guild import Guild
from ...localization import Locale
from ...localization.utils import LOCALE_DEFAULT
from ...message import Message
from ...permission import Permission
from ...permission.permission import PERMISSION_PRIVATE
from ...user import ClientUserBase, User, ZEROUSER

from ..interaction_metadata import InteractionMetadataBase

from .preinstanced import InteractionType

# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id_into = entity_id_optional_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)

# application_permissions

parse_application_permissions = flag_parser_factory('app_permissions', Permission)
put_application_permissions_into = string_flag_putter_factory('app_permissions')
validate_application_permissions = flag_validator_factory('application_permissions', Permission)

# channel

parse_channel = default_entity_parser_factory(
    'channel', Channel, default_factory = lambda : create_partial_channel_from_id(0, ChannelType.unknown, 0)
)
put_channel_into = entity_putter_factory('channel', Channel)
validate_channel = default_entity_validator(
    'channel', Channel, default_factory = lambda : create_partial_channel_from_id(0, ChannelType.unknown, 0)
)

# guild_locale

parse_guild_locale = preinstanced_parser_factory('guild_locale', Locale, LOCALE_DEFAULT)
put_guild_locale_into = preinstanced_putter_factory('guild_locale')
validate_guild_locale = preinstanced_validator_factory('guild_locale', Locale)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id')

# interaction

def validate_interaction(interaction, interaction_type):
    """
    Validates the given `interaction`.
    
    Parameters
    ----------
    interaction : `None`, ``InteractionMetadataBase``
        Interaction metadata.
    
    interaction_type : ``InteractionType``
        The respective interaction type.
    
    Returns
    -------
    interaction : ``InteractionMetadataBase``
    
    Raises
    ------
    TypeError
        - If `interaction`-s type is incorrect.
    """
    if interaction is None:
        return interaction_type.metadata_type()
    
    if not isinstance(interaction, InteractionMetadataBase):
        raise TypeError(
            f'`interaction` can be `None`, `{InteractionMetadataBase.__name__}` instance, got '
            f'{interaction.__class__.__name__}; {interaction!r}.'
        )
    
    if not isinstance(interaction, interaction_type.metadata_type):
        raise TypeError(
            f'Interactions of `{interaction_type!r}` type event can only be '
            f'`{interaction_type.metadata_type.__name__}` instances. '
            f'Make sure to pass the correct `interaction_type` parameter. '
            f'Got {interaction.__class__.__name__}; {interaction!r}.'
        )
    
    return interaction

# locale

parse_locale = preinstanced_parser_factory('locale', Locale, LOCALE_DEFAULT)
put_locale_into = preinstanced_putter_factory('locale')
validate_locale = preinstanced_validator_factory('locale', Locale)

# message

parse_message = nullable_entity_parser_factory('message', Message)

def put_message_into(message, data, defaults):
    """
    Puts the given `message` into the given data.
    
    Parameters
    ----------
    message : `None`, ``Message``
        The message to put into the given `data`.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (message is not None):
        if message is None:
            entity_data = None
        else:
            entity_data = message.to_data(defaults = defaults, include_internals = True)
        
        data['message'] = entity_data
    
    return data

validate_message = nullable_entity_validator_factory('message', Message)

# token

parse_token = force_string_parser_factory('token')
put_token_into = force_string_putter_factory('token')
validate_token = force_string_validator_factory('token', 0, 1024)

# type

parse_type = preinstanced_parser_factory('type', InteractionType, InteractionType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('interaction_type', InteractionType)

# user & user_permissions

def parse_user(data, guild_id):
    """
    Parses out the interaction event's user from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Interaction event data.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    # user
    try:
        guild_profile_data = data['member']
    except KeyError:
        try:
            user_data = data['user']
        except KeyError:
            return ZEROUSER
        
        guild_profile_data = None
    else:
        try:
            user_data = guild_profile_data['user']
        except KeyError:
            return ZEROUSER
    
    return User.from_data(user_data, guild_profile_data, guild_id)


def put_user_into(user, data, defaults, *, guild_id = 0):
    """
    Puts the given `user` into the given data.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to put into the given `data`.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The user's specific guild's identifier to use for getting the user's local profile.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    try:
        guild_profile = user.guild_profiles[guild_id]
    except KeyError:
        data['user'] = user.to_data(defaults = defaults, include_internals = True)
    
    else:
        guild_profile_data = guild_profile.to_data(defaults = defaults, include_internals = True)
        guild_profile_data['user'] = user.to_data(defaults = defaults, include_internals = True)
        
        data['member'] = guild_profile_data
    
    return data


validate_user = default_entity_validator('user', ClientUserBase, default = ZEROUSER)

# user_permissions

def parse_user_permissions(data):
    """
    Parses out the interaction's user's permissions from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Interaction data.
    
    Return
    ------
    user_permissions : ``Permission``
    """
    try:
        guild_profile_data = data['member']
    except KeyError:
        return PERMISSION_PRIVATE
    
    try:
        user_permissions = guild_profile_data['permissions']
    except KeyError:
        return PERMISSION_PRIVATE
    
    return Permission(user_permissions)


def put_user_permissions_into(user_permissions, data, defaults):
    """
    Puts the given `user_permissions` into the given data.
    
    Parameters
    ----------
    user_permissions : ``Permission``
        The permission to put into the given `data`.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    try:
        guild_profile_data = data['member']
    except KeyError:
        pass
    else:
        guild_profile_data['permissions'] = format(user_permissions, 'd')
    
    return data

validate_user_permissions = flag_validator_factory('user_permissions', Permission)
