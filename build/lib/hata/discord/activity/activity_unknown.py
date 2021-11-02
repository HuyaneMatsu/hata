__all__ = ('ACTIVITY_UNKNOWN', 'ActivityUnknown')

from .activity_base import ActivityBase

class ActivityUnknown(ActivityBase):
    """
    Represents if a user has no activity set. This activity type is not a valid Discord activity.
    
    ``activity_unknown`` is a singleton with type value of `127`.
    
    Class Attributes
    ----------------
    created_at : `datetime`
        When the activity was created. Defaults to Discord epoch.
    color : ``Color`` = `Color(0)
        The color of the activity.
    name : `str` = `'Unknown'`
        The activity's name. Subclasses might overwrite it as member descriptor.
    id : `int` = `0`
        The activity's id. Subclasses might overwrite it as member descriptor.
    type : `int` = `127`
        The activity's type value.
    """
    __slots__ = ()
    
    def __repr__(self):
        """Returns the activity's representation."""
        return f'<{self.__class__.__name__}>'

ACTIVITY_UNKNOWN = object.__new__(ActivityUnknown)
