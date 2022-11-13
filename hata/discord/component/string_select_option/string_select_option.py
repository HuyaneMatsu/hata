__all__ = ('StringSelectOption',)

import reprlib

from scarletio import RichAttributeErrorBaseType

from ..shared_fields import parse_emoji, put_emoji_into, validate_emoji

from .fields import (
    parse_default, parse_description, parse_label, parse_value, put_default_into, put_description_into, put_label_into,
    put_value_into, validate_default, validate_description, validate_label, validate_value
)


class StringSelectOption(RichAttributeErrorBaseType):
    """
    An option of a string select component.
    
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
    """
    def __new__(cls, value, label = None, emoji = None, *, default = False, description = None):
        """
        Creates a new component option with the given parameters.
        
        Parameters
        ----------
        value : `str`
            The option's value.
        
        label : `str` = `None`, Optional
            Label of the component option.
            
            Defaults to the `value` parameter if not given.
        
        emoji : `None`, ``Emoji`` = `None`, Optional
            Emoji of the option if applicable.
        
        default : `bool` = `False`, Optional (Keyword only)
            Whether this the the default option. Defaults to `False`.
        
        description : `None`, `str` = `None`, Optional (Keyword only)
            Description of the component option.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        default = validate_default(default)
        description = validate_description(description)
        emoji = validate_emoji(emoji)
        label = validate_label(label)
        value = validate_value(value)
        
        if label is None:
            label = value
        
        self = object.__new__(cls)
        self.default = default
        self.description = description
        self.emoji = emoji
        self.label = label
        self.value = value
        return self


    @classmethod
    def from_data(cls, data):
        """
        Creates a new string select option from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            String select option data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        
        self.default = parse_default(data)
        self.description = parse_description(data)
        self.emoji = parse_emoji(data)
        self.label = parse_label(data)
        self.value = parse_value(data)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the string select option to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
        """
        data = {}
        
        put_default_into(self.default, data, defaults)
        put_description_into(self.description, data, defaults)
        put_emoji_into(self.emoji, data, defaults)
        put_label_into(self.label, data, defaults)
        put_value_into(self.value, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the string select option's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # System fields : value
        
        # value
        repr_parts.append(', value = ')
        repr_parts.append(reprlib.repr(self.value))
        
        # Text fields : emoji & label
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji = ')
            repr_parts.append(repr(emoji))
        
        # label
        label = self.label
        if (label is not None):
            repr_parts.append(', label = ')
            repr_parts.append(reprlib.repr(label))
        
        # Optional descriptive fields: description & default
        
        # description
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(reprlib.repr(description))
        
        # default
        if self.default:
            repr_parts.append(', default = True')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two string select options are equal."""
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
    
    
    def __hash__(self):
        """Returns the string select option's hash value."""
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
    
    
    def copy(self):
        """
        Copies the string select option.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.default = self.default
        new.description = self.description
        new.emoji = self.emoji
        new.label = self.label
        new.value = self.value
        return new
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copes the string select with modifying it's defined attributes.
        
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which attribute should be overwritten.
        
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
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        # default
        try:
            default = keyword_parameters.pop('default')
        except KeyError:
            default = self.default
        else:
            default = validate_default(default)
        
        # description
        try:
            description = keyword_parameters.pop('description')
        except KeyError:
            description = self.description
        else:
            description = validate_description(description)
        
        # emoji
        try:
            emoji = keyword_parameters.pop('emoji')
        except KeyError:
            emoji = self.emoji
        else:
           emoji = validate_emoji(emoji)
        
        
        # label
        try:
            label = keyword_parameters.pop('label')
        except KeyError:
            label = self.label
        else:
            label = validate_label(label)
        
        # value
        try:
            value = keyword_parameters.pop('value')
        except KeyError:
            value = self.value
        else:
            value = validate_value(value)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        if label is None:
            label = value
        
        new = object.__new__(type(self))
        new.default = default
        new.description = description
        new.emoji = emoji
        new.label = label
        new.value = value
        return new
