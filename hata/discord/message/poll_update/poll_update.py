__all__ = ('PollUpdate',)

from itertools import count

from scarletio import RichAttributeErrorBaseType

from ...poll import Poll

from .fields import validate_old_attributes, validate_poll


class PollUpdate(RichAttributeErrorBaseType):
    """
    Represents an updated poll with storing the poll and it's old updated attributes in a `dict`.
    
    Attributes
    ----------
    old_attributes : `dict<str, object>`
        The changed attributes of the poll in `attribute-name` - `old-value` relation. Can contain any of the
        following items:
        
        +---------------------------+-----------------------------------+
        | Keys                      | Values                            |
        +===========================+===================================+
        | allow_multiple_choices    | `bool`                            |
        +---------------------------+-----------------------------------+
        | answers                   | `None`, `tuple` of ``PollAnswer`` |
        +---------------------------+-----------------------------------+
        | duration                  | `int`                             |
        +---------------------------+-----------------------------------+
        | expires_at                | `None`, `DateTime`                |
        +---------------------------+-----------------------------------+
        | finalized                 | `bool`                            |
        +---------------------------+-----------------------------------+
        | layout                    | ``PollLayout``                    |
        +---------------------------+-----------------------------------+
        | question                  | `None`, ``PollQuestion``          |
        +---------------------------+-----------------------------------+
    
    poll : ``Poll``
        The updated poll.
    """
    __slots__ = ('poll', 'old_attributes',)
    
    def __new__(cls, *, old_attributes = ..., poll = ...):
        """
        Creates a new poll change instance with the given fields.
        
        Parameters
        ----------
        old_attributes : `None`, `dict<str, object>`, Optional (Keyword only)
            The changed attributes of the poll.
        
        poll : ``Poll``, Optional (Keyword only)
            The updated poll.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
        """
        # old_attributes
        if old_attributes is ...:
            old_attributes = {}
        else:
            old_attributes = validate_old_attributes(old_attributes)
        
        # poll
        if poll is ...:
            poll = Poll()
        else:
            poll = validate_poll(poll)
        
        # Construct
        self = object.__new__(cls)
        self.old_attributes = old_attributes
        self.poll = poll
        return self
    
    
    @classmethod
    def from_fields(cls, poll, old_attributes):
        """
        Creates a new poll change instance with the given fields.
        
        Parameters
        ----------
        poll : ``Poll``
            The updated poll.
        
        old_attributes : `dict<str, object>`
            The changed attributes of the poll.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.old_attributes = old_attributes
        self.poll = poll
        return self
    
    
    def __repr__(self):
        """Returns the representation of the poll update."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' poll = ')
        repr_parts.append(repr(self.poll))
        
        repr_parts.append(', old_attributes = ')
        repr_parts.append(repr(self.old_attributes))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the poll update's hash value."""
        hash_value = 0
        
        # old_attributes
        old_attributes = self.old_attributes
        hash_value ^= len(old_attributes)
        
        for mask, key in zip(count(5, 7), sorted(old_attributes.keys())):
            hash_value ^= (mask | hash(key)) & hash(old_attributes[key])
        
        # poll
        hash_value ^= hash(self.poll)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two poll updates are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.old_attributes != other.old_attributes:
            return False
        
        if self.poll != other.poll:
            return False
        
        return True
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    
    def __iter__(self):
        """
        Unpacks the poll update.
        
        This method is a generator.
        """
        yield self.poll
        yield self.old_attributes
    
    
    def copy(self):
        """
        Copies the poll update.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.old_attributes = self.old_attributes.copy()
        new.poll = self.poll.copy()
        return new
    
    
    def copy_with(self, *, old_attributes = ..., poll = ...):
        """
        Copies the poll change with the given fields.
        
        Parameters
        ----------
        old_attributes : `None`, `dict<str, object>`, Optional (Keyword only)
            The changed attributes of the poll.
        
        poll : ``Poll``, Optional (Keyword only)
            The updated poll.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
        """
        # old_attributes
        if old_attributes is ...:
            old_attributes = self.old_attributes.copy()
        else:
            old_attributes = validate_old_attributes(old_attributes)
        
        # poll
        if poll is ...:
            poll = self.poll.copy()
        else:
            poll = validate_poll(poll)
        
        # Construct
        new = object.__new__(type(self))
        new.poll = poll
        new.old_attributes = old_attributes
        return new
