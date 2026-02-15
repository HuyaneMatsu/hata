__all__ = ('CheckboxGroupOption',)

import reprlib

from scarletio import RichAttributeErrorBaseType

from ..shared_fields import (
    parse_default, parse_description, parse_label, parse_value, put_default, put_description, put_label, put_value,
    validate_default, validate_description, validate_label, validate_value
)


class CheckboxGroupOption(RichAttributeErrorBaseType):
    """
    An option of a checkbox group component.
    
    Attributes
    ----------
    default : `bool`
        Whether this option is the default one.
    
    description : `None`, `str`
        Description of the option.
    
    label : `str`
        Label of the option.
    
    value : `str`
        Identifier value of the option.
    """
    def __new__(cls, value, label = ..., default = ..., description = ...):
        """
        Creates a new checkbox group option with the given parameters.
        
        Parameters
        ----------
        value : `str`
            The option's value.
        
        label : `None | str`, Optional
            Label of the component option.
            
            Defaults to the `value` parameter if not given or if given as `None`.
        
        default : `bool`, Optional (Keyword only)
            Whether this the the default option. Defaults to `False`.
        
        description : `None`, `str`, Optional (Keyword only)
            Description of the component option.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        value = validate_value(value)
        
        # default
        if default is ...:
            default = False
        else:
            default = validate_default(default)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # label
        if label is ...:
            label = None
        else:
            label = validate_label(label)
        
        # Post validation
        if label is None:
            label = value
        
        # Construct
        self = object.__new__(cls)
        self.default = default
        self.description = description
        self.label = label
        self.value = value
        return self


    @classmethod
    def from_data(cls, data):
        """
        Creates a new checkbox group option from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            String select option data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        
        self.default = parse_default(data)
        self.description = parse_description(data)
        self.label = parse_label(data)
        self.value = parse_value(data)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the checkbox group option to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_default(self.default, data, defaults)
        put_description(self.description, data, defaults)
        put_label(self.label, data, defaults)
        put_value(self.value, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the checkbox group option's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # System fields : value
        
        # value
        repr_parts.append(', value = ')
        repr_parts.append(reprlib.repr(self.value))
        
        # Text fields : label
        
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
        """Returns whether the two checkbox group options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # default
        if self.default != other.default:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # label
        if self.label != other.label:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the checkbox group option's hash value."""
        hash_value = 0
        
        # default
        if self.default:
            hash_value ^= 1 << 8
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
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
        Copies the checkbox group option.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.default = self.default
        new.description = self.description
        new.label = self.label
        new.value = self.value
        return new
    
    
    def copy_with(
        self,
        default = ...,
        description = ...,
        label = ...,
        value = ...,
    ):
        """
        Copes the checkbox group with modifying it's defined attributes.
        
        Parameters
        ----------
        default : `bool`, Optional (Keyword only)
            Whether this the the default option. Defaults to `False`.
        
        description : `None`, `str`, Optional (Keyword only)
            Description of the component option.
        
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
        ValueError
            - If a parameter's value is incorrect.
        """
        # default
        if default is ...:
            default = self.default
        else:
            default = validate_default(default)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # label
        if label is ...:
            label = self.label
        else:
            label = validate_label(label)
        
        # value
        if value is ...:
            value = self.value
        else:
            value = validate_value(value)
        
        # Post validation
        if label is None:
            label = value
        
        # Construct
        new = object.__new__(type(self))
        new.default = default
        new.description = description
        new.label = label
        new.value = value
        return new
