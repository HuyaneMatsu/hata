__all__ = ()

from .constants import (
    EMBEDDED_ACTIVITY_UPDATE_CREATE, EMBEDDED_ACTIVITY_UPDATE_DELETE, EMBEDDED_ACTIVITY_UPDATE_UPDATE,
    EMBEDDED_ACTIVITY_UPDATE_USER_ADD, EMBEDDED_ACTIVITY_UPDATE_USER_DELETE
)
from .embedded_activity_state import EmbeddedActivityState


def difference_handle_embedded_activity_update_event(data):
    """
    Handles embedded activity events returning the embedded activity state and the changes with it.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Embedded activity update event.
    
    Returns
    -------
    embedded_activity_state : ``EmbeddedActivityState``
        The updated embedded activity state.
    
    changes : `list` of `tuple` (`int`, `object`)
        Change entries. Each tuple` has `2` elements:
        
        - The action identifier of the change:
        
            Can be one of the following:
            
            +---------------------------------------+-------+
            | Respective name                       | Value |
            +=======================================+=======+
            | EMBEDDED_ACTIVITY_UPDATE_NONE         | 0     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_CREATE       | 1     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_DELETE       | 2     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_UPDATE       | 3     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_USER_ADD     | 4     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_USER_DELETE  | 5     |
            +---------------------------------------+-------+
        
        - The value in the context of the action.
            
            If `action` is `EMBEDDED_ACTIVITY_UPDATE_UPDATE`, this value will contain the updated attributes of the
            activity.
            
            +-------------------+-----------------------------------+
            | Keys              | Values                            |
            +===================+===================================+
            | assets            | `None`, ``ActivityAssets``        |
            +-------------------+-----------------------------------+
            | created_at        | `datetime`                        |
            +-------------------+-----------------------------------+
            | details           | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | flags             | ``ActivityFlag``                  |
            +-------------------+-----------------------------------+
            | name              | `str`                             |
            +-------------------+-----------------------------------+
            | metadata          | ``ActivityMetadataBase``          |
            +-------------------+-----------------------------------+
            | party             | `None`, ``ActivityParty``         |
            +-------------------+-----------------------------------+
            | secrets           | `None`, ``ActivitySecrets``       |
            +-------------------+-----------------------------------+
            | session_id        | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | state             | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | sync_id           | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | timestamps        | `None`, `ActivityTimestamps``     |
            +-------------------+-----------------------------------+
            | url               | `None`, `str`                     |
            +-------------------+-----------------------------------+
            
            If `action` is `EMBEDDED_ACTIVITY_UPDATE_USER_ADD`, `EMBEDDED_ACTIVITY_UPDATE_USER_DELETE`, it will
            contain the joined or left user's identifier.
    """
    embedded_activity_state, is_created = EmbeddedActivityState.from_data_is_created(data)
    
    changes = []
    
    # If the object was just created, we have 2 cases:
    # Just came to cache as a deleted activity / it was created
    if is_created:
        if embedded_activity_state.user_ids:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_CREATE, None))
        else:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_DELETE, None))
    
    else:
        joined_user_ids, left_user_ids = embedded_activity_state._difference_update_user_ids(data)
        for user_id in joined_user_ids:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_USER_ADD, user_id))
        
        for user_id in left_user_ids:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_USER_DELETE, user_id))
        
        if embedded_activity_state.user_ids:
            activity_old_attributes = embedded_activity_state._difference_update_activity(data)
            if activity_old_attributes:
                changes.append((EMBEDDED_ACTIVITY_UPDATE_UPDATE, activity_old_attributes))
        else:
            embedded_activity_state._update_activity(data)
            changes.append((EMBEDDED_ACTIVITY_UPDATE_DELETE, None))
    
    return embedded_activity_state, changes


def handle_embedded_activity_update_event(data):
    """
    Handles an embedded activity event.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Embedded activity update event.
    """
    embedded_activity_state, is_created = EmbeddedActivityState.from_data_is_created(data)
    if not is_created:
        embedded_activity_state._update_user_ids(data)
        embedded_activity_state._update_activity(data)
