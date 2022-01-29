__all__ = ('ComponentSelectOption',)

import reprlib

from scarletio import copy_docs, export

from ...emoji import create_partial_emoji_data, create_partial_emoji_from_data

from .component_base import ComponentBase
from .debug import (
    _debug_component_default, _debug_component_description, _debug_component_emoji, _debug_component_label,
    _debug_component_select_option_value
)


@export
class ComponentSelectOption(ComponentBase):
    """
    An option of a select component.
    
    Attributes
    ----------
    default : `bool`
        Whether this option is the default one.
    description : `None`, `str`
        Description of the option.
    emoji : `None`, ``Emoji``
        Emoji on the option if applicable.
    label : `str`
        Label of the option.
    value : `str`
        Identifier value of the option.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.none`
        The component's type.
    custom_id : `NoneType` = `None`
        `custom_id` is not applicable for select options.
    """
    __slots__ = ('default', 'description', 'emoji', 'label', 'value')
    
    def __new__(cls, value, label, emoji=None, *, default=False, description=None):
        """
        Creates a new component option with the given parameters.
        
        Parameters
        ----------
        value : `str`
            The option's value.
        label : `str`
            Label of the component option.
        emoji : `None`, ``Emoji`` = `None`, Optional
            Emoji of the option if applicable.
        default : `bool` = `False`, Optional (Keyword only)
            Whether this the the default option. Defaults to `False`.
        description : `None`, `str` = `None`, Optional (Keyword only)
            Description of the component option.
        """
        if __debug__:
            _debug_component_default(default)
            _debug_component_description(description)
            _debug_component_emoji(emoji)
            _debug_component_label(label)
            _debug_component_select_option_value(value)
        
        # default
        # No additional checks
        
        # description
        if (description is not None) and (not description):
            description = None
        
        # emoji
        # No additional checks
        
        # label
        if __debug__:
            if (label is None) or (not label):
                raise AssertionError(
                    f'`label` cannot be empty.'
                )
        
        # value
        # No additional checks
        
        self = object.__new__(cls)
        self.default = default
        self.description = description
        self.emoji = emoji
        self.label = label
        self.value = value
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        # default
        self.default = data.get('default', False)
        
        # description
        self.description = data.get('description', None)
        
        # emoji
        emoji_data = data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        self.emoji = emoji
        
        # label
        self.label = data['label']
        
        # value
        self.value = data['value']
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        # label & value
        data = {
            'label': self.label,
            'value': self.value,
        }
        
        # default
        if self.default:
            data['default'] = True
        
        # description
        description = self.description
        if (description is not None):
            data['description'] = description
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            data['emoji'] = create_partial_emoji_data(emoji)
        
        return data


    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # System fields : value
        
        # value
        repr_parts.append(', value=')
        repr_parts.append(reprlib.repr(self.value))
        
        # Text fields : emoji & label
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji=')
            repr_parts.append(repr(emoji))
        
        # label
        label = self.label
        if (label is not None):
            repr_parts.append(', label=')
            repr_parts.append(reprlib.repr(label))
        
        # Optional descriptive fields: description & default
        
        # description
        description = self.description
        if (description is not None):
            repr_parts.append(', description=')
            repr_parts.append(reprlib.repr(description))
        
        # default
        if self.default:
            repr_parts.append(', default=True')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.default = self.default
        new.description = self.description
        new.emoji = self.emoji
        new.label = self.label
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
        default : `bool`
            Whether this the the default option. Defaults to `False`.
        description : `None`, `str`, Optional (Keyword only)
            Description of the component option.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            Emoji of the option if applicable.
        label : `str`, Optional (Keyword only)
            Label of the component option.
        value : `str`, Optional (Keyword only)
            The option's value.
        
        Returns
        -------
        new : ``ComponentSelectOption``
        """
        # default
        try:
            default = kwargs.pop('default')
        except KeyError:
            default = self.default
        else:
            if __debug__:
                _debug_component_default(default)
        
        # description
        try:
            description = kwargs.pop('description')
        except KeyError:
            description = self.description
        else:
            if __debug__:
                _debug_component_description(description)
            
            if (description is not None) and (not description):
                description = None
        
        # emoji
        try:
            emoji = kwargs.pop('emoji')
        except KeyError:
            emoji = self.emoji
        else:
            if __debug__:
                _debug_component_emoji(emoji)
        
        
        # label
        try:
            label = kwargs.pop('label')
        except KeyError:
            label = self.label
        else:
            if __debug__:
                _debug_component_label(label)
                
                if (label is None) or (not label):
                    raise AssertionError(
                        f'`label` cannot be empty.'
                    )
        
        # value
        try:
            value = kwargs.pop('value')
        except KeyError:
            value = self.value
        else:
            if __debug__:
                _debug_component_select_option_value(value)
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        new = object.__new__(type(self))
        new.default = default
        new.description = description
        new.emoji = emoji
        new.label = label
        new.value = value
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # default
        if self.default != other.default:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        # label
        if self.label != other.label:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # default
        if self.default:
            hash_value ^= 1 << 8
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= emoji.id
        
        # label
        label = self.label
        if (label is not None):
            hash_value ^= hash(label)
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
