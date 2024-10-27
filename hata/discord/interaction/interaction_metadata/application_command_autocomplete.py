__all__ = ('InteractionMetadataApplicationCommandAutocomplete',)

from warnings import warn

from scarletio import copy_docs

from .base import InteractionMetadataBase
from .fields import (
    parse_id, parse_name, parse_options, put_id_into, put_name_into, put_options_into, validate_id, validate_name,
    validate_options
)


class InteractionMetadataApplicationCommandAutocomplete(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Parameters
    ----------
    id : `int`
        The represented application command's identifier number.
    
    name : `str`
        The represented application command's name.
    
    options : `None | tuple<InteractionOption>`
        Application command option representations. Like sub-command or parameter.
    """
    __slots__ = ('id', 'name', 'options')
    
    def __new__(
        cls,
        *,
        application_command_id = ...,
        id = ...,
        name = ...,
        options = ...,
    ):
        """
        Creates a new interaction metadata from the given parameters.
        
        Parameters
        ----------
        application_command_id : `int`, Optional (Keyword only)
            The represented application command's identifier number.
        
        name : `str`, Optional (Keyword only)
            The represented application command's name.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Application command option representations. Like sub-command or parameter.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # id - Deprecated
        if id is not ...:
            warn(
                (
                    f'`{cls.__name__}.__new__`\' `id` parameter is deprecated '
                    f'and will be removed in 2024 December. '
                    f'Please use `application_command_id` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            application_command_id = id
        
        # application_command_id
        if application_command_id is ...:
            application_command_id = 0
        else:
            application_command_id = validate_id(application_command_id)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # Construct
        self = object.__new__(cls)
        self.id = application_command_id
        self.name = name
        self.options = options
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.id = 0
        self.name = ''
        self.options = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.id = self.id
        new.name = self.name
        
        options = self.options
        if (options is not None):
            options = (*(option.copy() for option in options),)
        new.options = options
        
        return new
    
    
    def copy_with(
        self,
        *,
        application_command_id = ...,
        id = ...,
        name = ...,
        options = ...,
    ):
        """
        Copies the interaction metadata with the given fields.
        
        Parameters
        ----------
        application_command_id : `int`, Optional (Keyword only)
            The represented application command's identifier number.
        
        name : `str`, Optional (Keyword only)
            The represented application command's name.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Application command option representations. Like sub-command or parameter.
        
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
        # id - Deprecated
        if id is not ...:
            warn(
                (
                    f'`{type(self).__name__}.copy_with`\' `id` parameter is deprecated '
                    f'and will be removed in 2024 December. '
                    f'Please use `application_command_id` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            application_command_id = id
        
        # application_command_id
        if application_command_id is ...:
            application_command_id = self.id
        else:
            application_command_id = validate_id(application_command_id)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = (*(option.copy() for option in options),)
        else:
            options = validate_options(options)
        
        # Construct
        new = object.__new__(type(self))
        new.id = application_command_id
        new.name = name
        new.options = options
        return new
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, guild_id = 0):
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.options = parse_options(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = {}
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        put_options_into(self.options, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # options
        options = self.options
        if (options is not None):
            repr_parts.append(', options = ')
            repr_parts.append(repr(options))
        
        return True
    
    
    @copy_docs(InteractionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options)
            
            for option in options:
                hash_value ^= hash(option)
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
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
