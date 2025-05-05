__all__ = ('InteractionOption',)

import reprlib

from scarletio import RichAttributeErrorBaseType, export

from ...application_command import ApplicationCommandOptionType

from .fields import (
    parse_focused, parse_name, parse_options, parse_type, parse_value, put_focused, put_name,
    put_options, put_type, put_value, validate_focused, validate_name, validate_options, validate_type,
    validate_value
)


@export
class InteractionOption(RichAttributeErrorBaseType):
    """
    Integration option representing a parameter or a sub-command-group.
    
    Attributes
    ----------
    focused : `bool`
        Whether this field is focused by the user. This field is applicable for auto complete options.
    
    name : `str`
        The option's name.
    
    options : `None`, `tuple` of ``InteractionOption``
        Nested options.
    
    type : ``ApplicationCommandOptionType``
        The represented option's type.
    
    value : `None`, `str`, `float`, `int`
        The value the user has been typed or selected.
    """
    __slots__ = ('focused', 'name', 'options', 'type', 'value')
    
    
    def __new__(
        cls,
        *,
        focused = ...,
        name = ...,
        option_type = ...,
        options = ...,
        value = ...,
    ):
        """
        Creates a new interaction option from the given keyword parameters.
        
        Parameters
        ----------
        focused : `bool`, Optional (Keyword only)
            Whether this field is focused by the user.
        
        name : `str`, Optional (Keyword only)
            The option's name.
        
        option_type : ``ApplicationCommandOptionType``, `int`, Optional (Keyword only)
            The represented option's type.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Nested options.
        
        value : `None`, `str`, `float`, `int`, Optional (Keyword only)
            The value the user has been typed or selected.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # focused
        if focused is ...:
            focused = False
        else:
            focused = validate_focused(focused)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # option_type
        if option_type is ...:
            option_type = ApplicationCommandOptionType.none
        else:
            option_type = validate_type(option_type)
        
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # value
        if value is ...:
            value = None
        else:
            value = validate_value(value)
        
        
        # Construct
        self = object.__new__(cls)
        self.focused = focused
        self.name = name
        self.options = options
        self.type = option_type
        self.value = value
        return self
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an interaction option with it's default values set.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.focused = False
        self.name = ''
        self.options = None
        self.type = ApplicationCommandOptionType.none
        self.value = None
        return self
    
    
    def copy(self):
        """
        Copies the interaction option.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        new.focused = self.focused
        new.name = self.name
        options = self.options
        if (options is not None):
            options = (*(option.copy() for option in options),)
        new.options = options
        new.type = self.type
        new.value = self.value
        return new
    
    
    def copy_with(
        self,
        *,
        focused = ...,
        name = ...,
        option_type = ...,
        options = ...,
        value = ...,
    ):
        """
        Copies the interaction option with replacing the defined fields.
        
        Parameters
        ----------
        focused : `bool`, Optional (Keyword only)
            Whether this field is focused by the user.
        
        name : `str`, Optional (Keyword only)
            The option's name.
        
        option_type : ``ApplicationCommandOptionType``, `int`, Optional (Keyword only)
            The represented option's type.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Nested options.
        
        value : `None`, `str`, `float`, `int`, Optional (Keyword only)
            The value the user has been typed or selected.
        
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
        # focused
        if focused is ...:
            focused = self.focused
        else:
            focused = validate_focused(focused)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # option_type
        if option_type is ...:
            option_type = self.type
        else:
            option_type = validate_type(option_type)
        
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = (*(option.copy() for option in options),)
        else:
            options = validate_options(options)
        
        # value
        if value is ...:
            value = self.value
        else:
            value = validate_value(value)
        
        
        # Construct
        new = object.__new__(type(self))
        new.focused = focused
        new.name = name
        new.options = options
        new.type = option_type
        new.value = value
        return new
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new interaction option from the data received from Discord.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Interaction option data.
        """
        self = object.__new__(cls)
        self.focused = parse_focused(data)
        self.name = parse_name(data)
        self.options = parse_options(data)
        self.type = parse_type(data)
        self.value = parse_value(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the interaction option into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_focused(self.focused, data, defaults)
        put_name(self.name, data, defaults)
        put_options(self.options, data, defaults)
        put_type(self.type, data, defaults)
        put_value(self.value, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the interaction option's representation."""
        repr_parts = ['<', type(self).__name__,]
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # focused
        focused = self.focused
        if focused:
            repr_parts.append(', focused = ')
            repr_parts.append(repr(focused))
        
        # value
        value = self.value
        if (value is not None):
            repr_parts.append(', value = ')
            repr_parts.append(reprlib.repr(value))
        
        # type
        option_type = self.type
        repr_parts.append(', type = ')
        repr_parts.append(option_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(option_type.value))
        
        # options
        options = self.options
        if (options is not None):
            repr_parts.append(', options = [')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the interaction option's hash value."""
        hash_value = 0
        
        # focused
        hash_value ^= (self.focused << 16)
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options) << 8)
            
            for option in options:
                hash_value ^= hash(option)
        
        # type
        hash_value ^= self.type.value
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two interaction option's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # focused
        if self.focused != other.focused:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    def iter_options(self):
        """
        Iterates over the sub-options of the interaction option.
        
        This method is an iterable generator.
        
        Yields
        ------
        option : ``InteractionOption``
        """
        options = self.options
        if options is not None:
            yield from options
    
    
    @property
    def focused_option(self):
        """
        Returns the focused option of the interaction option.
        
        Returns
        -------
        option : `None`, `instance<cls>`
        """
        if self.focused:
            return self
        
        for option in self.iter_options():
            focused_option =  option.focused_option
            if (focused_option is not None):
                return focused_option
    
    
    def _iter_non_focused_values(self):
        """
        Iterates over the non focused values of the interaction option.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
            The option's name.
        value : `None`, `str`
            The option's value.
        """
        type_ = self.type
        if (
            (type_ is ApplicationCommandOptionType.sub_command) or
            (type_ is ApplicationCommandOptionType.sub_command_group)
        ):
            for option in self.iter_options():
                yield from option._iter_non_focused_values()
        else:
            if not self.focused:
                yield self.name, self.value
    
    
    def get_value_of(self, *option_names):
        """
        Gets the value for the option by the given name stack.
        
        Parameters
        ----------
        *option_names : `str`
            The option(s)'s name.
        
        Returns
        -------
        value : `None`, `str`
            The value, the user has been typed.
        """
        if option_names:
            option_name, *option_names = option_names
            
            for option in self.iter_options():
                if option.name == option_name:
                    value = option.get_value_of(*option_names)
                    break
            else:
                value = None
        else:
            value = self.value
        
        return value
