__all__ = ('AuditLogEntryDetailConversionGroup', )

from scarletio import RichAttributeErrorBaseType


class AuditLogEntryDetailConversionGroup(RichAttributeErrorBaseType):
    """
    Represents how details are converted of an audit log entry.
    
    Attributes
    ----------
    conversions : `tuple<AuditLogEntryDetailConversion>`
        The grouped conversions.
    key_to_conversion : `None | dict<str, AuditLogEntryDetailConversion>`
        Field key to conversion relation used when deserializing.
    name_to_conversion : `None | dict<str, AuditLogEntryDetailConversion>`
        Name to conversion relation.
    """
    __slots__ = ('conversions', 'key_to_conversion', 'name_to_conversion')
    
    def __new__(cls, *conversions):
        """
        Creates a new detail conversion group with the given conversions..
        
        Parameters
        ----------
        *conversions : ``AuditLogEntryDetailConversion``
            Conversions to group.
        """
        key_to_conversion = None
        name_to_conversion = None
        
        for conversion in conversions:
            field_key = conversion.field_key
            
            if key_to_conversion is None:
                key_to_conversion = {}
            
            key_to_conversion[field_key] = conversion
            
            field_name = conversion.field_name
            if field_name:
                if name_to_conversion is None:
                    name_to_conversion = {}
                
                name_to_conversion[field_name] = conversion
        
        # Construct
        self = object.__new__(cls)
        self.conversions = conversions
        self.key_to_conversion = key_to_conversion
        self.name_to_conversion = name_to_conversion
        return self
    
    
    def __repr__(self):
        """Returns the detail conversion's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # conversions
        repr_parts.append(' conversions = ')
        repr_parts.append(repr(self.conversions))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the entry detail conversion's hash value."""
        return hash(self.conversions)
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # conversions
        if self.conversions != other.conversions:
            return False
        
        return True
    
    
    def get_conversion_for_key(self, key):
        """
        Gets the conversion for the given key.
        
        Parameters
        ----------
        key : `str`
            Conversion key.
        
        Returns
        -------
        conversion : `None | AuditLogEntryDetailConversion`
        """
        key_to_conversion = self.key_to_conversion
        if (key_to_conversion is not None):
            return key_to_conversion.get(key, None)

    
    def get_conversion_for_name(self, name):
        """
        Gets the conversion for the given name.
        
        Parameters
        ----------
        name : `str`
            Conversion name.
        
        Returns
        -------
        conversion : `None | AuditLogEntryDetailConversion`
        """
        name_to_conversion = self.name_to_conversion
        if (name_to_conversion is not None):
            return name_to_conversion.get(name, None)
