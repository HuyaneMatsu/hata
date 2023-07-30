__all__ = ()

from ...channel import Channel, create_partial_channel_data, create_partial_channel_from_data
from ...field_parsers import int_parser_factory, force_string_parser_factory, nullable_date_time_parser_factory
from ...field_putters import int_putter_factory, nullable_functional_putter_factory, force_string_putter_factory, \
    nullable_date_time_optional_putter_factory
from ...field_validators import int_conditional_validator_factory, nullable_entity_validator_factory, \
    force_string_validator_factory, nullable_date_time_validator_factory
from ...guild import create_partial_guild_from_data, create_partial_guild_data, create_partial_guild_from_id

# approximate_online_count

parse_approximate_online_count = int_parser_factory('approximate_presence_count', 0)
put_approximate_online_count_into = int_putter_factory('approximate_presence_count')
validate_approximate_online_count = int_conditional_validator_factory(
    'approximate_online_count',
    0,
    lambda approximate_online_count : approximate_online_count >= 0,
    '>= 0',
)

# approximate_user_count

parse_approximate_user_count = int_parser_factory('approximate_member_count', 0)
put_approximate_user_count_into = int_putter_factory('approximate_member_count')
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
    channel : `None`, ``Channel``
    """
    channel_data = data.get('channel', None)
    if (channel_data is not None):
        return create_partial_channel_from_data(channel_data, guild_id)
    
    # Do we get channel_id key?
    """
    channel_id = data.get('channel_id', None)
    if (channel_id is not None):
        return create_partial_channel_from_id(int(channel_id), ChannelType.unknown, guild_id)
    """
    return None

put_channel_into = nullable_functional_putter_factory('channel', create_partial_channel_data)
validate_channel = nullable_entity_validator_factory('channel', Channel)

# code

parse_code = force_string_parser_factory('code')
put_code_into = force_string_putter_factory('code')
validate_code = force_string_validator_factory('code', 0, 1024)

# created_at

parse_created_at = nullable_date_time_parser_factory('created_at')
put_created_at_into = nullable_date_time_optional_putter_factory('created_at')
validate_created_at = nullable_date_time_validator_factory('created_at')

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
    guild : `None`, ``Guild``
    """
    guild_data = data.get('guild', None)
    if (guild_data is not None):
        return create_partial_guild_from_data(guild_data)
    
    guild_id = data.get('guild_id', None)
    if (guild_id is not None):
        return create_partial_guild_from_id(int(guild_id))
    
    return None

put_guild_into = nullable_functional_putter_factory('guild', create_partial_guild_data)
validate_guild = nullable_entity_validator_factory('guild', Channel)
