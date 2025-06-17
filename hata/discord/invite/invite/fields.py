__all__ = ()

from ...application import Application
from ...channel import (
    Channel, ChannelType, create_partial_channel_data, create_partial_channel_from_data, create_partial_channel_from_id
)
from ...field_parsers import (
    bool_parser_factory, default_entity_parser_factory, flag_parser_factory, force_string_parser_factory,
    int_parser_factory, nullable_date_time_parser_factory, nullable_entity_parser_factory,
    nullable_functional_parser_factory, nullable_int_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, default_entity_putter_factory, entity_id_optional_putter_factory,
    entity_id_putter_factory, flag_optional_putter_factory, force_string_putter_factory, int_putter_factory,
    nullable_date_time_optional_putter_factory, nullable_entity_optional_putter_factory,
    nullable_field_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator_factory, entity_id_validator_factory, flag_validator_factory,
    force_string_validator_factory, int_conditional_validator_factory, nullable_date_time_validator_factory,
    nullable_entity_validator_factory, preinstanced_validator_factory
)
from ...guild import (
    Guild, GuildActivityOverview, create_partial_guild_data, create_partial_guild_from_data, create_partial_guild_from_id
)
from ...user import ClientUserBase, User, ZEROUSER

from .flags import InviteFlag
from .preinstanced import InviteTargetType, InviteType


# approximate_online_count

parse_approximate_online_count = int_parser_factory('approximate_presence_count', 0)
put_approximate_online_count = int_putter_factory('approximate_presence_count')
validate_approximate_online_count = int_conditional_validator_factory(
    'approximate_online_count',
    0,
    lambda approximate_online_count : approximate_online_count >= 0,
    '>= 0',
)

# approximate_user_count

parse_approximate_user_count = int_parser_factory('approximate_member_count', 0)
put_approximate_user_count = int_putter_factory('approximate_member_count')
validate_approximate_user_count = int_conditional_validator_factory(
    'approximate_user_count',
    0,
    lambda approximate_user_count : approximate_user_count >= 0,
    '>= 0',
)

# channel

def parse_channel(data, guild_id = 0):
    """
    Parses a partial channel out of the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Invite data.
    guild_id : `int` = `0`, Optional
        The channel's guild's identifier.
    
    Returns
    -------
    channel : ``None | Channel``
    """
    channel_data = data.get('channel', None)
    if (channel_data is not None):
        return create_partial_channel_from_data(channel_data, guild_id)
    
    # If the data is partial, `channel_id` is received instead of `channel`.
    channel_id = data.get('channel_id', None)
    if (channel_id is not None):
        return create_partial_channel_from_id(int(channel_id), ChannelType.unknown, guild_id)
    
    return None


def put_channel(channel, data, defaults):
    """
    Puts the invite's channel into the given data.
    
    Parameters
    ----------
    channel : ``None | Channel``
        The channel to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if channel is None:
        channel_data = None
        channel_id = None
    else:
        channel_data = create_partial_channel_data(channel)
        channel_id = str(channel.id)
    
    data['channel'] = channel_data
    data['channel_id'] = channel_id
    
    return data


validate_channel = nullable_entity_validator_factory('channel', Channel)

# channel_id

put_channel_id = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)

# code

parse_code = force_string_parser_factory('code')
put_code = force_string_putter_factory('code')
validate_code = force_string_validator_factory('invite_code', 0, 1024)

# created_at

parse_created_at = nullable_date_time_parser_factory('created_at')
put_created_at = nullable_date_time_optional_putter_factory('created_at')
validate_created_at = nullable_date_time_validator_factory('created_at')

# flags

parse_flags = flag_parser_factory('flags', InviteFlag)
put_flags = flag_optional_putter_factory('flags', InviteFlag())
validate_flags = flag_validator_factory('flags', InviteFlag)

# guild

def parse_guild(data):
    """
    Parses a partial guild out of the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Invite data.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    guild_data = data.get('guild', None)
    if (guild_data is not None):
        return create_partial_guild_from_data(guild_data)
    
    # If the data is partial, `guild_id` is received instead of `guild_id`.
    guild_id = data.get('guild_id', None)
    if (guild_id is not None):
        return create_partial_guild_from_id(int(guild_id))
    
    return None


