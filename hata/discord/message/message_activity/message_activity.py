__all__ = ('MessageActivity', )

from scarletio import RichAttributeErrorBaseType

from .fields import parse_party_id, parse_type, put_party_id_into, put_type_into, validate_party_id, validate_type
from .preinstanced import MessageActivityType


class MessageActivity(RichAttributeErrorBaseType):
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    party_id : `None`, `str`
        The message activity's party's id.
    type : ``MessageActivityType``
        The message activity's type.
    """
    __slots__ = ('party_id', 'type',)
    
    
    def __new__(cls, *, message_activity_type = ..., party_id = ...):
        """
        Creates a new message activity from the given parameters.
        
        Parameters
        ----------
        message_activity_type : ``MessageActivityType``, `int`, Optional (Keyword only)
            The message activity's type.
        party_id : `None`, `str`, Optional (Keyword only)
            The message activity's party's id.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # message_activity_type
        if message_activity_type is ...:
            message_activity_type = MessageActivityType.none
        else:
            message_activity_type = validate_type(message_activity_type)
        
        # party_id
        if party_id is ...:
            party_id = None
        else:
            party_id = validate_party_id(party_id)
        
        self = object.__new__(cls)
        self.party_id = party_id
        self.type = message_activity_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``MessageActivity`` from message activity data included inside of a ``Message``'s data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Message activity data.
        """
        self = object.__new__(cls)
        self.party_id = parse_party_id(data)
        self.type = parse_type(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the message activity back to json a serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`)
        """
        data = {}
        put_party_id_into(self.party_id, data, defaults)
        put_type_into(self.type, data, defaults)
        return data
    
    
    def __eq__(self, other):
        """Returns whether the two message activities are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # party_id
        if self.party_id != other.party_id:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the message activity's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        party_type = self.type
        repr_parts.append(' type = ')
        repr_parts.append(repr(party_type.name))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(party_type.value))
        
        party_id = self.party_id
        if (party_id is not None):
            repr_parts.append(', party_id = ')
            repr_parts.append(repr(party_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the message activity's hash value."""
        hash_value = 0
        
        # party_id
        party_id = self.party_id
        if (party_id is not None):
            hash_value ^= hash(party_id)
        
        # type
        hash_value ^= self.type.value
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the message activity.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.party_id = self.party_id
        new.type = self.type
        return new
    
    
    def copy_with(self, *, message_activity_type = ..., party_id = ...):
        """
        Copies the message activity with the given fields.
        
        Parameters
        ----------
        message_activity_type : ``MessageActivityType``, `int`, Optional (Keyword only)
            The message activity's type.
        party_id : `None`, `str`, Optional (Keyword only)
            The message activity's party's id.
        
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
        # message_activity_type
        if message_activity_type is ...:
            message_activity_type = self.type
        else:
            message_activity_type = validate_type(message_activity_type)
        
        # party_id
        if party_id is ...:
            party_id = self.party_id
        else:
            party_id = validate_party_id(party_id)
        
        new = object.__new__(type(self))
        new.party_id = party_id
        new.type = message_activity_type
        return new
