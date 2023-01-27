__all__ = ('ActivityUpdate',)

from itertools import count

from scarletio import RichAttributeErrorBaseType

from ...activity import Activity

from .fields import validate_activity, validate_old_attributes


class ActivityUpdate(RichAttributeErrorBaseType):
    """
    Represents an updated activity with storing the activity and it's old updated attributes in a `dict`.
    
    Attributes
    ----------
    activity : ``Activity``
        The updated activity.
    old_attributes : `dict` of (`str`, `object`) items
        The changed attributes of the activity in `attribute-name` - `old-value` relation. Can contain any of the
        following items:
        
        +-------------------+-----------------------------------+
        | Keys              | Values                            |
        +===================+===================================+
        | assets            | `None`, ``ActivityAssets``        |
        +-------------------+-----------------------------------+
        | created_at        | `datetime`                        |
        +-------------------+-----------------------------------+
        | details           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | emoji             | `None`, ``Emoji``                 |
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
    """
    __slots__ = ('activity', 'old_attributes',)
    
    def __new__(cls, activity = ..., old_attributes = ...):
        """
        Creates a new activity change instance with the given fields.
        
        Parameters
        ----------
        activity : ``Activity``, Optional (Keyword only)
            The updated activity.
        old_attributes : `None`, `dict` of (`str`, `object`) items, Optional (Keyword only)
            The changed attributes of the activity.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
        """
        # activity
        if activity is ...:
            activity = Activity()
        else:
            activity = validate_activity(activity)
        
        # old_attributes
        if old_attributes is ...:
            old_attributes = {}
        else:
            old_attributes = validate_old_attributes(old_attributes)
        
        # Construct
        self = object.__new__(cls)
        self.activity = activity
        self.old_attributes = old_attributes
        return self
    
    
    @classmethod
    def from_fields(cls, activity, old_attributes):
        """
        Creates a new activity change instance with the given fields.
        
        Parameters
        ----------
        activity : ``Activity``
            The updated activity.
        old_attributes : `dict` of (`str`, `object`) items
            The changed attributes of the activity.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.activity = activity
        self.old_attributes = old_attributes
        return self
    
    
    def __repr__(self):
        """Returns the representation of the activity update."""
        return f'<{self.__class__.__name__} changes: {len(self.old_attributes)!r}, activity = {self.activity!r}>'
    
    
    def __hash__(self):
        """Returns the activity update's hash value."""
        hash_value = 0
        
        # activity
        hash_value ^= hash(self.activity)
        
        # old_attributes
        old_attributes = self.old_attributes
        hash_value ^= len(old_attributes)
        
        for mask, key in zip(count(5, 7), sorted(old_attributes.keys())):
            hash_value ^= (mask | hash(key)) & hash(old_attributes[key])
        
        return hash_value
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.activity != other.activity:
            return False
        
        if self.old_attributes != other.old_attributes:
            return False
        
        return True
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    
    def __iter__(self):
        """
        Unpacks the activity update.
        
        This method is a generator.
        """
        yield self.activity
        yield self.old_attributes
    
    
    def copy(self):
        """
        Copies the activity update.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.activity = self.activity.copy()
        new.old_attributes = self.old_attributes.copy()
        return new
    
    
    def copy_with(self, *, activity = ..., old_attributes = ...):
        """
        Copies the activity change with the given fields.
        
        Parameters
        ----------
        activity : ``Activity``, Optional (Keyword only)
            The updated activity.
        old_attributes : `None`, `dict` of (`str`, `object`) items, Optional (Keyword only)
            The changed attributes of the activity.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
        """
        # activity
        if activity is ...:
            activity = self.activity.copy()
        else:
            activity = validate_activity(activity)
        
        # old_attributes
        if old_attributes is ...:
            old_attributes = self.old_attributes.copy()
        else:
            old_attributes = validate_old_attributes(old_attributes)
        
        # Construct
        new = object.__new__(type(self))
        new.activity = activity
        new.old_attributes = old_attributes
        return new
