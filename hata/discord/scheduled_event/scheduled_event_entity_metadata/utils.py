__all__ = ()

from .base import ScheduledEventEntityMetadataBase
from .location import ScheduledEventEntityMetadataLocation
from .stage import ScheduledEventEntityMetadataStage


def try_get_scheduled_event_metadata_type_from_data(data):
    """
    Tries to detect what type of scheduled metadata the given data is.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Scheduled event metadata data.
    
    Returns
    -------
    metadata_type : `type<ScheduledEventEntityMetadataBase>`
    """
    if 'location' in data:
        metadata_type = ScheduledEventEntityMetadataLocation
    elif 'speaker_ids' in data:
        metadata_type = ScheduledEventEntityMetadataStage
    else:
        metadata_type = ScheduledEventEntityMetadataBase
    
    return metadata_type
