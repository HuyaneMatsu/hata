__all__ = ('ComponentTextInput',)

import reprlib

from scarletio import copy_docs, include

from ...preconverters import preconvert_preinstanced_type

from .component_base import ComponentBase
from .debug import (
    _debug_component_custom_id, _debug_component_label, _debug_component_max_length, _debug_component_min_length,
    _debug_component_placeholder, _debug_component_required, _debug_component_text_input_value
)
from .preinstanced import ComponentType, TextInputStyle


create_auto_custom_id = include('create_auto_custom_id')

class ComponentTextInput(ComponentBase):
    """
    Text input component.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        Custom identifier to detect which text input was clicked by the user.
    
    label : `None`, `str`
        Label of the component.
    
    max_length : `int`
        The maximal length of the inputted text.
        
        Defaults to `0` if not applicable.
        
    min_length : `int`
        The minimal length of the inputted text.
        
        Defaults to `0` if not applicable.
    
    placeholder : `str`
        Placeholder text of the text input.
    
    required : `bool`
        Whether the field is required to be fulfilled.
    
    style : `None`, ``TextInputStyle``
        The text input's style.
    
    value : `None`, `str`
        The text input's default value.
    
    Class Attributes
    ----------------
    default_style : ``TextInputStyle`` = `TextInputStyle.short`
        The default text input style to use if style is not given.
    type : ``ComponentType`` = `ComponentType.text_input`
        The component's type.
    """
    default_style = TextInputStyle.short
    type = ComponentType.text_input
    
    __slots__ = (
        'custom_id', 'label', 'max_length', 'min_length', 'placeholder', 'required', 'style', 'value'
    )
    
    def __new__(cls, label=None, *, custom_id=None, max_length=0, min_length=0, placeholder=None, required=None,
            style=None, value=None):
        """
        Creates a new component instance with the given parameters.
        
        Parameters
        ----------
        label : `None`, `str` = `None`, Optional
            Label of the component.
        
        custom_id : `None`, `str` = `None`, Optional (Keyword only)
            Custom identifier to detect which text input was clicked by the user.
        
        max_length : `int` = `0`, Optional (Keyword only)
            The maximal length of the inputted text.
            
            Defaults to `0` if not applicable.
        
        min_length : `int` = `0`, Optional (Keyword only)
            The minimal length of the inputted text.
            
            Defaults to `0` if not applicable.
        
        placeholder : `None`, `str` = `None`, Optional (Keyword only)
            Placeholder text of the select.
        
        required : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
            
            If not given, or given as `None`, will default to `True` if `min_length` is defined as higher than `0`.
        
        style : `None`, ``TextInputStyle``, `int` = `None`, Optional (Keyword only)
            The text input's style.
        
        value : `None`, `str` = `None`, Optional (Keyword only)
            The text input's default value.
        
        Raises
        ------
        TypeError
            If `style`'s type is unexpected.
        AssertionError
            - If `custom_id` was not given neither as `None`, `str`.
            - If `style` was not given as any of the `type`'s expected styles.
            - If `label` was not given neither as `None` nor as `int`.
            - If `label`'s length is over `80`.
            - If `custom_id`'s length is over `100`.
            - If `max_length` was not given as `int`.
            - If `man_length`'s is out of the expected range.
            - If `min_length` was not given as `int`.
            - If `min_length`'s is out of the expected range.
            - If `required` is neither `None` nor `bool`.
            - If `value` is neither `None` nor `bool`.
        """
        if __debug__:
            _debug_component_custom_id(custom_id)
            _debug_component_label(label)
            _debug_component_max_length(max_length)
            _debug_component_min_length(min_length)
            _debug_component_placeholder(placeholder)
            _debug_component_required(required)
            _debug_component_text_input_value(value)
        
        # custom_id
        if (custom_id is None) or (not custom_id):
            custom_id = create_auto_custom_id()
        
        # label
        if (label is not None) and (not label):
            label = None
        
        # max_length
        # No additional checks
        
        # min_length
        # No additional checks
        
        # placeholder
        if (placeholder is not None) and (not placeholder):
            placeholder = None
        
        # required
        # If required is `None`, we detect it from `min_value`.
        if (required is None):
            if min_length > 0:
                required = True
            else:
                required = False
        
        # style
        if style is None:
            style = cls.default_style
        else:
            style = preconvert_preinstanced_type(style, 'style', TextInputStyle)

        # value
        if (value is not None) and (not value):
            value = None
        
        self = object.__new__(cls)
        
        self.custom_id = custom_id
        self.label = label
        self.max_length = max_length
        self.min_length = min_length
        self.placeholder = placeholder
        self.required = required
        self.style = style
        self.value = value
        
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        # custom_id
        self.custom_id = data.get('custom_id', None)
        
        # label
        self.label = data.get('label', None)
        
        # max_length
        self.max_length = data.get('max_length', 0)
        
        # min_length
        self.min_length = data.get('min_length', 0)
        
        # placeholder
        placeholder = data.get('placeholder', None)
        if (placeholder is not None) and (not placeholder):
            placeholder = None
        self.placeholder = placeholder
        
        # required
        self.required = data.get('required', True)
        
        # style
        style = data.get('style', None)
        if (style is not None):
            style = TextInputStyle.get(style)
        self.style = style
        
        # value
        value = data['value']
        if (value is not None) and (not value):
            value = None
        self.value = value
        
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        # type
        data = {
            'type': self.type.value,
        }
        
        #  custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            data['custom_id'] = custom_id
        
        # label
        label = self.label
        if (label is not None):
            data['label'] = label
        
        # max_length
        max_length = self.max_length
        if max_length:
            data['max_length'] = max_length
        
        # min_length
        min_length = self.min_length
        if min_length:
            data['min_length'] = min_length
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            data['placeholder'] = placeholder
        
        # required
        if (not self.required):
            data['required'] = False
        
        # style
        style = self.style
        if (style is not None):
            data['style'] = style.value
        
        # value
        value = self.value
        if (value is not None):
            data['value'] = value
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields : type & style
        
        # type
        type_ = self.type
        repr_parts.append(' type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        # style
        style = self.style
        repr_parts.append(', style=')
        repr_parts.append(style.name)
        repr_parts.append(' (')
        repr_parts.append(repr(style.value))
        repr_parts.append(')')
        
        # System fields : custom_id
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id=')
            repr_parts.append(reprlib.repr(custom_id))
        
        # Text fields : label & placeholder & value
        
        # label
        label = self.label
        if (label is not None):
            repr_parts.append(', label=')
            repr_parts.append(reprlib.repr(label))
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            repr_parts.append(', placeholder=')
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
            repr_parts.append(', min_length=')
            repr_parts.append(repr(min_length))
        
        # min_length
        max_length = self.max_length
        if max_length:
            repr_parts.append(', max_length=')
            repr_parts.append(repr(max_length))
        
        # required (relation with `min_length`)
        required = self.required
        if (min_length > 0) ^ required:
            repr_parts.append(', required=')
            repr_parts.append(repr(required))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.custom_id = self.custom_id
        new.label = self.label
        new.max_length = self.max_length
        new.min_length = self.min_length
        new.placeholder = self.placeholder
        new.required = self.required
        new.style = self.style
        new.value = self.value
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which text input was clicked by the user.
        
        label : `None`, `str`, Optional (Keyword only)
            Label of the component.
        
        max_length : `int`, Optional (Keyword only)
            The maximal length of the inputted text.
        
        min_length : `int`, Optional (Keyword only)
            The minimal length of the inputted text.
        
        placeholder : `None`, `str`, Optional (Keyword only)
            Placeholder text of the select.
        
        required : `None`, `bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
            
            If not given, or given as `None`, will default to `True` if `min_length` is defined as higher than `0`.
        
        style : `None`, ``TextInputStyle``, `int`, Optional (Keyword only)
            The text input's style.
        
        value : `None`, `str`, Optional (Keyword only)
            The text input's default value.
        
        Returns
        -------
        new : ``ComponentTextInput``
        """
        # custom_id
        try:
            custom_id = kwargs.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            if __debug__:
                _debug_component_custom_id(custom_id)
            
            if (custom_id is not None) and (not custom_id):
                custom_id = None
        
        if (custom_id is None):
            custom_id = create_auto_custom_id()
        
        # label
        try:
            label = kwargs.pop('label')
        except KeyError:
            label = self.label
        else:
            if __debug__:
                _debug_component_label(label)
        
        # max_length
        try:
            max_length = kwargs.pop('max_length')
        except KeyError:
            max_length = self.max_length
        else:
            if __debug__:
                _debug_component_max_length(max_length)
        
        # min_length
        try:
            min_length = kwargs.pop('min_length')
        except KeyError:
            min_length = self.min_length
        else:
            if __debug__:
                _debug_component_min_length(min_length)
        
        # placeholder
        try:
            placeholder = kwargs.pop('placeholder')
        except KeyError:
            placeholder = self.placeholder
        else:
            if __debug__:
                _debug_component_placeholder(placeholder)
            
            if (placeholder is not None) and (not placeholder):
                placeholder = None
        
        # required
        try:
            required = kwargs.pop('required')
        except KeyError:
            required = self.required
        else:
            if __debug__:
                _debug_component_required(required)
            
            if (required is None):
                if min_length > 0:
                    required = True
                else:
                    required = False
        
        # style
        try:
            style = kwargs.pop('style')
        except KeyError:
            style = self.style
        
        if style is None:
            style = self.default_style
        else:
            style = preconvert_preinstanced_type(style, 'style', TextInputStyle)
        
        # value
        try:
            value = kwargs.pop('value')
        except KeyError:
            value = None
        else:
            if __debug__:
                _debug_component_text_input_value(value)
            
            if (value is not None) and (not value):
                value = None
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        new = object.__new__(type(self))
        
        new.custom_id = custom_id
        new.label = label
        new.max_length = max_length
        new.min_length = min_length
        new.placeholder = placeholder
        new.required = required
        new.style = style
        new.value = value
        
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
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
        
        # style
        if self.style is not other.style:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        # type
        hash_value = self.type.value
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # label
        label = self.label
        if (label is not None):
            hash_value ^= hash(label)
        
        # max_length
        max_length = self.max_length
        if max_length:
            hash_value ^= max_length << 12
        
        # min_length
        min_length = self.min_length
        if min_length:
            hash_value ^= min_length << 20
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            hash_value ^= hash(placeholder)
        
        # required
        if self.required:
            hash_value ^= (1 << 28)
        
        # style
        style = self.style
        if (style is not None):
            hash_value ^= style.value
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
