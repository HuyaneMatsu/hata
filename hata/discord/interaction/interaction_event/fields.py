__all__ = ()

from ...application import Application, Entitlement
from ...channel import Channel, ChannelType, create_partial_channel_from_id
from ...field_parsers import (
    default_entity_parser_factory, entity_id_parser_factory, flag_parser_factory, force_string_parser_factory,
    int_parser_factory, nullable_entity_array_parser_factory, nullable_entity_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_optional_putter_factory, entity_id_putter_factory, entity_putter_factory, force_string_putter_factory,
    int_putter_factory, nullable_entity_array_optional_putter_factory, preinstanced_putter_factory,
    string_flag_putter_factory
)
from ...field_validators import (
    default_entity_validator_factory, entity_id_validator_factory, flag_validator_factory,
    force_string_validator_factory, int_conditional_validator_factory, nullable_entity_array_validator_factory,
    nullable_entity_validator_factory, preinstanced_validator_factory
)
from ...guild import (
    Guild, create_interaction_guild_data, create_partial_guild_from_id,
    create_partial_guild_from_interaction_guild_data
)
from ...guild.guild.guild_boost_perks import LEVEL_0, LEVEL_MAX
from ...localization import Locale
from ...localization.utils import LOCALE_DEFAULT
from ...message import Message
from ...message.message_interaction.fields import (
    parse_authorizer_user_ids, put_authorizer_user_ids, validate_authorizer_user_ids
)
from ...permission import Permission
from ...permission.permission import PERMISSION_PRIVATE
from ...user import ClientUserBase, User, ZEROUSER

from ..interaction_metadata import InteractionMetadataBase

from .preinstanced import InteractionType


# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id = entity_id_optional_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)


# application_permissions

parse_application_permissions = flag_parser_factory('app_permissions', Permission)
put_application_permissions = string_flag_putter_factory('app_permissions')
validate_application_permissions = flag_validator_factory('application_permissions', Permission)


# attachment_size_limit

parse_attachment_size_limit = int_parser_factory('attachment_size_limit', LEVEL_0.attachment_size_limit)
put_attachment_size_limit = int_putter_factory('attachment_size_limit')
validate_attachment_size_limit = int_conditional_validator_factory(
    'attachment_size_limit',
    LEVEL_0.attachment_size_limit,
    (
        lambda attachment_size_limit:
        attachment_size_limit >= LEVEL_0.attachment_size_limit and attachment_size_limit <= LEVEL_MAX.attachment_size_limit
    ),
    f'>= {LEVEL_0.attachment_size_limit} and <= {LEVEL_MAX.attachment_size_limit}',
)


# authorizer_user_ids

# Imported from `...message.message_interaction.fields`.
# They are the same.
# It does not matter where we define them.
#
# parse_authorizer_user_ids = ...
# put_authorizer_user_ids = ...
# validate_authorizer_user_ids = ...


# channel

parse_channel = default_entity_parser_factory(
    'channel', Channel, default_factory = lambda : create_partial_channel_from_id(0, ChannelType.unknown, 0)
)
put_channel = entity_putter_factory('channel', Channel, force_include_internals = True)
validate_channel = default_entity_validator_factory(
    'channel', Channel, default_factory = lambda : create_partial_channel_from_id(0, ChannelType.unknown, 0)
)

# entitlements

parse_entitlements = nullable_entity_array_parser_factory('entitlements', Entitlement)
put_entitlements = nullable_entity_array_optional_putter_factory(
    'entitlements', Entitlement, force_include_internals = True,
)
validate_entitlements = nullable_entity_array_validator_factory('entitlements', Entitlement)

# guild

def parse_guild(data):
    """
    Parses out the interaction's guild from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    guild_data = data.get('guild', None)
    if (guild_data is not None):
        return create_partial_guild_from_interaction_guild_data(guild_data)
    
    guild_id = data.get('guild_id', None)
    if (guild_id is not None):
        return create_partial_guild_from_id(int(guild_id))
    
    return None


def put_guild(guild, data, defaults):
    """
    Puts the given `guild''s data into the given interaction data.
    
    Parameters
    ----------
    guild : ``None | Guild``
        The guild to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (guild is not None) or defaults:
        if guild is None:
            guild_data = None
            guild_id = None
            guild_locale = None
        else:
            guild_data = create_interaction_guild_data(guild)
            guild_id = str(guild.id)
            guild_locale = guild.locale.value
        
        data['guild'] = guild_data
        data['guild_id'] = guild_id
        data['guild_locale'] = guild_locale
    
    return data


validate_guild = nullable_entity_validator_factory('guild', Guild)

# guild_locale

parse_guild_locale = preinstanced_parser_factory('guild_locale', Locale, LOCALE_DEFAULT)
put_guild_locale = preinstanced_putter_factory('guild_locale')
validate_guild_locale = preinstanced_validator_factory('guild_locale', Locale)

# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
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
            f'{type(interaction).__name__}; {interaction!r}.'
        )
    
    if not isinstance(interaction, interaction_type.metadata_type):
        raise TypeError(
            f'Interactions of `{interaction_type!r}` type event can only be '
            f'`{interaction_type.metadata_type.__name__}` instances. '
            f'Make sure to pass the correct `interaction_type` parameter. '
            f'Got {type(interaction).__name__}; {interaction!r}.'
        )
    
    return interaction

# message

parse_message = nullable_entity_parser_factory('message', Message)

def put_message(message, data, defaults):
    """
    Puts the given `message` into the given data.
    
    Parameters
    ----------
    message : `None`, ``Message``
        The message to put into the given `data`.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
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
put_token = force_string_putter_factory('token')
validate_token = force_string_validator_factory('token', 0, 1024)

# type

parse_type = preinstanced_parser_factory('type', InteractionType, InteractionType.none)
put_type = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('interaction_type', InteractionType)

# user & user_permissions

def parse_user(data, guild_id = 0):
    """
    Parses out the interaction event's user from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Interaction event data.
    guild_id : `int` = `0`, Optional (Keyword only)
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


def put_user(user, data, defaults, *, guild_id = 0):
    """
    Puts the given `user` into the given data.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to put into the given `data`.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The user's specific guild's identifier to use for getting the user's local profile.
    
    Returns
    -------
    data : `dict<str, object>`
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


validate_user = default_entity_validator_factory('user', ClientUserBase, default = ZEROUSER)

# user_locale

parse_user_locale = preinstanced_parser_factory('locale', Locale, LOCALE_DEFAULT)
put_user_locale = preinstanced_putter_factory('locale')
validate_user_locale = preinstanced_validator_factory('user_locale', Locale)

# user_permissions

def parse_user_permissions(data):
    """
    Parses out the interaction's user's permissions from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
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


def put_user_permissions(user_permissions, data, defaults):
    """
    Puts the given `user_permissions` into the given data.
    
    Parameters
    ----------
    user_permissions : ``Permission``
        The permission to put into the given `data`.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    try:
        guild_profile_data = data['member']
    except KeyError:
        pass
    else:
        guild_profile_data['permissions'] = format(user_permissions, 'd')
    
    return data

validate_user_permissions = flag_validator_factory('user_permissions', Permission)
