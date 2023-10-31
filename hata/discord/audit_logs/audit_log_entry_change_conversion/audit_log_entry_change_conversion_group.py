__all__ = ('AuditLogEntryChangeConversionGroup', )

from scarletio import RichAttributeErrorBaseType


class AuditLogEntryChangeConversionGroup(RichAttributeErrorBaseType):
    """
    Represents how changes are converted of an audit log entry.
    
    Attributes
    ----------
    conversions : `tuple<AuditLogEntryChangeConversion>`
        The grouped conversions.
    get_converters : `dict<str, (str, int, FunctionType)>`
        Raw to processed converters.
    put_converters : `dict<(str, int), (str, FunctionType)>`
       Processed to raw converters.
    validators : `dict<(str, int), FunctionType>`
        Validators.
    """
    __slots__ = ('conversions', 'get_converters', 'put_converters', 'validators')
    
    def __new__(cls, *conversions):
        """
        Creates a new change conversion group with the given conversions..
        
        Parameters
        ----------
        *conversions : ``AuditLogEntryChangeConversion``
            Conversions to group.
        """
        get_converters = {}
        put_converters = {}
        validators = {}
        
        for conversion in conversions:
            get_converters.setdefault(
                conversion.field_key,
                (conversion.field_name, conversion.flags, conversion.get_converter),
            )
            put_converters.setdefault(
                (conversion.field_name, conversion.flags),
                (conversion.field_key, conversion.put_converter),
            )
            validators.setdefault(
                (conversion.field_name, conversion.flags),
                conversion.validator,
            )
        
        # Construct
        self = object.__new__(cls)
        self.conversions = conversions
        self.get_converters = get_converters
        self.put_converters = put_converters
        self.validators = validators
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
