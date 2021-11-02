__all__ = ('create_activity_from_data', )

from . import activity_types as ACTIVITY_TYPES
from .activity_unknown import ACTIVITY_UNKNOWN
from .activity_custom import ActivityCustom
from . activity_rich import ActivityRich

def create_activity_from_data(activity_data):
    """
    A factory function to create activity from the json data sent by Discord.
    
    If the data is `None` returns ``ActivityUnknown``.
    
    Parameters
    ----------
    activity_data : `dict` of (`str`, `Any`) items
        Activity data received from Discord.
    
    Returns
    -------
    activity : ``ActivityBase`` instance
    """
    if activity_data is None:
        return ACTIVITY_UNKNOWN
    
    if activity_data['type'] == ACTIVITY_TYPES.custom:
        activity_type = ActivityCustom
    else:
        activity_type = ActivityRich
    
    return activity_type.from_data(activity_data)
