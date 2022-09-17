__all__ = ()

from .location import ScheduledEventEntityMetadataLocation
from .stage import ScheduledEventEntityMetadataStage


def try_get_scheduled_event_metadata_type_from_data(data):
    """
    Tries to detect what type of scheduled metadata the given data is.
    
    Parameters
    ----------
    data : `dict` of (`str`, `str`) items
        Scheduled event metadata data.
    
    Returns
    -------
    metadata_type : `None`, `type`
    """
    if 'location' in data:
        metadata_type = ScheduledEventEntityMetadataLocation
    elif 'speaker_ids' in data:
        metadata_type = ScheduledEventEntityMetadataStage
    else:
        metadata_type = None
    
    return metadata_type
