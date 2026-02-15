__all__ = ()

from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_optional_putter_factory
from ...field_validators import (
    default_entity_validator_factory, entity_id_validator_factory, nullable_date_time_validator_factory
)
from ...utils import datetime_to_id, id_to_datetime
from ...user import ClientUserBase, User, ZEROUSER

from ..scheduled_event import ScheduledEvent


# scheduled_event_id

parse_scheduled_event_id = entity_id_parser_factory('guild_scheduled_event_id')
put_scheduled_event_id = entity_id_optional_putter_factory('guild_scheduled_event_id')
validate_scheduled_event_id = entity_id_validator_factory('scheduled_event_id', ScheduledEvent)


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


# user

def parse_user(data, guild_id = 0):
    """
    Parses aa user out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    guild_id : `int` = `0`, Optional
        The respective guild's identifier.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    user_data = data.get('user', None)
    if user_data is None:
        return ZEROUSER
    
    return User.from_data(user_data, user_data.get('member', None), guild_id)


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
    user_data = user.to_data(defaults = defaults, include_internals = True)
    
    try:
        guild_profile = user.guild_profiles[guild_id]
    except KeyError:
        pass
    else:
        user_data['member'] = guild_profile.to_data(defaults = defaults, include_internals = True)
    
    data['user'] = user_data
    
    return data


validate_user = default_entity_validator_factory('user', ClientUserBase, default = ZEROUSER)
