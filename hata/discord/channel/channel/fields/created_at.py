__all__ = ()

from ....field_validators import nullable_date_time_validator_factory
from ....utils import datetime_to_timestamp, timestamp_to_datetime


def parse_created_at(data):
    """
    Parses out the `created_at` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    created_at : `int`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        created_at = None
    else:
        created_at_timestamp = sub_data.get('create_timestamp', None)
        if (created_at_timestamp is None):
            created_at = None
        else:
            created_at = timestamp_to_datetime(created_at_timestamp)
    
    return created_at


def put_created_at_into(created_at, data, defaults):
    """
    Puts the `created_at`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    created_at : `None`, `datetime`
        When the channel was created.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (created_at is not None):
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        if created_at is None:
            created_at_timestamp = None
        else:
            created_at_timestamp = datetime_to_timestamp(created_at)
            
        sub_data['create_timestamp'] = created_at_timestamp
    
    return data


validate_created_at = nullable_date_time_validator_factory('created_at')
