__all__ = ('InteractionOption',)

import reprlib

from scarletio import RichAttributeErrorBaseType, export

from ...application_command import ApplicationCommandOptionType

from .fields import (
    parse_focused, parse_name, parse_options, parse_type, parse_value, put_focused_into, put_name_into,
    put_options_into, put_type_into, put_value_into, validate_focused, validate_name, validate_options, validate_type,
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
    
    
    def __new__(cls, **keyword_parameters):
        """
        Creates a new interaction option from the given keyword parameters.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which fields and how should be set.
        
        Other Parameters
        ----------------
        focused : `bool`, Optional (Keyword only)
            Whether this field is focused by the user.
        
        name : `str`, Optional (Keyword only)
            The option's name.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Nested options.
        
        type_ : ``ApplicationCommandOptionType``, Optional (Keyword only)
            The represented option's type.
        
        value : `None`, `str`, `float`, `int`, Optional (Keyword only)
            The value the user has been typed or selected.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        self = cls._create_empty()
        self._populate_from_keyword_parameters(keyword_parameters)
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
            options = tuple(option.copy() for option in options)
        new.options = options
        new.type = self.type
        new.value = self.value
        return new
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copies the interaction option with replacing the defined fields.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which fields and how should be set.
        
        Other Parameters
        ----------------
        focused : `bool`, Optional (Keyword only)
            Whether this field is focused by the user.
        
        name : `str`, Optional (Keyword only)
            The option's name.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Nested options.
        
        type_ : ``ApplicationCommandOptionType``, Optional (Keyword only)
            The represented option's type.
        
        value : `None`, `str`, `float`, `int`, Optional (Keyword only)
            The value the user has been typed or selected.
        
        Returns
        -------
        new : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        self = self.copy()
        self._populate_from_keyword_parameters(keyword_parameters)
        return self
    
    
    def _populate_from_keyword_parameters(self, keyword_parameters):
        """
        Sets the interaction option's attributes from the given keyword parameters.
        
        Parameters
        keyword_parameters : `dict` of (`str`, `object`) items
            A dictionary of keyword parameters defining which fields and how should be set.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        if not keyword_parameters:
            return
        
        # focused
        try:
            focused = keyword_parameters.pop('focused')
        except KeyError:
            pass
        else:
            self.focused = validate_focused(focused)
        
        # name
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            pass
        else:
            self.name = validate_name(name)
        
        # options
        try:
            options = keyword_parameters.pop('options')
        except KeyError:
            pass
        else:
            self.options = validate_options(options)
        
        # type
        try:
            type_ = keyword_parameters.pop('type_')
        except KeyError:
            pass
        else:
            self.type = validate_type(type_)
        
        # value
        try:
            value = keyword_parameters.pop('value')
        except KeyError:
            pass
        else:
            self.value = validate_value(value)
        
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new interaction option from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
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
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        put_focused_into(self.focused, data, defaults)
        put_name_into(self.name, data, defaults)
        put_options_into(self.options, data, defaults)
        put_type_into(self.type, data, defaults)
        put_value_into(self.value, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the interaction option's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' name=', repr(self.name),
        ]
        
        if self.focused:
            repr_parts.append(' (focused)')
        
        value = self.value
        if (value is not None):
            repr_parts.append(', value=')
            repr_parts.append(reprlib.repr(value))
        
        type_ = self.type
        repr_parts.append(', type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
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
