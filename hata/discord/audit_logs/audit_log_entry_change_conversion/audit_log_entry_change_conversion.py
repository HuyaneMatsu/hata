__all__ = ('AuditLogEntryChangeConversion', )

from scarletio import RichAttributeErrorBaseType

from ..conversion_helpers.helpers import _eq_functions, _hash_function

from .change_deserializers import change_deserializer_modification
from .change_serializers import change_serializer_modification


class AuditLogEntryChangeConversion(RichAttributeErrorBaseType):
    """
    Represents how changes are converted of an audit log entry.
    
    Attributes
    ----------
    change_deserialization_key_pre_check : `None | FunctionType | MethodType`
        In case the deserialization is not key matched, this can be used to match the keys instead.
    change_deserializer : `GeneratorFunctionType`
        Change deserializers to use.
    change_serializer : `GeneratorFunctionType`
        Change serialiser to use.
    field_keys : `None | tuple<str>`
        The serialised name of the field.
    field_name : `str`
        The field's name.
    value_deserializer : `None | FunctionType | MethodType`
        Raw to processed value converter.
    value_merger : `None | FunctionType | MethodType`
        Merger to use to merge two entries.
    value_serializer : `None | FunctionType | MethodType`
        Processed to raw value converter.
    value_validator : `FunctionType | MethodType`
        Change value validator.
    """
    __slots__ = (
        'change_deserialization_key_pre_check', 'change_deserializer', 'change_serializer', 'field_keys', 'field_name',
        'value_deserializer', 'value_merger', 'value_serializer', 'value_validator'
    )
    
    def __new__(
        cls,
        field_keys,
        field_name,
        *,
        change_deserialization_key_pre_check = ...,
        change_deserializer = ...,
        change_serializer = ...,
        value_deserializer = ...,
        value_merger = ...,
        value_serializer = ...,
        value_validator = ...
    ):
        """
        Creates a new change conversion representation with the given fields.
        
        Parameters
        ----------
        field_keys : `None | tuple<str>`
            The serialised name of the field.
        field_name : `str`
            The field's name.
        change_deserializer  : `GeneratorFunctionType`, Optional (Keyword only)
            Deserializer to use.
        change_deserialization_key_pre_check : `FunctionType | MethodType`, Optional (Keyword only)
            In case the deserialization is not key matched, this can be used to match the keys instead.
        change_serializer : `GeneratorFunctionType`, Optional (Keyword only)
            Change serialiser to use.
        value_deserializer : `FunctionType | MethodType`, Optional (Keyword only)
            Raw to processed value converter.
        value_merger : `FunctionType | MethodType`, Optional (Keyword only)
            Merger to use to merge two entries.
        value_serializer : `FunctionType | MethodType`, Optional (Keyword only)
            Processed to raw value converter.
        value_validator : `FunctionType | MethodType`, Optional (Keyword only)
            Change value validator.
        """
        if change_deserialization_key_pre_check is ...:
            change_deserialization_key_pre_check = None
        
        if change_deserializer is ...:
            change_deserializer = change_deserializer_modification
        
        if change_serializer is ...:
            change_serializer = change_serializer_modification
        
        if value_deserializer is ...:
            value_deserializer = None
        
        if value_merger is ...:
            value_merger = None
        
        if value_serializer is ...:
            value_serializer = None
        
        if value_validator is ...:
            value_validator = None
        
        self = object.__new__(cls)
        self.change_deserializer = change_deserializer
        self.change_deserialization_key_pre_check = change_deserialization_key_pre_check
        self.change_serializer = change_serializer
        self.value_merger = value_merger
        self.field_keys = field_keys
        self.field_name = field_name
        self.value_deserializer = value_deserializer
        self.value_serializer = value_serializer
        self.value_validator = value_validator
        return self
    
    
    def __repr__(self):
        """Returns the change conversion's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # field_keys
        repr_parts.append(' field_keys = ')
        repr_parts.append(repr(self.field_keys))
        
        # field_name
        repr_parts.append(', field_name = ')
        repr_parts.append(repr(self.field_name))
        
        # change_deserializer
        change_deserializer = self.change_deserializer
        repr_parts.append(', change_deserializer = ')
        repr_parts.append(change_deserializer.__module__)
        repr_parts.append('.')
        repr_parts.append(change_deserializer.__name__)
        
        # change_serializer
        change_serializer = self.change_serializer
        repr_parts.append(', change_serializer = ')
        repr_parts.append(change_serializer.__module__)
        repr_parts.append('.')
        repr_parts.append(change_serializer.__name__)
        
        # change_deserialization_key_pre_check
        change_deserialization_key_pre_check = self.change_deserialization_key_pre_check
        change_deserialization_key_pre_check = self.value_merger
        if (change_deserialization_key_pre_check is not None):
            repr_parts.append(', change_deserialization_key_pre_check = ')
            repr_parts.append(change_deserialization_key_pre_check.__module__)
            repr_parts.append('.')
            repr_parts.append(change_deserialization_key_pre_check.__name__)
        
        # value_merger
        value_merger = self.value_merger
        if (value_merger is not None):
            repr_parts.append(', value_merger = ')
            repr_parts.append(value_merger.__module__)
            repr_parts.append('.')
            repr_parts.append(value_merger.__name__)
        
        
        # value_deserializer
        value_deserializer = self.value_deserializer
        if (value_deserializer is not None):
            repr_parts.append(', value_deserializer = ')
            repr_parts.append(value_deserializer.__module__)
            repr_parts.append('.')
            repr_parts.append(value_deserializer.__name__)
        
        # value_serializer
        value_serializer = self.value_serializer
        if (value_serializer is not None):
            repr_parts.append(', value_serializer = ')
            repr_parts.append(value_serializer.__module__)
            repr_parts.append('.')
            repr_parts.append(value_serializer.__name__)
        
        # value_validator
        value_validator = self.value_validator
        if (value_validator is not None):
            repr_parts.append(', value_validator = ')
            repr_parts.append(value_validator.__module__)
            repr_parts.append('.')
            repr_parts.append(value_validator.__name__)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the entry change conversion's hash value."""
        hash_value = 0
        
        # change_deserialization_key_pre_check
        hash_value ^= _hash_function(self.change_deserialization_key_pre_check)
        
        # change_deserializer
        hash_value ^= _hash_function(self.change_deserializer)
        
        # change_serializer
        hash_value ^= _hash_function(self.change_serializer)
        
        # field_keys
        field_keys = self.field_keys
        if (field_keys is not None):
            hash_value ^= hash(field_keys)
        
        # field_name
        hash_value ^= hash(self.field_name)
        
        # value_deserializer
        hash_value ^= _hash_function(self.value_deserializer)
        
        # value_merger
        hash_value ^= hash(self.value_merger)
        
        # value_serializer
        hash_value ^= _hash_function(self.value_serializer)
        
        # value_validator
        hash_value ^= _hash_function(self.value_validator)
        
        return hash_value
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # change_deserialization_key_pre_check
        if not _eq_functions(self.change_deserialization_key_pre_check, other.change_deserialization_key_pre_check):
            return False
        
        # change_deserializer
        if not _eq_functions(self.change_deserializer, other.change_deserializer):
            return False
        
        # change_serializer
        if not _eq_functions(self.change_serializer, other.change_serializer):
            return False
        
        # field_keys
        if self.field_keys != other.field_keys:
            return False
        
        # field_name
        if self.field_name != other.field_name:
            return False
        
        # value_deserializer
        if not _eq_functions(self.value_deserializer, other.value_deserializer):
            return False
        
        # value_merger
        if not _eq_functions(self.value_merger, other.value_merger):
            return False
        
        # value_serializer
        if not _eq_functions(self.value_serializer, other.value_serializer):
            return False
        
        # value_validator
        if not _eq_functions(self.value_validator, other.value_validator):
            return False
        
        return True
    
    
    def iter_field_keys(self):
        """
        Iterates over the field keys of the audit log change conversion.
        
        This method is an iterable generator.
        
        Yields
        ------
        field_key : `str`
        """
        field_keys = self.field_keys
        if (field_keys is not None):
            yield from field_keys
    
    
    def get_field_key(self, index):
        """
        Gets the field key at the given index.
        
        Parameters
        ----------
        index : `int`
            The index to get the field key at.
        
        Returns
        -------
        field_key : `None | str`
        """
        field_keys = self.field_keys
        if (field_keys is None):
            return None
        
        if index < 0 or index >= len(field_keys):
            return None
        
        return field_keys[index]
    
    
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
    
    
    def should_add_as_key_based_deserializer(self):
        """
        Whether the conversion should be added as a key based deserializer.
        
        Returns
        -------
        should_add_as_key_based_deserializer : `bool`
        """
        if self.field_keys is None:
            return False
        
        if self.change_deserialization_key_pre_check is not None:
            return False
        
        return True
    
    
    def should_add_as_key_pre_check_deserializer(self):
        """
        Whether the conversion should be added as a default deserializer.
        
        Returns
        -------
        should_add_as_key_pre_check_deserializer : `bool`
        """
        if self.change_deserialization_key_pre_check is None:
            return False
        
        return True
    
    
    def should_add_by_field_name(self):
        """
        Whether the conversion should be registered into a group based on its ``-field_name``.
        
        Returns
        -------
        should_add_by_field_name : `str`
        """
        if not self.field_name:
            return False
        
        return True
