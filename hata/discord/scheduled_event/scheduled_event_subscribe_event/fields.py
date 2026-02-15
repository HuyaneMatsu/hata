__all__ = ()

from ..scheduled_event import ScheduledEvent

from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_putter_factory
from ...field_validators import entity_id_validator_factory, nullable_date_time_validator_factory
from ...user import ClientUserBase
from ...utils import datetime_to_id, id_to_datetime


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')


# timestamp

def parse_timestamp(data):
    """
    Parses cancellation timestamp.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    timestamp : `DateTime`
    """
    timestamp_as_id = data.get('guild_scheduled_event_exception_id', None)
    if timestamp_as_id is None:
        return None
    
    return id_to_datetime(int(timestamp_as_id))


def put_timestamp(timestamp, data, defaults):
    """
    Serialises the timestamp into the given data.
    
    Parameters
    ----------
    timestamp : `DateTime`
        The timestamp to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (timestamp is not None):
        data['guild_scheduled_event_exception_id'] = None if (timestamp is None) else str(datetime_to_id(timestamp))
    
    return data


validate_timestamp = nullable_date_time_validator_factory('timestamp')


# scheduled_event_id

parse_scheduled_event_id = entity_id_parser_factory('guild_scheduled_event_id')
put_scheduled_event_id = entity_id_putter_factory('guild_scheduled_event_id')
validate_scheduled_event_id = entity_id_validator_factory('scheduled_event_id', ScheduledEvent)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
