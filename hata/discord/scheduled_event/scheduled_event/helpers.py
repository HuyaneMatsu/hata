__all__ = ()

from .preinstanced import ScheduledEventEntityType


def guess_scheduled_event_entity_type_from_keyword_parameters(keyword_parameters):
    """
    Guesses scheduled event entity type from the given keyword parameters.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Scheduled event metadata data.
    
    Returns
    -------
    metadata_type : `type<ScheduledEventEntityMetadataBase>`
    """
    if 'location' in keyword_parameters:
        metadata_type = ScheduledEventEntityType.location
    elif 'speaker_ids' in keyword_parameters:
        metadata_type = ScheduledEventEntityType.stage
    else:
        metadata_type = ScheduledEventEntityType.none
    
    return metadata_type
