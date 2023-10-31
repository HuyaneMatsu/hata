__all__ = ('AuditLogEntryDetailConversion', )

from scarletio import RichAttributeErrorBaseType

from ..conversion_helpers.helpers import _default_converter_and_validator, _eq_functions, _hash_function


class AuditLogEntryDetailConversion(RichAttributeErrorBaseType):
    """
    Represents how details are converted of an audit log entry.
    
    Attributes
    ----------
    field_key : `str`
        The serialised name of the field.
    field_name : `str`
        The field's name.
    get_converter : `FunctionType`
        Raw to processed value converter.
    put_converter : `FunctionType`
        Processed to raw value converter.
    validator : `FunctionType`
        Detail validator.
    """
    __slots__ = ('field_key', 'field_name', 'get_converter', 'put_converter', 'validator')
    
    def __new__(cls, field_key, field_name, *, get_converter = ..., put_converter = ..., validator = ...):
        """
        Creates a new detail conversion representation with the given fields.
        
        Parameters
        ----------
        field_key : `str`
            The serialised name of the field.
        field_name : `str`
            The field's name.
        get_converter : `FunctionType`, Optional (Keyword only)
            Raw to processed value converter.
        put_converter : `FunctionType`, Optional (Keyword only)
            Processed to raw value converter.
        validator : `FunctionType`, Optional (Keyword only)
            Detail validator.
        """
        if get_converter is ...:
            get_converter = _default_converter_and_validator
        
        if put_converter is ...:
            put_converter = _default_converter_and_validator
        
        if validator is ...:
            validator = _default_converter_and_validator
        
        self = object.__new__(cls)
        self.field_key = field_key
        self.field_name = field_name
        self.get_converter = get_converter
        self.put_converter = put_converter
        self.validator = validator
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
        
        # get_converter
        get_converter = self.get_converter
        if get_converter is not _default_converter_and_validator:
            repr_parts.append(', get_converter = ')
            repr_parts.append(get_converter.__module__)
            repr_parts.append('.')
            repr_parts.append(get_converter.__name__)
        
        # put_converter
        put_converter = self.put_converter
        if put_converter is not _default_converter_and_validator:
            repr_parts.append(', put_converter = ')
            repr_parts.append(put_converter.__module__)
            repr_parts.append('.')
            repr_parts.append(put_converter.__name__)
        
        # validator
        validator = self.validator
        if validator is not _default_converter_and_validator:
            repr_parts.append(', validator = ')
            repr_parts.append(validator.__module__)
            repr_parts.append('.')
            repr_parts.append(validator.__name__)
        
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
        
        # get_converter
        get_converter = self.get_converter
        if get_converter is not _default_converter_and_validator:
            hash_value ^= _hash_function(get_converter)
        
        # put_converter
        put_converter = self.put_converter
        if put_converter is not _default_converter_and_validator:
            hash_value ^= _hash_function(put_converter)
        
        # validator
        validator = self.validator
        if validator is not _default_converter_and_validator:
            hash_value ^= _hash_function(validator)
        
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
        
        # get_converter
        if not _eq_functions(self.get_converter, other.get_converter):
            return False
        
        # put_converter
        if not _eq_functions(self.put_converter, other.put_converter):
            return False
        
        # validator
        if not _eq_functions(self.validator, other.validator):
            return False
        
        return True
    
    
    def set_get_converter(self, get_converter):
        """
        Sets the get converter of the conversion and returns it back.
        
        Parameters
        ----------
        get_converter : `FunctionType`
            Converter to put.
        
        Returns
        -------
        get_converter : `get_converter`
        """
        self.get_converter = get_converter
        return get_converter
    
    
    def set_put_converter(self, put_converter):
        """
        Sets the put converter of the conversion and returns it back.
        
        Parameters
        ----------
        put_converter : `FunctionType`
            Converter to put.
        
        Returns
        -------
        put_converter : `put_converter`
        """
        self.put_converter = put_converter
        return put_converter
    
    
    def set_validator(self, validator):
        """
        Sets the converter of the conversion and returns it back.
        
        Parameters
        ----------
        validator : `FunctionType`
            Converter to put.
        
        Returns
        -------
        validator : `validator`
        """
        self.validator = validator
        return validator
