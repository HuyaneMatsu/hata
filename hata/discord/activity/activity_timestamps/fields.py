__all__ = ()

from ...field_validators import nullable_date_time_validator_factory
from ...utils import datetime_to_millisecond_unix_time, millisecond_unix_time_to_datetime

# end

def parse_end(data):
    """
    Parses activity timestamp end time from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Activity timestamp data.
    
    Returns
    -------
    end : `None | DateTime`
    """
    end = data.get('end', None)
    if (end is not None):
        return millisecond_unix_time_to_datetime(end)


def put_end(end, data, defaults):
    """
    Puts the activity timestamps end into the given data.
    
    Parameters
    ----------
    end : `None | DateTime`
        Activity timestamps end.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
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
    data : `dict<str, object>`
        Activity timestamp data.
    
    Returns
    -------
    start : `None | DateTime`
    """
    start = data.get('start', None)
    if (start is not None):
        return millisecond_unix_time_to_datetime(start)


def put_start(start, data, defaults):
    """
    Puts the activity timestamps start into the given data.
    
    Parameters
    ----------
    start : `None | DateTime`
        Activity timestamps start.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (start is not None):
        if (start is not None):
            start = datetime_to_millisecond_unix_time(start)
        
        data['start'] = start
    
    return data


validate_start = nullable_date_time_validator_factory('start')
