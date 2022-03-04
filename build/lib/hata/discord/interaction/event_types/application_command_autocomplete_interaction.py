__all__ = ('ApplicationCommandAutocompleteInteraction', 'ApplicationCommandAutocompleteInteractionOption')

import reprlib

from scarletio import copy_docs

from ..preinstanced import ApplicationCommandOptionType

from .interaction_field_base import InteractionFieldBase


class ApplicationCommandAutocompleteInteraction(InteractionFieldBase):
    """
    Represents an ``ApplicationCommand``'s auto completion interaction.
    
    Attributes
    ----------
    id : `int`
        The represented application command's identifier number.
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None`, `tuple` of ``ApplicationCommandAutocompleteOption``
        Parameter auto completion options.
    """
    __slots__ = ('id', 'name', 'options',)
    
    @copy_docs(InteractionFieldBase.__new__)
    def __new__(cls, data, interaction_event):
        # id
        id_ = int(data['id'])
        
        # name
        name = data['name']
        
        # options
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(
                ApplicationCommandAutocompleteInteractionOption(option_data) for option_data in option_datas
            )
        
        self = object.__new__(cls)
        
        self.id = id_
        self.name = name
        self.options = options
        
        return self
    
    
    @copy_docs(InteractionFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id),
            ', name=', repr(self.name),
        ]
        
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
    
    
    @copy_docs(InteractionFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options) << 8)
            
            for option in options:
                hash_value ^= hash(option)
        
        return hash_value
    
    
    @copy_docs(InteractionFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        return True
        
    
    @property
    def focused_option(self):
        """
        Returns the focused option of the application command autocomplete interaction.
        
        Returns
        -------
        option : `None`, ``ApplicationCommandAutocompleteInteractionOption``
        """
        options = self.options
        if options is None:
            focused_option = None
        else:
            for option in options:
                focused_option = option.focused_option
                if (focused_option is not None):
                    break
            else:
                focused_option = None
        
        return focused_option
    
    
    def get_non_focused_values(self):
        """
        Gets the non focused values of the interaction.
        
        Returns
        -------
        non_focused_options : `dict` of (`str`, (`None`, `str`)) items
        """
        return dict(self._iter_non_focused_values())
    
    
    def _iter_non_focused_values(self):
        """
        Iterates over the non focused values of the interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
            The option's name.
        value : `None`, `str`
            The option's value.
        """
        options = self.options
        if (options is not None):
            for option in options:
                yield from option._iter_non_focused_values()
    
    
    def get_value_of(self, *option_names):
        """
        Gets the value for the option by the given name.
        
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
            
            options = self.options
            if options is None:
                value = None
            else:
                for option in options:
                    if option.name == option_name:
                        value = option.get_value_of(*option_names)
                        break
                else:
                    value = None
        else:
            value = None
        
        return value
    
    
    @property
    def value(self):
        """
        Returns the focused option's value of the application command autocomplete interaction.
        
        Returns
        -------
        value : `None`, `str`
        """
        focused_option = self.focused_option
        if (focused_option is None):
            value = None
        else:
            value = focused_option.value
        
        return value



class ApplicationCommandAutocompleteInteractionOption:
    """
    Application auto complete option representing an auto completable parameters.
    
    Attributes
    ----------
    focused : `bool`
        Whether this field is focused by the user.
    name : `str`
        The name of the parameter.
    options : `None`, `tuple` of ``ApplicationCommandAutocompleteInteractionOption``
        Nested functions.
    type : ``ApplicationCommandOptionType``
        The represented option's type.
    value : `None`, `str`
        The value, the user has been typed.
    """
    __slots__ = ('focused', 'name', 'options', 'type', 'value')
    
    def __new__(cls, data):
        """
        Creates a new ``ApplicationCommandAutocompleteOption`` from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Application command autocomplete option data.
        """
        # focused
        focused = data.get('focused', False)
        
        # name
        name = data['name']
        
        # options
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(
                ApplicationCommandAutocompleteInteractionOption(option_data) for option_data in option_datas
            )
        
        # type
        type_ = ApplicationCommandOptionType.get(data['type'])
        
        # value
        value = data.get('value', None)
        if (value is not None) and (not value):
            value = None
        
        self = object.__new__(cls)
        self.focused = focused
        self.name = name
        self.options = options
        self.type = type_
        self.value = value
        return self
    
    
    def __repr__(self):
        """Returns the application command autocomplete option's representation."""
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
        """Returns the application command autocomplete option's representation."""
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
        """Returns whether the two application command autocomplete option's are equal."""
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
    
    
    @property
    def focused_option(self):
        """
        Returns the focused option of the application command autocomplete interaction option.
        
        Returns
        -------
        option : `None`, ``ApplicationCommandAutocompleteInteractionOption``
        """
        if self.focused:
            return self
        
        options = self.options
        if (options is not None):
            for option in options:
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
            options = self.options
            if (options is not None):
                for option in options:
                    yield from option._iter_non_focused_values()
        else:
            if not self.focused:
                yield self.name, self.value
    
    
    def get_value_of(self, *option_names):
        """
        Gets the value for the option by the given name.
        
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
            
            options = self.options
            if options is None:
                value = None
            else:
                for option in options:
                    if option.name == option_name:
                        value = option.get_value_of(*option_names)
                        break
                else:
                    value = None
        else:
            value = self.value
        
        return value
