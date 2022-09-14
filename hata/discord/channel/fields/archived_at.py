__all__ = ()

from datetime import datetime as DateTime

from ...utils import datetime_to_timestamp, timestamp_to_datetime


def parse_archived_at(data):
    """
    Parses out the `archived_at` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    archived_at : `int`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        archived_at = None
    else:
        archived_at_timestamp = sub_data.get('archive_timestamp', None)
        if (archived_at_timestamp is None):
            archived_at = None
        else:
            archived_at = timestamp_to_datetime(archived_at_timestamp)
    
    return archived_at


def validate_archived_at(archived_at):
    """
    Validates the given `archived_at` field.
    
    Parameters
    ----------
    archived_at : `None`, `datetime`
        When the channel was archived.
    
    Returns
    -------
    archived_at : `None`, `datetime`
    
    Raises
    ------
    TypeError
        - If `archived_at` is not `None`, `datetime`.
    """
    if (archived_at is not None) and (not isinstance(archived_at, DateTime)):
        raise TypeError(
            f'`archived_at` can be `None`, `datetime`, got {archived_at.__class__.__name__}; {archived_at!r}.'
        )
    
    return archived_at


def put_archived_at_into(archived_at, data, defaults):
    """
    Puts the `archived_at`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    archived_at : `None`, `datetime`
        When the channel was archived.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (archived_at is not None):
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        if archived_at is None:
            archived_at_timestamp = None
        else:
            archived_at_timestamp = datetime_to_timestamp(archived_at)
            
        sub_data['archive_timestamp'] = archived_at_timestamp
    
    return data
