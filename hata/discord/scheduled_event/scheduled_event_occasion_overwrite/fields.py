__all__ = ()

from ...field_parsers import bool_parser_factory, nullable_date_time_parser_factory
from ...field_putters import force_bool_putter_factory, nullable_date_time_optional_putter_factory
from ...field_validators import (
    bool_validator_factory, force_date_time_validator_factory, nullable_date_time_validator_factory
)
from ...utils import DISCORD_EPOCH_START, datetime_to_id, id_to_datetime


# cancelled

parse_cancelled = bool_parser_factory('is_canceled', False)
put_cancelled = force_bool_putter_factory('is_canceled')
validate_cancelled = bool_validator_factory('cancelled', False)


# end

parse_end = nullable_date_time_parser_factory('scheduled_end_time')
put_end = nullable_date_time_optional_putter_factory('scheduled_end_time')
validate_end = nullable_date_time_validator_factory('end')


# start

parse_start = nullable_date_time_parser_factory('scheduled_start_time')
put_start = nullable_date_time_optional_putter_factory('scheduled_start_time')
validate_start = nullable_date_time_validator_factory('start')


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
    timestamp_as_id = data.get('event_exception_id', None)
    if timestamp_as_id is None:
        return DISCORD_EPOCH_START
    
    return id_to_datetime(int(timestamp_as_id))


def put_timestamp(timestamp, data, defaults):
    """
    Serialises the timestamp into the given data.
    
    Parameters
    ----------
    timestamp : `None | tuple<DateTime>`
        The timestamp to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['event_exception_id'] = datetime_to_id(timestamp)
    return data


validate_timestamp = force_date_time_validator_factory('timestamp')
