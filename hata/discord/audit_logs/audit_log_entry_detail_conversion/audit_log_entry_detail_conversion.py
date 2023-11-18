__all__ = ('AuditLogEntryDetailConversion', )

from scarletio import RichAttributeErrorBaseType

from ..conversion_helpers.helpers import _eq_functions, _hash_function


class AuditLogEntryDetailConversion(RichAttributeErrorBaseType):
    """
    Represents how details are converted of an audit log entry.
    
    Attributes
    ----------
    field_key : `str`
        The serialised name of the field.
    field_name : `str`
        The field's name.
    value_deserializer : `FunctionType | MethodType`
        Raw to processed value converter.
    value_serializer : `FunctionType | MethodType`
        Processed to raw value converter.
    value_validator : `FunctionType | MethodType`
        Detail value validator.
    """
    __slots__ = ('field_key', 'field_name', 'value_deserializer', 'value_serializer', 'value_validator')
    
    def __new__(cls, field_key, field_name, *, value_deserializer = ..., value_serializer = ..., value_validator = ...):
        """
        Creates a new detail conversion representation with the given fields.
        
        Parameters
        ----------
        field_key : `str`
            The serialised name of the field.
        field_name : `str`
            The field's name.
        value_deserializer : `FunctionType | MethodType`, Optional (Keyword only)
            Raw to processed value converter.
        value_serializer : `FunctionType | MethodType`, Optional (Keyword only)
            Processed to raw value converter.
        value_validator : `FunctionType | MethodType`, Optional (Keyword only)
            Detail value validator.
        """
        if value_deserializer is ...:
            value_deserializer = None
        
        if value_serializer is ...:
            value_serializer = None
        
        if value_validator is ...:
            value_validator = None
        
        self = object.__new__(cls)
        self.field_key = field_key
        self.field_name = field_name
        self.value_deserializer = value_deserializer
        self.value_serializer = value_serializer
        self.value_validator = value_validator
        return self
    
    
    def __repr__(self):
        """Returns the detail conversion's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # field_key
        repr_parts.append(' field_key = ')
        repr_parts.append(repr(self.field_key))
        
        # field_name
        repr_parts.append(', field_name = ')
        repr_parts.append(repr(self.field_name))
        
        # value_deserializer
        value_deserializer = self.value_deserializer
        if value_deserializer is not None:
            repr_parts.append(', value_deserializer = ')
            repr_parts.append(value_deserializer.__module__)
            repr_parts.append('.')
            repr_parts.append(value_deserializer.__name__)
        
        # value_serializer
        value_serializer = self.value_serializer
        if value_serializer is not None:
            repr_parts.append(', value_serializer = ')
            repr_parts.append(value_serializer.__module__)
            repr_parts.append('.')
            repr_parts.append(value_serializer.__name__)
        
        # value_validator
        value_validator = self.value_validator
        if value_validator is not None:
            repr_parts.append(', value_validator = ')
            repr_parts.append(value_validator.__module__)
            repr_parts.append('.')
            repr_parts.append(value_validator.__name__)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the entry detail conversion's hash value."""
        hash_value = 0
        
        # field_key
        field_key = self.field_key
        hash_value ^= hash(field_key)
        
        # field_name
        field_name = self.field_name
        if field_key != field_name:
            hash_value ^= hash(field_name)
        
        # value_deserializer
        value_deserializer = self.value_deserializer
        if value_deserializer is not None:
            hash_value ^= _hash_function(value_deserializer)
        
        # value_serializer
        value_serializer = self.value_serializer
        if value_serializer is not None:
            hash_value ^= _hash_function(value_serializer)
        
        # value_validator
        value_validator = self.value_validator
        if value_validator is not None:
            hash_value ^= _hash_function(value_validator)
        
        return hash_value
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # field_key
        if self.field_key != other.field_key:
            return False
        
        # field_name
        if self.field_name != other.field_name:
            return False
        
        # value_deserializer
        if not _eq_functions(self.value_deserializer, other.value_deserializer):
            return False
        
        # value_serializer
        if not _eq_functions(self.value_serializer, other.value_serializer):
            return False
        
        # value_validator
        if not _eq_functions(self.value_validator, other.value_validator):
            return False
        
        return True
    
    
    def set_value_deserializer(self, value_deserializer):
        """
        Sets the get converter of the conversion and returns it back.
        
        Parameters
        ----------
        value_deserializer : `FunctionType | MethodType`
            Converter to put.
        
        Returns
        -------
        value_deserializer : `value_deserializer`
        """
        self.value_deserializer = value_deserializer
        return value_deserializer
    
    
    def set_value_serializer(self, value_serializer):
        """
        Sets the put converter of the conversion and returns it back.
        
        Parameters
        ----------
        value_serializer : `FunctionType | MethodType`
            Converter to put.
        
        Returns
        -------
        value_serializer : `value_serializer`
        """
        self.value_serializer = value_serializer
        return value_serializer
    
    
    def set_value_validator(self, value_validator):
        """
        Sets the converter of the conversion and returns it back.
        
        Parameters
        ----------
        value_validator : `FunctionType | MethodType`
            Converter to put.
        
        Returns
        -------
        value_validator : `value_validator`
        """
        self.value_validator = value_validator
        return value_validator
