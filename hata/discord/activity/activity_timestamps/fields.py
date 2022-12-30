__all__ = ()

from ...field_validators import nullable_date_time_validator_factory
from ...utils import datetime_to_millisecond_unix_time, millisecond_unix_time_to_datetime

# end

def parse_end(data):
    """
    Parses activity timestamp end time from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Activity timestamp data.
    
    Returns
    -------
    end : `None`, `datetime`
    """
    end = data.get('end', None)
    if (end is not None):
        return millisecond_unix_time_to_datetime(end)


def put_end_into(end, data, defaults):
    """
    Puts the activity timestamps end into the given data.
    
    Parameters
    ----------
    end : `None`, `datetime`
        Activity timestamps end.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (end is not None):
        if (end is not None):
            end = datetime_to_millisecond_unix_time(end)
        
        data['end'] = end
    
    return data


validate_end = nullable_date_time_validator_factory('end')

# start

def parse_start(data):
    """
    Parses activity timestamp time from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Activity timestamp data.
    
    Returns
    -------
    start : `None`, `datetime`
    """
    start = data.get('start', None)
    if (start is not None):
        return millisecond_unix_time_to_datetime(start)


def put_start_into(start, data, defaults):
    """
    Puts the activity timestamps start into the given data.
    
    Parameters
    ----------
    start : `None`, `datetime`
        Activity timestamps start.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (start is not None):
        if (start is not None):
            start = datetime_to_millisecond_unix_time(start)
        
        data['start'] = start
    
    return data


validate_start = nullable_date_time_validator_factory('start')
