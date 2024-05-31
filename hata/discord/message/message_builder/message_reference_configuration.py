__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .preinstanced import MessageReferenceType


class MessageReferenceConfiguration(RichAttributeErrorBaseType):
    """
    Message reference configuration for message create endpoints.
    
    Attributes
    ----------
    channel_id : `int`
        The referenced message's channel's identifier. Used when forwarding.
    fail_fallback : `bool`
        Whether normal message should be sent if the referenced message is deleted. Used when replying.
    message_id : `int`
        The referenced message's identifier.
    message_reference_type : ``MessageReferenceType``
        What kind of reference does the instance represents.
    """
    __slots__ = ('channel_id', 'fail_fallback', 'message_id', 'type')
    
    def __new__(
        cls,
        *,
        channel_id = 0,
        fail_fallback = False,
        message_id = 0,
        message_reference_type = MessageReferenceType.reply,
    ):
        """
        Creates a new message reference.
        
        Parameters
        ----------
        channel_id : `int` = `0`, Optional (Keyword only)
            The referenced message's channel's identifier.
        fail_fallback : `bool` = `False`, Optional (Keyword only)
            Whether normal message should be sent if the referenced message is deleted.
        message_id : `int` = `0`, Optional (Keyword only)
            The referenced message's identifier.
        message_reference_type : ``MessageReferenceType`` = `MessageReferenceType.reply`, Optional (Keyword only)
            What kind of reference does the instance represents.
        """    
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.fail_fallback = fail_fallback
        self.message_id = message_id
        self.type = message_reference_type
        return self
        
    
    def to_data(self):
        """
        Serialises the message reference configuration.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {'message_id' : str(self.message_id)}
        
        message_reference_type = self.type
        
        if message_reference_type is MessageReferenceType.reply:
            if self.fail_fallback:
                data['fail_if_not_exists'] = False
        
        else:
            data['type'] = message_reference_type.value
            
            if message_reference_type is MessageReferenceType.forward:
                data['channel_id'] = str(self.channel_id)
        
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
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # fail_fallback
        if self.fail_fallback != other.fail_fallback:
            return False
        
        # message_id
        if self.message_id != other.message_id:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        # channel_id
        channel_id = self.channel_id
        if channel_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' channel_id = ')
            repr_parts.append(repr(channel_id))
        
        # message_id
        message_id = self.message_id
        if message_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
    
            repr_parts.append(' message_id = ')
            repr_parts.append(repr(message_id))
        
        # fail_fallback
        fail_fallback = self.fail_fallback
        if fail_fallback:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(', fail_fallback = ')
            repr_parts.append(repr(fail_fallback))
        
        # type
        message_reference_type = self.type
        if message_reference_type is not MessageReferenceType.reply:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
    
            repr_parts.append(' type = ')
            repr_parts.append(message_reference_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(message_reference_type.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the configuration's hash value."""
        hash_value = 0
        
        # channel_id
        hash_value ^= self.channel_id
        
        # fail_fallback
        hash_value ^= self.fail_fallback
        
        # message_id
        hash_value ^= self.message_id
        
        # type
        hash_value ^= self.type
        
        return hash_value
    
    
    def __or__(self, other):
        """Merges the two configurations"""
        if type(self) is not type(other):
            return NotImplemented
        
        # channel_id
        channel_id = other.channel_id
        if not channel_id:
            channel_id = self.channel_id
        
        # fail_fallback
        fail_fallback = other.fail_fallback
        if not fail_fallback:
            fail_fallback = self.fail_fallback
        
        # message_id
        message_id = other.message_id
        if not message_id:
            message_id = self.message_id
        
        # message_reference_type
        message_reference_type = other.type
        if message_reference_type is MessageReferenceType.reply:
            message_reference_type = self.type
        
        # Construct
        new = object.__new__(type(self))
        new.channel_id = channel_id
        new.fail_fallback = fail_fallback
        new.message_id = message_id
        new.type = message_reference_type
        return new