def put_guild(guild, data, defaults):
    """
    Puts the invite's guild into the given data.
    
    Parameters
    ----------
    guild : ``None | Guild``
        The guild to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if guild is None:
        guild_data = None
        guild_id = None
    else:
        guild_data = create_partial_guild_data(guild)
        guild_id = str(guild.id)
    
    data['guild'] = guild_data
    data['guild_id'] = guild_id
    
    return data


validate_guild = nullable_entity_validator_factory('guild', Guild)


# guild_activity_overview

parse_guild_activity_overview = nullable_entity_parser_factory('profile', GuildActivityOverview)
put_guild_activity_overview = nullable_entity_optional_putter_factory(
    'profile', GuildActivityOverview, force_include_internals = True
)
validate_guild_activity_overview = nullable_entity_validator_factory('guild_activity_overview', GuildActivityOverview)


# guild_id

put_guild_id = entity_id_putter_factory('guild_id')

# inviter

parse_inviter = default_entity_parser_factory('inviter', User, default = ZEROUSER)
put_inviter = default_entity_putter_factory('inviter', ClientUserBase, ZEROUSER, force_include_internals = True)
validate_inviter = default_entity_validator_factory('inviter', ClientUserBase, default = ZEROUSER)

# inviter_id | extra for audit logs

validate_inviter_id = entity_id_validator_factory('inviter_id', ClientUserBase)

# max_age

parse_max_age = nullable_int_parser_factory('max_age')
put_max_age = nullable_field_optional_putter_factory('max_age')
validate_max_age = int_conditional_validator_factory(
    'max_age',
    None,
    lambda max_age : max_age >= 0,
    '>= 0',
)

# max_uses

parse_max_uses = nullable_int_parser_factory('max_uses')
put_max_uses = nullable_field_optional_putter_factory('max_uses')
validate_max_uses = int_conditional_validator_factory(
    'max_uses',
    None,
    lambda max_uses : max_uses >= 0,
    '>= 0',
)

# target_application

parse_target_application = nullable_functional_parser_factory('target_application', Application.from_data_invite)


def put_target_application(target_application, data, defaults):
    """
    Puts the invite's target application into the given data.
    
    Parameters
    ----------
    target_application : ``None | Application``
        The application to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (target_application is not None):
        if target_application is None:
            target_application_data = None
        else:
            target_application_data = target_application.to_data_invite(defaults = defaults, include_internals = True)
        
        data['target_application'] = target_application_data
    
    return data


validate_target_application = nullable_entity_validator_factory('target_application', Application)

# put_target_application_id

put_target_application_id = entity_id_optional_putter_factory('target_application_id')
validate_target_application_id = entity_id_validator_factory('target_application_id', Application)

# target_type

parse_target_type = preinstanced_parser_factory(
    'target_type', InviteTargetType, InviteTargetType.none
)


def put_target_type(target_type, data, defaults):
    """
    Puts the invite's target type into the given data.
    
    Parameters
    ----------
    target-type : ``InviteTargetType``
        The target type to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if target_type is not InviteTargetType.none:
        data['target_type'] = target_type.value
    
    return data


validate_target_type = preinstanced_validator_factory('target_type', InviteTargetType)

# target_user

parse_target_user = nullable_entity_parser_factory('target_user', User)
put_target_user = nullable_entity_optional_putter_factory(
    'target_user', ClientUserBase, force_include_internals = True
)
validate_target_user = nullable_entity_validator_factory('target_user', ClientUserBase)

# put_target_user_id

put_target_user_id = entity_id_optional_putter_factory('target_user_id')
validate_target_user_id = entity_id_validator_factory('target_user_id', ClientUserBase)

# temporary

parse_temporary = bool_parser_factory('temporary', False)
put_temporary = bool_optional_putter_factory('temporary', False)
validate_temporary = bool_validator_factory('temporary', False)

# type

parse_type = preinstanced_parser_factory('type', InviteType, InviteType.guild)
put_type = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('invite_type', InviteType)

# validate_unique

put_unique = bool_optional_putter_factory('unique', False)
validate_unique = bool_validator_factory('unique', False)

# uses

parse_uses = nullable_int_parser_factory('uses')
put_uses = nullable_field_optional_putter_factory('uses')
validate_uses = int_conditional_validator_factory(
    'uses',
    None,
    lambda uses : uses >= 0,
    '>= 0',
)
