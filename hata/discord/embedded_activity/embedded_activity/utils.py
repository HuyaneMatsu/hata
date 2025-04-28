__all__ = ()

from .constants import (
    EMBEDDED_ACTIVITY_UPDATE_CREATE, EMBEDDED_ACTIVITY_UPDATE_DELETE, EMBEDDED_ACTIVITY_UPDATE_USER_ADD,
    EMBEDDED_ACTIVITY_UPDATE_USER_DELETE
)
from .embedded_activity import EmbeddedActivity


def difference_handle_embedded_activity_update_event(data):
    """
    Handles embedded activity events returning the embedded activity and the changes with it.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Embedded activity update event.
    
    Returns
    -------
    embedded_activity : ``EmbeddedActivity``
        The updated embedded activity.
    
    changes : `list` of `tuple` (`int`, `object`)
        Change entries. Each tuple` has `2` elements:
        
        - The action identifier of the change:
        
            Can be one of the following:
            
            +---------------------------------------+-------+-----------+
            | Respective name                       | Value | Notes     |
            +=======================================+=======+===========+
            | EMBEDDED_ACTIVITY_UPDATE_NONE         | 0     |           |
            +---------------------------------------+-------+-----------+
            | EMBEDDED_ACTIVITY_UPDATE_CREATE       | 1     |           |
            +---------------------------------------+-------+-----------+
            | EMBEDDED_ACTIVITY_UPDATE_DELETE       | 2     |           |
            +---------------------------------------+-------+-----------+
            | EMBEDDED_ACTIVITY_UPDATE_UPDATE       | 3     | Not used. |
            +---------------------------------------+-------+-----------+
            | EMBEDDED_ACTIVITY_UPDATE_USER_ADD     | 4     |           |
            +---------------------------------------+-------+-----------+
            | EMBEDDED_ACTIVITY_UPDATE_USER_DELETE  | 5     |           |
            +---------------------------------------+-------+-----------+
        
        - The value in the context of the action.
            
            If `action` is `EMBEDDED_ACTIVITY_UPDATE_USER_ADD`, `EMBEDDED_ACTIVITY_UPDATE_USER_DELETE`, it will
            contain the joined or left users.
    """
    embedded_activity, created = EmbeddedActivity.from_data_is_created(data)
    
    changes = []
    
    # If the object was just created, we have 2 cases:
    # Just came to cache as a deleted activity / it was created
    if created:
        if embedded_activity.user_states:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_CREATE, None))
        else:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_DELETE, None))
    
    else:
        joined_users, left_users = embedded_activity._difference_update_user_states(data)
        for user in joined_users:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_USER_ADD, user))
        
        for user in left_users:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_USER_DELETE, user))
        
        if not embedded_activity.user_states:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_DELETE, None))
    
    return embedded_activity, changes


def handle_embedded_activity_update_event(data):
    """
    Handles an embedded activity event.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Embedded activity update event.
    """
    embedded_activity, created = EmbeddedActivity.from_data_is_created(data)
    if not created:
        embedded_activity._update_user_states(data)
