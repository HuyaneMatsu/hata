__all__ = ('Preinstance',)

from scarletio import RichAttributeErrorBaseType


class Preinstance(RichAttributeErrorBaseType):
    """
    An object that is picked up and created an instance with after the type is initialised.
    
    Attributes
    ----------
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to preinstance with.
    
    name : `str`
        The instance's name.
    
    positional_parameters : `tuple<object>`
        Additional positional parameters to preinstance with.
    
    value : `int | str`
        The instance's value.
    """
    __slots__ = ('keyword_parameters', 'name', 'positional_parameters', 'value')
    
    def __new__(cls, value, name, *positional_parameters, **keyword_parameters):
        """
        Creates a new value to preinstance..
        
        Parameters
        ----------
        value : `int | str`
            The instance's value.
        
        name : `str`
            The instance's name.
        
        *positional_parameters : Positional parameters
            Additional positional parameters.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        """
        self = object.__new__(cls)
        self.keyword_parameters = keyword_parameters
        self.name = name
        self.positional_parameters = positional_parameters
        self.value = value
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = [type(self).__name__, '(']
        
        # value
        repr_parts.append(repr(self.value))
        
        # name
        repr_parts.append(', ')
        repr_parts.append(repr(self.name))
        
        # positional_parameters
        for positional_parameter in self.positional_parameters:
            repr_parts.append(', ')
            repr_parts.append(repr(positional_parameter))
        
        # keyword_parameters
        keyword_parameters = self.keyword_parameters
        if keyword_parameters:
            for key, value in sorted(keyword_parameters.items()):
                repr_parts.append(', ')
                repr_parts.append(key)
                repr_parts.append(' = ')
                repr_parts.append(repr(value))
        
        repr_parts.append(')')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # value
        hash_value ^= hash(self.value)
        
        # name
        hash_value ^= hash(self.name)
        
        # positional_parameters
        hash_value ^= hash(self.positional_parameters)
        
        # keyword_parameters
        keyword_parameters = self.keyword_parameters
        if keyword_parameters:
            hash_value ^= hash(tuple(sorted(keyword_parameters)))
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # value
        if self.value != other.value:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # positional_parameters
        if self.positional_parameters != other.positional_parameters:
            return False
        
        # keyword_parameters
        if self.keyword_parameters != other.keyword_parameters:
            return False
        
        return True
