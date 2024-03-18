__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .descriptor import _conversion_descriptor_sort_key


class SerializationConfiguration(RichAttributeErrorBaseType):
    """
    Configuration representing which fields of a builder and how should be serialised.
    
    Attributes
    ----------
    conversions : `tuple<Conversion>`
        Conversions.
    defaults : `bool`
        Whether defaults should be included.
    """
    __slots__ = ('conversions', 'defaults')
    
    def __new__(cls, conversion_descriptors, defaults):
        """
        Creates a new serialisation configuration.
        
        Parameters
        ----------
        conversion_descriptors : `list<ConversionDescriptor>`
            Conversion descriptors.
        defaults : `bool`
            Whether defaults should be included.
        """
        conversion_descriptors = sorted(conversion_descriptors, key = _conversion_descriptor_sort_key)
        conversions = (*(descriptor.conversion for descriptor in conversion_descriptors),)
        
        self = object.__new__(cls)
        self.conversions = conversions
        self.defaults = defaults
        return self
    
    
    def __repr__(self):
        """Returns the serialization configuration's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # conversions
        repr_parts.append(' conversions = ')
        repr_parts.append(repr(self.conversions))
        
        # defaults
        repr_parts.append(' defaults = ')
        repr_parts.append(repr(self.defaults))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
