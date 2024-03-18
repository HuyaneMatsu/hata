__all__ = ()

from scarletio import RichAttributeErrorBaseType


class ReplyConfiguration(RichAttributeErrorBaseType):
    """
    Reply configuration for message create endpoints.
    
    Attributes
    ----------
    fail_fallback : `bool`
        Whether normal message should be sent if the referenced message is deleted.
    message_id : `int`
        The referenced message's identifier.
    """
    __slots__ = ('fail_fallback', 'message_id')
    
    def __new__(cls, *, fail_fallback = False, message_id = 0):
        """
        Creates a new message reference.
        
        Parameters
        ----------
        fail_fallback : `bool` = `False`, Optional (Keyword only)
            Whether normal message should be sent if the referenced message is deleted.
        message_id : `int` = `0`, Optional (Keyword only)
            The referenced message's identifier.
        """    
        new = object.__new__(cls)
        new.fail_fallback = fail_fallback
        new.message_id = message_id
        return new
        
    
    def to_data(self):
        """
        Serialises the reply configuration.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {'message_id' : str(self.message_id)}
        
        if self.fail_fallback:
            data['fail_if_not_exists'] = False
        
        return data
    
    
    def __bool__(self):
        """Returns whether the configuration has any valuable configuration stored in it."""
        if self.message_id:
            return True
        
        return False
    
    
    def __eq__(self, other):
        """Returns whether the two configurations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # fail_fallback
        if self.fail_fallback != other.fail_fallback:
            return False
        
        # message_id
        if self.message_id != other.message_id:
            return False
        
        return True
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # message_id
        repr_parts.append(' message_id = ')
        repr_parts.append(repr(self.message_id))
        
        # fail_fallback
        fail_fallback = self.fail_fallback
        if fail_fallback:
            repr_parts.append(', fail_fallback = ')
            repr_parts.append(repr(fail_fallback))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the configuration's hash value."""
        hash_value = 0
        
        # fail_fallback
        hash_value ^= self.fail_fallback
        
        # message_id
        hash_value ^= self.message_id
        
        return hash_value
    
    
    def __or__(self, other):
        """Merges the two configurations"""
        if type(self) is not type(other):
            return NotImplemented
        
        # fail_fallback
        fail_fallback = other.fail_fallback
        if not fail_fallback:
            fail_fallback = self.fail_fallback
        
        # message_id
        message_id = other.message_id
        if not message_id:
            message_id = self.message_id
        
        # Construct
        new = object.__new__(type(self))
        new.fail_fallback = fail_fallback
        new.message_id = message_id
        return new
