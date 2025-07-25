__all__ = ()

from datetime import datetime as DateTime

from ...channel import Channel
from ...field_parsers import (
    default_entity_parser_factory, entity_id_array_parser_factory, entity_id_parser_factory,
    force_string_parser_factory, int_parser_factory, nullable_date_time_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory, nullable_entity_parser_factory
)
from ...field_putters import (
    default_entity_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    force_string_putter_factory, int_putter_factory,  nullable_date_time_optional_putter_factory,
    optional_entity_id_array_optional_putter_factory, nullable_string_optional_putter_factory,
    preinstanced_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    default_entity_validator_factory, entity_id_array_validator_factory, entity_id_validator_factory,
    force_string_validator_factory, int_conditional_validator_factory, nullable_date_time_validator_factory,
    nullable_string_validator_factory, preinstanced_validator_factory, nullable_entity_validator_factory,
    nullable_object_array_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER
from ...utils import datetime_to_id, id_to_datetime

from ..schedule import Schedule
from ..scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite
from ..scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation

from .constants import DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN, NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .preinstanced import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus


# occasion_overwrites


def parse_occasion_overwrites(data):
    """
    Parses occasion_overwrites out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    occasion_overwrites : `None | tuple<DateTime>`
    """
    occasion_overwrite_datas = data.get('guild_scheduled_event_exceptions', None)
    if (occasion_overwrite_datas is not None) and occasion_overwrite_datas:
        return tuple(sorted(
            ScheduledEventOccasionOverwrite.from_data(occasion_overwrite_data) for occasion_overwrite_data in occasion_overwrite_datas
        ))


def put_occasion_overwrites(occasion_overwrites, data, defaults, *, scheduled_event_id = 0):
    """
    Serialises the occasion_overwrites into the given data.
    
    Parameters
    ----------
    occasion_overwrites : `None | tuple<DateTime>`
        The cancelled occurrences.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    scheduled_event_id : `int` = `0`, Optional (Keyword only)
        The owner scheduled event's identifier.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (occasion_overwrites is not None):
        occasion_overwrite_datas = []
        
        if (occasion_overwrites is not None):
            if scheduled_event_id:
                scheduled_event_id_serialized = str(scheduled_event_id)
            else:
                scheduled_event_id_serialized = None
            
            for occasion_overwrite in occasion_overwrites:
                occasion_overwrite_data = occasion_overwrite.to_data(defaults = defaults, include_internals = True)
                occasion_overwrite_data['event_id'] = scheduled_event_id_serialized
                
                occasion_overwrite_datas.append(occasion_overwrite_data)
        
        data['guild_scheduled_event_exceptions'] = occasion_overwrite_datas
    
    return data


validate_occasion_overwrites = nullable_object_array_validator_factory(
    'occasion_overwrites', ScheduledEventOccasionOverwrite, ordered = True
)


# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id = entity_id_optional_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)


# creator

parse_creator = default_entity_parser_factory('creator', User, default = ZEROUSER)
put_creator = default_entity_putter_factory('creator', ClientUserBase, ZEROUSER, force_include_internals = True)
validate_creator = default_entity_validator_factory('creator', ClientUserBase, default = ZEROUSER)


# description

parse_description = nullable_string_parser_factory('description')
put_description = nullable_string_optional_putter_factory('description')
validate_description = nullable_string_validator_factory('description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX)


# end

parse_end = nullable_date_time_parser_factory('scheduled_end_time')
put_end = nullable_date_time_optional_putter_factory('scheduled_end_time')
validate_end = nullable_date_time_validator_factory('end')


# entity_id

parse_entity_id = entity_id_parser_factory('entity_id')
put_entity_id = entity_id_optional_putter_factory('entity_id')
validate_entity_id = entity_id_validator_factory('entity_id')


# entity_metadata

def parse_entity_metadata(data, entity_type):
    """
    Parsers out a scheduled event entity's metadata form the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Scheduled event data.
    
    entity_type : ``ScheduledEventEntityType``
        The scheduled event entity's type.
    
    Returns
    -------
    entity_metadata : ``ScheduledEventEntityMetadataBase``
    """
    entity_metadata_type = entity_type.metadata_type
    entity_metadata_data = data.get('entity_metadata', None)
    
    if entity_metadata_data is None:
        entity_metadata = entity_metadata_type._create_empty()
    else:
        entity_metadata = entity_metadata_type.from_data(entity_metadata_data)
    
    return entity_metadata


def put_entity_metadata(entity_metadata, data, defaults):
    """
    Puts the given scheduled event entity's metadata into the given `data` json serializable object.
    
    Parameters
    ----------
    entity_metadata : ``ScheduledEventEntityMetadataBase``
        Scheduled event entity metadata.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (type(entity_metadata) is not ScheduledEventEntityMetadataBase):
        data['entity_metadata'] = entity_metadata.to_data(defaults = defaults)
    
    return data


# entity_type

parse_entity_type = preinstanced_parser_factory('entity_type', ScheduledEventEntityType, ScheduledEventEntityType.none)
put_entity_type = preinstanced_putter_factory('entity_type')
validate_entity_type = preinstanced_validator_factory('entity_type', ScheduledEventEntityType)


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')


# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('scheduled_event_id')


# name

parse_name = force_string_parser_factory('name')
put_name = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)


