__all__ = ('PollChange',)

from scarletio import RichAttributeErrorBaseType

from .fields import validate_added, validate_updated, validate_removed


class PollChange(RichAttributeErrorBaseType):
    """
    Represents a message's changed poll.
    
    Attributes
    ----------
    added : `None`, ``Poll``
        The added poll to the respective message. Defaults to `None`.
    
    removed: `None`, ``Poll``
        The removed poll from the respective message. Defaults to `None`.
    
    updated : `None`, ``PollUpdate``
        The updated poll of the respective message. Defaults to `None`.
    """
    __slots__ = ('added', 'updated', 'removed',)
    
    def __new__(cls, *, added = ..., removed = ..., updated = ...):
        """
        Creates a new poll change with the given parameters.
        
        Parameters
        ----------
        added : `None`, ``Poll``, Optional (Keyword only)
            The added poll to the message.
        
        removed: `None`, ``Poll``, Optional (Keyword only)
            The removed poll from the message.
        
        updated : `None`, ``PollUpdate``, Optional (Keyword only)
            The updated poll of the message.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # added
        if added is ...:
            added = None
        else:
            added = validate_added(added)
        
        # removed
        if removed is ...:
            removed = None
        else:
            removed = validate_removed(removed)
        
        # updated
        if updated is ...:
            updated = None
        else:
            updated = validate_updated(updated)
        
        # Construct
        self = object.__new__(cls)
        self.added = added
        self.removed = removed
        self.updated = updated
        return self
    
    
    @classmethod
    def from_fields(cls, added, updated, removed):
        """
        Creates a new poll change with the given parameters.
        
        Parameters
        ----------
        added : `None`, ``Poll``
            The added poll to the message.
        
        updated : `None`, ``PollUpdate``
            The updated poll of the message.
        
        removed: `None`, ``Poll``
            The removed poll from the message.
        """
        self = object.__new__(cls)
        self.added = added
        self.removed = removed
        self.updated = updated
        return self
    
    
    def __repr__(self):
        """Returns the representation of the poll change."""
        repr_parts = ['<',
            self.__class__.__name__,
        ]
        
        added = self.added
        if added is None:
            field_added = False
        else:
            repr_parts.append(' added = ')
            repr_parts.append(repr(added))
            field_added = True
        
        updated = self.updated
        if (updated is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' updated = ')
            repr_parts.append(repr(updated))
        
        removed = self.removed
        if (removed is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' removed = ')
            repr_parts.append(repr(removed))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the poll change's hash value."""
        hash_value = 0
        
        added = self.added
        if (added is not None):
            hash_value ^= hash(added)
        
        removed = self.removed
        if (removed is not None):
            hash_value ^= hash(removed)
        
        updated = self.updated
        if (updated is not None):
            hash_value ^= hash(updated)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two poll change are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.added != other.added:
            return False
        
        if self.removed != other.removed:
            return False
        
        if self.updated != other.updated:
            return False
        
        return True
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    
    def __iter__(self):
        """
        Unpacks the poll change.
        
        This method is a generator.
        """
        yield self.added
        yield self.updated
        yield self.removed
    
    
    def copy(self):
        """
        Copies the poll change.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        added = self.added
        if (added is not None):
            added = added.copy()
        
        removed = self.removed
        if (removed is not None):
            removed = removed.copy()
        
        updated = self.updated
        if (updated is not None):
            updated = updated.copy()
        
        new = object.__new__(type(self))
        new.added = added
        new.updated = updated
        new.removed = removed
        return new
    
    
    def copy_with(self, *, added = ..., removed = ..., updated = ...):
        """
        Copies the poll change with the given fields.
        
        Parameters
        ----------
        added : `None`, ``Poll``, Optional (Keyword only)
            The added poll to the message.
        
        removed: `None`, ``Poll``, Optional (Keyword only)
            The removed poll from the message.
        
        updated : `None`, ``PollUpdate``, Optional (Keyword only)
            The updated poll of the message.
        
        Returns
        -------
        new : `instance<type<self>>`
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # added
        if added is ...:
            added = self.added
            if (added is not None):
                added = added.copy()
        else:
            added = validate_added(added)
        
        # removed
        if removed is ...:
            removed = self.removed
            if (removed is not None):
                removed = removed.copy()
        else:
            removed = validate_removed(removed)
        
        # updated
        if updated is ...:
            updated = self.updated
            if (updated is not None):
                updated = updated.copy()
        else:
            updated = validate_updated(updated)
        
        # Construct
        new = object.__new__(type(self))
        new.added = added
        new.removed = removed
        new.updated = updated
        return new
