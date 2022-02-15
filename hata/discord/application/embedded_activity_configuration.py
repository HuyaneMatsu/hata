__all__ = ('EmbeddedActivityConfiguration',)

from scarletio import RichAttributeErrorBaseType

class EmbeddedActivityConfiguration(RichAttributeErrorBaseType):
    """
    Configuration of an embedded activity.
    
    Attributes
    ----------
    required_premium_tier : `int`
        The required boost level of a guild to start the activity.
    """
    __slots__ = ('required_premium_tier',)
    
    def __new__(cls, data):
        """
        Creates a new embedded activity configuration from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embedded activity configuration data.
        """
        self = object.__new__(cls)
        self.required_premium_tier = data.get('activity_premium_tier_level', 0)
        return self
    
    
    def __repr__(self):
        """Returns the embedded activity configuration's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        required_premium_tier = self.required_premium_tier
        if required_premium_tier:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' required_premium_tier=')
            repr_parts.append(repr(required_premium_tier))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the embedded activity configuration's hash value."""
        hash_value = 0
        
        required_premium_tier = self.required_premium_tier
        if required_premium_tier:
            hash_value ^= required_premium_tier
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activity configurations are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.required_premium_tier != other.required_premium_tier:
            return False
        
        return True