# privacy_level

parse_privacy_level = preinstanced_parser_factory('privacy_level', PrivacyLevel, PrivacyLevel.guild_only)
put_privacy_level = preinstanced_putter_factory('privacy_level')
validate_privacy_level = preinstanced_validator_factory('privacy_level', PrivacyLevel)


# schedule

parse_schedule = nullable_entity_parser_factory('recurrence_rule', Schedule)


def put_schedule(schedule, data, defaults, *, start = None):
    """
    Serialises the given schedule.
    
    Parameters
    ----------
    schedule : ``None | Schedule``
        The schedule to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    start : `None | DateTime` = `None`, Optional (Keyword only)
        Start date to use if schedule does not define it.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (schedule is not None):
        if schedule is None:
            schedule_data = None
        else:
            schedule_data = schedule.to_data(defaults = defaults, start = start)
        
        data['recurrence_rule'] = schedule_data
    
    return data    


validate_schedule = nullable_entity_validator_factory('schedule', Schedule)


# start

parse_start = nullable_date_time_parser_factory('scheduled_start_time')
put_start = nullable_date_time_optional_putter_factory('scheduled_start_time')
validate_start = nullable_date_time_validator_factory('start')


# sku_ids

parse_sku_ids = entity_id_array_parser_factory('sku_ids')
put_sku_ids = optional_entity_id_array_optional_putter_factory('sku_ids')
validate_sku_ids = entity_id_array_validator_factory('sku_ids', NotImplemented, include = 'SKU')


# status

parse_status = preinstanced_parser_factory('status', ScheduledEventStatus, ScheduledEventStatus.none)
put_status = preinstanced_optional_putter_factory('status', ScheduledEventStatus.none)
validate_status = preinstanced_validator_factory('status', ScheduledEventStatus)


# user_count

parse_user_count = int_parser_factory('user_count', 0)
put_user_count = int_putter_factory('user_count')
validate_user_count = int_conditional_validator_factory(
    'user_count',
    0,
    (lambda user_count : user_count >= 0),
    '>= 0',
)


# Target parsers

ENTITY_METADATA_DEFAULT = ScheduledEventEntityMetadataBase._create_empty()


# location

def validate_target_location(location):
    """
    Validates scheduled event target (location).
    
    Parameters
    ----------
    location : `None`, `str`
        The place where the event will take place.
    
    Returns
    -------
    entity_type : ``ScheduledEventEntityType``
        Scheduled event entity type.
    entity_metadata : ``ScheduledEventEntityMetadataBase``
        Scheduled event entity metadata.
    channel_id : `int`
        Scheduled event target channel identifier.
    
    Raises
    ------
    TypeError
        - If `location`'s type is incorrect.
    ValueError
        - If `location`'s value is incorrect.
    """
    entity_metadata = ScheduledEventEntityMetadataLocation(location = location)
    return ScheduledEventEntityType.location, entity_metadata, 0


# voice

def validate_target_voice(voice):
    """
    Validates scheduled event target (voice channel).
    
    Parameters
    ----------
    voice : ``Channel``
        The voice channel where the event will take place.
    
    Returns
    -------
    entity_type : ``ScheduledEventEntityType``
        Scheduled event entity type.
    entity_metadata : ``ScheduledEventEntityMetadataBase``
        Scheduled event entity metadata.
    channel_id : `int`
        Scheduled event target channel identifier.
    
    Raises
    ------
    TypeError
        - If `voice`'s type is incorrect.
    ValueError
        - If `voice`'s value is incorrect.
    """
    channel_id = validate_channel_id(voice)
    return ScheduledEventEntityType.voice, ENTITY_METADATA_DEFAULT, channel_id


# stage

def validate_target_stage(stage):
    """
    Validates scheduled event target (stage channel).
    
    Parameters
    ----------
    stage : ``Channel``
        The stage channel where the event will take place.
    
    Returns
    -------
    entity_type : ``ScheduledEventEntityType``
        Scheduled event entity type.
    entity_metadata : ``ScheduledEventEntityMetadataBase``
        Scheduled event entity metadata.
    channel_id : `int`
        Scheduled event target channel identifier.
    
    Raises
    ------
    TypeError
        - If `stage`'s type is incorrect.
    ValueError
        - If `stage`'s value is incorrect.
    """
    channel_id = validate_channel_id(stage)
    return ScheduledEventEntityType.stage, ENTITY_METADATA_DEFAULT, channel_id


# target

def put_target(target, data, defaults):
    """
    Puts the given scheduled event target into the given `data` json serializable object.
    
    Used when creating  or editing a scheduled events.
    
    Parameters
    ----------
    target : `tuple` (``ScheduledEventEntityType``, ``ScheduledEventEntityMetadataBase``, `int`)
        Scheduled event target.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    entity_type, entity_metadata, channel_id = target
    put_entity_type(entity_type, data, defaults)
    put_entity_metadata(entity_metadata, data, defaults)
    put_channel_id(channel_id, data, defaults)
    return data
