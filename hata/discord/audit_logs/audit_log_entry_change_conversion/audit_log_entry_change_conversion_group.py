__all__ = ('AuditLogEntryChangeConversionGroup', )

from scarletio import RichAttributeErrorBaseType


class AuditLogEntryChangeConversionGroup(RichAttributeErrorBaseType):
    """
    Represents how changes are converted of an audit log entry.
    
    Attributes
    ----------
    conversions : `tuple<AuditLogEntryChangeConversion>`
        The grouped conversions.
    key_pre_checker_conversions : `None | list<AuditLogEntryChangeConversion>`
        Conversions which have key pre checker.
    key_to_conversion : `None | dict<str, AuditLogEntryChangeConversion>`
        Field key to conversion relation used when deserializing.
    name_to_conversion : `None | dict<str, AuditLogEntryChangeConversion>`
        Name to conversion relation.
    """
    __slots__ = ('conversions', 'key_pre_checker_conversions', 'key_to_conversion', 'name_to_conversion',)
    
    def __new__(cls, *conversions):
        """
        Creates a new change conversion group with the given conversions..
        
        Parameters
        ----------
        *conversions : ``AuditLogEntryChangeConversion``
            Conversions to group.
        """
        key_pre_checker_conversions = None
        key_to_conversion = None
        name_to_conversion = None
        
        
        for conversion in conversions:
            if conversion.should_add_as_key_based_deserializer():
                for key in conversion.iter_field_keys():
                    if key_to_conversion is None:
                        key_to_conversion = {}
                    
                    key_to_conversion[key] = conversion
            
            if conversion.should_add_as_key_pre_check_deserializer():
                if key_pre_checker_conversions is None:
                    key_pre_checker_conversions = []
                
                key_pre_checker_conversions.append(conversion)
            
            if conversion.should_add_by_field_name():
                if name_to_conversion is None:
                    name_to_conversion = {}
                
                name_to_conversion[conversion.field_name] = conversion
        
        # Construct
        self = object.__new__(cls)
        self.conversions = conversions
        self.key_pre_checker_conversions = key_pre_checker_conversions
        self.key_to_conversion = key_to_conversion
        self.name_to_conversion = name_to_conversion
        return self
    
    
    def __repr__(self):
        """Returns the change conversion's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # conversions
        repr_parts.append(' conversions = ')
        repr_parts.append(repr(self.conversions))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the entry change conversion's hash value."""
        return hash(self.conversions)
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # conversions
        if self.conversions != other.conversions:
            return False
        
        return True
    
    
    def iter_field_keys(self):
        """
        Iterates over the field keys of the conversion group.
        
        This method is an iterable generator.
        
        Yields
        ------
        field_key : `str`
        """
        for conversion in self.conversions:
            yield from conversion.iter_field_keys()
    
    
    def get_conversion_for_key(self, key):
        """
        Gets the conversion for the given key.
        
        Parameters
        ----------
        key : `str`
            Conversion key.
        
        Returns
        -------
        conversion : `None | AuditLogEntryChangeConversion`
        """
        key_to_conversion = self.key_to_conversion
        if (key_to_conversion is not None):
            try:
                conversion = key_to_conversion[key]
            except KeyError:
                pass
            else:
                return conversion
        
        key_pre_checker_conversions = self.key_pre_checker_conversions
        if (key_pre_checker_conversions is not None):
            for conversion in key_pre_checker_conversions:
                if conversion.change_deserialization_key_pre_check(key):
                    return conversion
    
    
    def get_conversion_for_name(self, name):
        """
        Gets the conversion for the given name.
        
        Parameters
        ----------
        name : `str`
            Conversion name.
        
        Returns
        -------
        conversion : `None | AuditLogEntryChangeConversion`
        """
        name_to_conversion = self.name_to_conversion
        if (name_to_conversion is not None):
            return name_to_conversion.get(name, None)
