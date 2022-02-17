__all__ = ('EmbeddedActivityConfiguration',)

from scarletio import RichAttributeErrorBaseType

class EmbeddedActivityConfiguration(RichAttributeErrorBaseType):
    """
    Configuration of an embedded activity.
    
    Attributes
    ----------
    premium_tier_treatment_default : `int`
        Default value of premium tier treatment for missing keys.
    premium_tier_treatment_map : `None`, `dict` of (`int`, `int`) items
        ???
    required_premium_tier : `int`
        The required boost level of a guild to start the activity.
    """
    __slots__ = ('premium_tier_treatment_default', 'premium_tier_treatment_map', 'required_premium_tier',)
    
    def __new__(cls, data):
        """
        Creates a new embedded activity configuration from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embedded activity configuration data.
        """
        try:
            premium_tier_treatment_all = data['activity_premium_tier_treatment_map']
        except KeyError:
            premium_tier_treatment_default = 0
            premium_tier_treatment_map = None
        else:
            premium_tier_treatment_default = premium_tier_treatment_all.pop('default', 0)
            premium_tier_treatment_map = None
            
            for key, value in premium_tier_treatment_all.items():
                if value != premium_tier_treatment_default:
                    if premium_tier_treatment_map is None:
                        premium_tier_treatment_map = {}
                    
                    premium_tier_treatment_map[int(key)] = value
        
        required_premium_tier = data.get('activity_premium_tier_level', 0)
        
        self = object.__new__(cls)
        self.premium_tier_treatment_default = premium_tier_treatment_default
        self.premium_tier_treatment_map = premium_tier_treatment_map
        self.required_premium_tier = required_premium_tier
        return self
    
    
    def __repr__(self):
        """Returns the embedded activity configuration's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        premium_tier_treatment_default = self.premium_tier_treatment_default
        if premium_tier_treatment_default:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' premium_tier_treatment_default=')
            repr_parts.append(repr(premium_tier_treatment_default))
        
        
        premium_tier_treatment_map = self.premium_tier_treatment_map
        if (premium_tier_treatment_map is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' premium_tier_treatment_map=')
            repr_parts.append(repr(premium_tier_treatment_map))
            
        
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
        
        premium_tier_treatment_default = self.premium_tier_treatment_default
        if premium_tier_treatment_default:
            hash_value ^= premium_tier_treatment_default << 4
        
        premium_tier_treatment_map = self.premium_tier_treatment_map
        if (premium_tier_treatment_map is not None):
            hash_value ^= hash(tuple(premium_tier_treatment_map.items()))
        
        required_premium_tier = self.required_premium_tier
        if required_premium_tier:
            hash_value ^= required_premium_tier
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activity configurations are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.premium_tier_treatment_default != other.premium_tier_treatment_default:
            return False
        
        if self.premium_tier_treatment_map != other.premium_tier_treatment_map:
            return False
        
        if self.required_premium_tier != other.required_premium_tier:
            return False
        
        return True
