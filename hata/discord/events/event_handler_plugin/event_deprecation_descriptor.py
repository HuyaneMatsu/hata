__all__ = ()

from scarletio import RichAttributeErrorBaseType


class EventDeprecationDescriptor(RichAttributeErrorBaseType):
    """
    Descriptor added for deprecated events.
    
    Attributes
    ----------
    name : `str`
        The name of the deprecated event.
    
    deprecation : ``EventDeprecation``
        Deprecation notice.
    """
    __slots__ = ('deprecation', 'name')
    
    def __new__(cls, name, deprecation):
        """
        Creates a new event deprecation descriptor.
        
        Parameters
        ----------
        name : `str`
            The name of the deprecated event.
        
        deprecation : ``EventDeprecation``
            Deprecation notice.
        """
        self = object.__new__(cls)
        self.deprecation = deprecation
        self.name = name
        return self
    
    
    def __get__(self, instance, instance_type):
        """
        Gets the field with the conversion.
        If accessed as a type attribute returns itself.
        
        Parameters
        ----------
        instance : `None | EventHandlerPlugin`
            Instance to set the fields to.
        
        instance_type : ``EventHandlerPluginMeta``
            The instance's type.
        
        Returns
        -------
        value : `object | self`
        """
        if instance is None:
            return self
        
        deprecation = self.deprecation
        deprecation.trigger(self.name, 2)
        return getattr(instance, deprecation.use_instead)
    
    
    def __set__(self, instance, value):
        """
        Sets the field.
        
        Parameters
        ----------
        instance : `FlagBase`
            Instance to set the fields to.
        
        value : `object`
            The value to set.
        """
        deprecation = self.deprecation
        deprecation.trigger(self.name, 2)
        setattr(instance, deprecation.use_instead, value)

    
    def __delattr__(self, instance):
        """
        Deletes the field.
        
        Parameters
        ----------
        instance : `FlagBase`
            Instance to set the fields to.
        """
        deprecation = self.deprecation
        deprecation.trigger(self.name, 2)
        delattr(instance, deprecation.use_instead)
    
    
    def __repr__(self):
        """Returns the descriptor's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # deprecation
        repr_parts.append(', deprecation = ')
        repr_parts.append(repr(self.deprecation))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two descriptors are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # deprecation
        if self.deprecation != other.deprecation:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the descriptor's hash value."""
        hash_value = 0
        
        # deprecation
        hash_value ^= hash(self.deprecation)
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
