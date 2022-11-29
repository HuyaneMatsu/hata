__all__ = ('ComponentMetadataSelectBase', )

import reprlib

from scarletio import copy_docs

from ..shared_fields import parse_custom_id, put_custom_id_into, validate_custom_id
from ..shared_helpers import create_auto_custom_id

from .base import ComponentMetadataBase
from .constants import MAX_VALUES_DEFAULT, MIN_VALUES_DEFAULT
from .fields import (
    parse_enabled, parse_max_values, parse_min_values, parse_placeholder, put_enabled_into, put_max_values_into,
    put_min_values_into, put_placeholder_into, validate_enabled, validate_max_values, validate_min_values,
    validate_placeholder
)


class ComponentMetadataSelectBase(ComponentMetadataBase):
    """
    Base select component metadata.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        Custom identifier to detect which component was used by the user.
    
    enabled : `bool`
        Whether the component is enabled.
    
    max_values : `int
        The maximal amount of options to select.
    
    min_values : `int`
        The minimal amount of options to select.
    
    placeholder : `None`, `str`
        Placeholder text of the select.
    """
    __slots__ = ('custom_id', 'enabled', 'max_values', 'min_values', 'placeholder')
    
    @copy_docs(ComponentMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # enabled
        try:
            enabled = keyword_parameters.pop('enabled')
        except KeyError:
            enabled = True
        else:
            enabled = validate_enabled(enabled)
        
        # max_values
        try:
            max_values = keyword_parameters.pop('max_values')
        except KeyError:
            max_values = MAX_VALUES_DEFAULT
        else:
            max_values = validate_max_values(max_values)
        
        # min_values
        try:
            min_values = keyword_parameters.pop('min_values')
        except KeyError:
            min_values = MIN_VALUES_DEFAULT
        else:
            min_values = validate_min_values(min_values)
        
        # placeholder
        try:
            placeholder = keyword_parameters.pop('placeholder')
        except KeyError:
            placeholder = None
        else:
            placeholder = validate_placeholder(placeholder)
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.enabled = enabled
        self.max_values = max_values
        self.min_values = min_values
        self.placeholder = placeholder
        return self
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # System fields : custom_id
        
        # custom_id
        repr_parts.append(' custom_id = ')
        repr_parts.append(reprlib.repr(self.custom_id))
        
        # Type specific fields
        self._add_type_specific_repr_fields_into(repr_parts)
        
        # Text fields : placeholder
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            repr_parts.append(', placeholder = ')
            repr_parts.append(repr(placeholder))
        
        # Optional descriptive fields: min_values & max_values & enabled
        
        # min_values
        min_values = self.min_values
        if min_values != MIN_VALUES_DEFAULT:
            repr_parts.append(', min_values = ')
            repr_parts.append(repr(min_values))
        
        # max_values
        max_values = self.max_values
        if max_values != MAX_VALUES_DEFAULT:
            repr_parts.append(', max_values = ')
            repr_parts.append(repr(max_values))
        
        # enabled
        enabled = self.enabled
        if (not enabled):
            repr_parts.append(', enabled = ')
            repr_parts.append(repr(enabled))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _add_type_specific_repr_fields_into(self, repr_parts):
        """
        Adds type specific representation fields into the given list.
        
        Parameters
        ----------
        repr_parts : `list` of `str`
            Representation builder string to extend.
        """
        
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(self.custom_id)
        
        # enabled
        if self.enabled:
            hash_value ^= 1 << 8
        
        # max_values
        max_values = self.max_values
        if (max_values != 1):
            hash_value ^= (max_values << 18)
        
        # min_values
        min_values = self.min_values
        if (min_values != 1):
            min_values ^= (min_values << 22)
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            hash_value ^= hash(placeholder)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # enabled
        if self.enabled != other.enabled:
            return False
        
        # max_values
        if self.max_values != other.max_values:
            return False
        
        # min_values
        if self.min_values != other.min_values:
            return False
        
        # placeholder
        if self.placeholder != other.placeholder:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.custom_id = parse_custom_id(data)
        self.enabled = parse_enabled(data)
        self.max_values = parse_max_values(data)
        self.min_values = parse_min_values(data)
        self.placeholder = parse_placeholder(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data =  {}
        
        put_custom_id_into(self.custom_id, data, defaults)
        put_enabled_into(self.enabled, data, defaults)
        put_max_values_into(self.max_values, data, defaults)
        put_min_values_into(self.min_values, data, defaults)
        put_placeholder_into(self.placeholder, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # enabled
        new.enabled = self.enabled
        
        # placeholder
        new.placeholder = self.placeholder
        
        # max_values
        new.max_values = self.max_values
        
        # min_values
        new.min_values = self.min_values
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with)
    def copy_with(self, keyword_parameters):
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # enabled
        try:
            enabled = keyword_parameters.pop('enabled')
        except KeyError:
            enabled = self.enabled
        else:
            enabled = validate_enabled(enabled)
        
        # max_values
        try:
            max_values = keyword_parameters.pop('max_values')
        except KeyError:
            max_values = self.max_values
        else:
            max_values = validate_max_values(max_values)
        
        # min_values
        try:
            min_values = keyword_parameters.pop('min_values')
        except KeyError:
            min_values = self.min_values
        else:
            min_values = validate_min_values(min_values)
        
        # placeholder
        try:
            placeholder = keyword_parameters.pop('placeholder')
        except KeyError:
            placeholder = self.placeholder
        else:
            placeholder = validate_placeholder(placeholder)
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        
        new = object.__new__(type(self))
        new.custom_id = custom_id
        new.enabled = enabled
        new.max_values = max_values
        new.min_values = min_values
        new.placeholder = placeholder
        return new
