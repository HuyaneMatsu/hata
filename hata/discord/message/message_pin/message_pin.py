__all__ = ('MessagePin',)

from scarletio import RichAttributeErrorBaseType

from ...utils import DATETIME_FORMAT_CODE, DISCORD_EPOCH_START

from .fields import parse_message, parse_pinned_at, put_message, put_pinned_at, validate_message, validate_pinned_at


class MessagePin(RichAttributeErrorBaseType):
    """
    Stores pin information.
    
    Attributes
    ----------
    message : ``None | Message``
        The pinned message.
    
    pinned_at : `DateTime`
        When the message was pinned.
    """
    __slots__ = ('message', 'pinned_at')
    
    def __new__(cls, *, message = ..., pinned_at = ...):
        """
        Creates a new message pin with the given parameters.
        
        Parameters
        ----------
        message : ``None | Message``, Optional (Keyword only)
            The pinned message.
        
        pinned_at : `DateTime`, Optional (Keyword only)
            When the message was pinned.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # message
        if message is ...:
            message = None
        else:
            message = validate_message(message)
        
        # pinned_at
        if pinned_at is ...:
            pinned_at = DISCORD_EPOCH_START
        else:
            pinned_at = validate_pinned_at(pinned_at)
        
        # Construct
        self = object.__new__(cls)
        self.message = message
        self.pinned_at = pinned_at
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a message pin from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message pin data.
        """
        self = object.__new__(cls)
        self.message = parse_message(data)
        self.pinned_at = parse_pinned_at(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the message pin to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_message(self.message, data, defaults)
        put_pinned_at(self.pinned_at, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # message
        repr_parts.append(' message = ')
        repr_parts.append(repr(self.message))
        
        # pinned_at
        repr_parts.append(', pinned_at = ')
        repr_parts.append(format(self.pinned_at, DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # message
        message = self.message
        if (message is not None):
            hash_value ^= hash(message)
        
        # pinned_at
        hash_value ^= hash(self.pinned_at)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return False
        
        # message
        if (self.message != other.message):
            return False
        
        # pinned_at
        if (self.pinned_at != other.pinned_at):
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the message pin.
        
        Returns
        -------
        new : `instance<type<self>`
        """
        new = object.__new__(type(self))
        new.message = self.message
        new.pinned_at = self.pinned_at
        return new
    
    
    def copy_with(self, *, message = ..., pinned_at = ...):
        """
        Copies the message pin with the given parameters.
        
        Parameters
        ----------
        message : ``None | Message``, Optional (Keyword only)
            The pinned message.
        
        pinned_at : `DateTime`, Optional (Keyword only)
            When the message was pinned.
        
        Returns
        -------
        new : `instance<type<self>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # message
        if message is ...:
            message = self.message
        else:
            message = validate_message(message)
        
        # pinned_at
        if pinned_at is ...:
            pinned_at = self.pinned_at
        else:
            pinned_at = validate_pinned_at(pinned_at)
        
        # Construct
        new = object.__new__(type(self))
        new.message = message
        new.pinned_at = pinned_at
        return new
