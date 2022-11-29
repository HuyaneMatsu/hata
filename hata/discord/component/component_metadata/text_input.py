__all__ = ('ComponentMetadataTextInput',)

import reprlib, warnings

from scarletio import copy_docs

from ..shared_fields import parse_custom_id, put_custom_id_into, validate_custom_id

from .base import ComponentMetadataBase
from .constants import MAX_LENGTH_DEFAULT, MIN_LENGTH_DEFAULT, TEXT_INPUT_STYLE_DEFAULT
from .fields import (
    parse_label, parse_max_length, parse_min_length, parse_placeholder, parse_required, parse_text_input_style,
    parse_value, put_label_into, put_max_length_into, put_min_length_into, put_placeholder_into, put_required_into,
    put_text_input_style_into, put_value_into, validate_label, validate_max_length, validate_min_length,
    validate_placeholder, validate_required, validate_text_input_style, validate_value
)


class ComponentMetadataTextInput(ComponentMetadataBase):
    """
    String select component metadata.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        Custom identifier to detect which component was used by the user.
    
    label : `None`, `str`
        Label of the component.
    
    max_length : `int
        The minimal length of the inputted text.
    
    min_length : `int`
        The minimal amount of options to select.
    
    placeholder : `None`, `str`
        Placeholder text of the select.
    
    required : `bool`
        Whether the field is required to be fulfilled.
    
    text_input_style : ``TextInputStyle``
        The text input's style.
    
    value : `None`, `str`
        The text input's default value.
    """
    __slots__ = (
        'custom_id', 'label', 'max_length', 'min_length', 'placeholder', 'required', 'text_input_style', 'value'
    )
    
    @copy_docs(ComponentMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # label
        try:
            label = keyword_parameters.pop('label')
        except KeyError:
            label = None
        else:
            label = validate_label(label)
        
        # max_length
        try:
            max_length = keyword_parameters.pop('max_length')
        except KeyError:
            max_length = MAX_LENGTH_DEFAULT
        else:
            max_length = validate_max_length(max_length)
        
        # min_length
        try:
            min_length = keyword_parameters.pop('min_length')
        except KeyError:
            min_length = MIN_LENGTH_DEFAULT
        else:
            min_length = validate_min_length(min_length)
        
        # placeholder
        try:
            placeholder = keyword_parameters.pop('placeholder')
        except KeyError:
            placeholder = None
        else:
            placeholder = validate_placeholder(placeholder)
        
        # required
        try:
            required = keyword_parameters.pop('required')
        except KeyError:
            required = None
        else:
            if (required is not None):
                required = validate_required(required)
        
        # text_input_style
        try:
            text_input_style = keyword_parameters.pop('text_input_style')
        except KeyError:
            text_input_style = TEXT_INPUT_STYLE_DEFAULT
        else:
            text_input_style = validate_text_input_style(text_input_style)
        
        # value
        try:
            value = keyword_parameters.pop('value')
        except KeyError:
            value = None
        else:
            value = validate_value(value)
        
        # Auto detect required if not-given / None
        
        if (required is None):
            if min_length > 0:
                required = True
            else:
                required = False
        
        # Extra checks
        
        if text_input_style is text_input_style.none:
            text_input_style = TEXT_INPUT_STYLE_DEFAULT
        
        # Construct
        
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.label = label
        self.max_length = max_length
        self.min_length = min_length
        self.placeholder = placeholder
        self.required = required
        self.text_input_style = text_input_style
        self.value = value
        return self
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # text_input_style
        text_input_style = self.text_input_style
        repr_parts.append(' text_input_style = ')
        repr_parts.append(text_input_style.name)
        repr_parts.append(' (')
        repr_parts.append(repr(text_input_style.value))
        repr_parts.append(')')
        
        # System fields : custom_id
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id = ')
            repr_parts.append(reprlib.repr(custom_id))
        
        # Text fields : label & placeholder & value
        
        # label
        label = self.label
        if (label is not None):
            repr_parts.append(', label = ')
            repr_parts.append(reprlib.repr(label))
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            repr_parts.append(', placeholder = ')
            repr_parts.append(repr(placeholder))
        
        # value
        value = self.value
        if (value is not None):
            repr_parts.append(', value=')
            repr_parts.append(repr(value))
        
        # Optional descriptive fields : max_length & min_length & required
        
        # min_length
        min_length = self.min_length
        if min_length:
            repr_parts.append(', min_length = ')
            repr_parts.append(repr(min_length))
        
        # min_length
        max_length = self.max_length
        if max_length:
            repr_parts.append(', max_length = ')
            repr_parts.append(repr(max_length))
        
        # required (relation with `min_length`)
        required = self.required
        if (min_length > 0) ^ required:
            repr_parts.append(', required = ')
            repr_parts.append(repr(required))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(self.custom_id)
        
        # label
        label = self.label
        if (label is not None):
            hash_value ^= hash(label)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 12
            for option in options:
                hash_value ^= hash(option)
        
        # max_length
        max_length = self.max_length
        if (max_length != 1):
            hash_value ^= (max_length << 18)
        
        # min_length
        min_length = self.min_length
        if (min_length != 1):
            min_length ^= (min_length << 22)
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None) and (placeholder != label):
            hash_value ^= hash(placeholder)
        
        # required
        if self.required:
            hash_value ^= (1 << 28)
        
        # text_input_style
        text_input_style = self.text_input_style
        if (text_input_style is not None):
            hash_value ^= text_input_style.value
        
        # value
        value = self.value
        if (value is not None) and (value != label) and (value != placeholder):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # label
        if self.label != other.label:
            return False
        
        # max_length
        if self.max_length != other.max_length:
            return False
        
        # min_length
        if self.min_length != other.min_length:
            return False
        
        # placeholder
        if self.placeholder != other.placeholder:
            return False
        
        # required
        if self.required != other.required:
            return False
        
        # text_input_style
        if self.text_input_style is not other.text_input_style:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.custom_id = parse_custom_id(data)
        self.label = parse_label(data)
        self.max_length = parse_max_length(data)
        self.min_length = parse_min_length(data)
        self.placeholder = parse_placeholder(data)
        self.required = parse_required(data)
        self.text_input_style = parse_text_input_style(data)
        self.value = parse_value(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data =  {}
        
        put_custom_id_into(self.custom_id, data, defaults)
        put_label_into(self.label, data, defaults)
        put_max_length_into(self.max_length, data, defaults)
        put_min_length_into(self.min_length, data, defaults)
        put_placeholder_into(self.placeholder, data, defaults)
        put_required_into(self.required, data, defaults)
        put_text_input_style_into(self.text_input_style, data, defaults)
        put_value_into(self.value, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.custom_id = self.custom_id
        new.label = self.label
        new.max_length = self.max_length
        new.min_length = self.min_length
        new.placeholder = self.placeholder
        new.required = self.required
        new.text_input_style = self.text_input_style
        new.value = self.value
        
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
        
        # label
        try:
            label = keyword_parameters.pop('label')
        except KeyError:
            label = self.label
        else:
            label = validate_label(label)
        
        # max_length
        try:
            max_length = keyword_parameters.pop('max_length')
        except KeyError:
            max_length = self.max_length
        else:
            max_length = validate_max_length(max_length)
        
        # min_length
        try:
            min_length = keyword_parameters.pop('min_length')
        except KeyError:
            min_length = self.min_length
        else:
            min_length = validate_min_length(min_length)
        
        # placeholder
        try:
            placeholder = keyword_parameters.pop('placeholder')
        except KeyError:
            placeholder = self.placeholder
        else:
            placeholder = validate_placeholder(placeholder)
        
        # required
        try:
            required = keyword_parameters.pop('required')
        except KeyError:
            required = self.required
        else:
            required = validate_required(required)
        
        # text_input_style
        try:
            text_input_style = keyword_parameters.pop('text_input_style')
        except KeyError:
            text_input_style = self.text_input_style
        else:
            text_input_style = validate_text_input_style(text_input_style)

        # value
        try:
            value = keyword_parameters.pop('value')
        except KeyError:
            value = self.value
        else:
            value = validate_value(value)
        
        # Deprecated: style
        
        try:
            style = keyword_parameters.pop('style')
        except KeyError:
            pass
        else:
            warnings.warn(
                (
                    '`style` parameter of components is deprecated and will be removed in 2023 February. '
                    'Please use `text_input_style` for text input components.'
                ),
                FutureWarning,
                stacklevel = 3,
            )
            
            text_input_style = validate_text_input_style(style)
        
        # Extra checks
        
        if text_input_style is text_input_style.none:
            text_input_style = TEXT_INPUT_STYLE_DEFAULT
        
        # Construct
        
        new = object.__new__(type(self))
        new.custom_id = custom_id
        new.label = label
        new.max_length = max_length
        new.min_length = min_length
        new.placeholder = placeholder
        new.required = required
        new.text_input_style = text_input_style
        new.value = value
        return new
