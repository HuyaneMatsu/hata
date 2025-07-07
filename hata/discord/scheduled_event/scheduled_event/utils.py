__all__ = ()

from .fields import (
    put_description, put_end, put_name, put_privacy_level, put_schedule, put_start,
    put_status, put_target, validate_description, validate_end, validate_name, validate_privacy_level,
    validate_schedule, validate_start, validate_status, validate_target_location, validate_target_stage,
    validate_target_voice
)


SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS = {
    'description': (validate_description, put_description),
    'end': (validate_end, put_end),
    'location': (validate_target_location, put_target),
    'name': (validate_name, put_name),
    'privacy_level': (validate_privacy_level, put_privacy_level),
    'schedule': (validate_schedule, put_schedule),
    'stage': (validate_target_stage, put_target),
    'start': (validate_start, put_start),
    'voice': (validate_target_voice, put_target),
}

SCHEDULED_EVENT_EDIT_FIELD_CONVERTERS = {
    **SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS,
    'status': (validate_status, put_status),
}


def scheduled_event_occasion_overwrite_get(scheduled_event, timestamp):
    """
    Gets the scheduled event occasion overwrite with the given timestamp.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``
        The scheduled event to update.
    
    timestamp : ``DateTime``
        Timestamp to search for.
    
    Return
    ------
    occasion_overwrite : ``None | ScheduledEventOccasionOverwrite``
    """
    occasion_overwrites = scheduled_event.occasion_overwrites
    if occasion_overwrites is None:
        return
    
    for occasion_overwrite in occasion_overwrites:
        if occasion_overwrite.timestamp == timestamp:
            return occasion_overwrite


def scheduled_event_occasion_overwrite_add(scheduled_event, occasion_overwrite):
    """
    Adds the given timestamp to ``ScheduledEvent.occasion_overwrites``.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``
        The scheduled event to update.
    
    occasion_overwrite : ``ScheduledEventOccasionOverwrite``
        Occasion overwrite to add.
    """
    occasion_overwrites = scheduled_event.occasion_overwrites
    if occasion_overwrites is None:
        scheduled_event.occasion_overwrites = (occasion_overwrite, )
        return
    
    timestamp = occasion_overwrite.timestamp
    new_occasion_overwrites = []
    
    iterator = iter(occasion_overwrites)
    while True:
        try:
            added_occasion_overwrite = next(iterator)
        except StopIteration:
            new_occasion_overwrites.append(occasion_overwrite)
            break
        
        if added_occasion_overwrite.timestamp < timestamp:
            new_occasion_overwrites.append(added_occasion_overwrite)
            continue
        
        new_occasion_overwrites.append(occasion_overwrite)
        new_occasion_overwrites.append(added_occasion_overwrite)
        new_occasion_overwrites.extend(iterator)
        break
    
    scheduled_event.occasion_overwrites = tuple(new_occasion_overwrites)
    return


def scheduled_event_occasion_overwrite_remove(scheduled_event, timestamp):
    """
    Removes the given timestamp to ``ScheduledEvent.occasion_overwrites``.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``
        The scheduled event to update.
    
    timestamp : ``DateTime``
        Timestamp to search for.
    
    Return
    ------
    occasion_overwrite : ``None | ScheduledEventOccasionOverwrite``
    """
    occasion_overwrites = scheduled_event.occasion_overwrites
    if occasion_overwrites is None:
        return None
    
    # Do nothing if already missing.
    for occasion_overwrite in occasion_overwrites:
        if timestamp == occasion_overwrite.timestamp:
            break
    else:
        return None
    
    if len(occasion_overwrites) == 1:
        occasion_overwrites = None
    else:
        occasion_overwrites = (*(
            added_occasion_overwrite for added_occasion_overwrite in occasion_overwrites
            if added_occasion_overwrite.timestamp != timestamp
        ),)
    
    scheduled_event.occasion_overwrites = occasion_overwrites
    return occasion_overwrite
