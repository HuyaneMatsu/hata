__all__ = ('InteractionMetadataApplicationCommandAutocomplete',)

from warnings import warn

from scarletio import copy_docs

from .base import InteractionMetadataBase
from .fields import (
    parse_application_command_id, parse_application_command_name, parse_options, put_application_command_id,
    put_application_command_name, put_options, validate_application_command_id, validate_application_command_name,
    validate_options
)


class InteractionMetadataApplicationCommandAutocomplete(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Parameters
    ----------
    application_command_id : `int`
        The represented application command's identifier number.
    
    application_command_name : `str`
        The represented application command's application_command_name.
    
    options : ``None | tuple<InteractionOption>``
        Application command option representations. Like sub-command or parameter.
    """
    __slots__ = ('application_command_id', 'application_command_name', 'options')
    
    def __new__(
        cls,
        *,
        application_command_id = ...,
        application_command_name = ...,
        name = ...,
        options = ...,
    ):
        """
        Creates a new interaction metadata from the given parameters.
        
        Parameters
        ----------
        application_command_id : ``None | int | ApplicationCommand``, Optional (Keyword only)
            The represented application command's identifier number.
        
        application_command_name : `None | str`, Optional (Keyword only)
            The represented application command's application_command_name.
        
        options : ``None | iterable<InteractionOption>``, Optional (Keyword only)
            Application command option representations. Like sub-command or parameter.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Deprecations
        if (name is not ...):
            warn(
                (
                    f'`{cls.__name__}.__new__`\'s `name` parameter is deprecated and is scheduled '
                    f'for removal at 2026 February. Please use the `application_command_name` parameter instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            application_command_name = name
        
        # application_command_id
        if application_command_id is ...:
            application_command_id = 0
        else:
            application_command_id = validate_application_command_id(application_command_id)
        
        # application_command_name
        if application_command_name is ...:
            application_command_name = ''
        else:
            application_command_name = validate_application_command_name(application_command_name)
        
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # Construct
        self = object.__new__(cls)
        self.application_command_id = application_command_id
        self.application_command_name = application_command_name
        self.options = options
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            application_command_id = keyword_parameters.pop('application_command_id', ...),
            application_command_name = keyword_parameters.pop('application_command_name', ...),
            options = keyword_parameters.pop('options', ...),
        )
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.application_command_id = 0
        self.application_command_name = ''
        self.options = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.application_command_id = self.application_command_id
        new.application_command_name = self.application_command_name
        
        options = self.options
        if (options is not None):
            options = (*(option.copy() for option in options),)
        new.options = options
        
        return new
    
    
    def copy_with(
        self,
        *,
        application_command_id = ...,
        application_command_name = ...,
        name = ...,
        options = ...,
    ):
        """
        Copies the interaction metadata with the given fields.
        
        Parameters
        ----------
        application_command_id : ``None | int | ApplicationCommand``, Optional (Keyword only)
            The represented application command's identifier number.
        
        application_command_name : `None | str`, Optional (Keyword only)
            The represented application command's application_command_name.
        
        options : ``None | iterable<InteractionOption>``, Optional (Keyword only)
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
        # Deprecations
        if (name is not ...):
            warn(
                (
                    f'`{type(self).__name__}.copy_with`\'s `name` parameter is deprecated and is scheduled '
                    f'for removal at 2026 February. Please use the `application_command_name` parameter instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            application_command_name = name
        
        # application_command_id
        if application_command_id is ...:
            application_command_id = self.application_command_id
        else:
            application_command_id = validate_application_command_id(application_command_id)
        
        # application_command_name
        if application_command_name is ...:
            application_command_name = self.application_command_name
        else:
            application_command_name = validate_application_command_name(application_command_name)
        
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = (*(option.copy() for option in options),)
        else:
            options = validate_options(options)
        
        # Construct
        new = object.__new__(type(self))
        new.application_command_id = application_command_id
        new.application_command_name = application_command_name
        new.options = options
        return new
    
    
    @copy_docs(InteractionMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            application_command_id = keyword_parameters.pop('application_command_id', ...),
            application_command_name = keyword_parameters.pop('application_command_name', ...),
            options = keyword_parameters.pop('options', ...),
        )
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, guild_id = 0):
        self = object.__new__(cls)
        self.application_command_id = parse_application_command_id(data)
        self.application_command_name = parse_application_command_name(data)
        self.options = parse_options(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = {}
        put_application_command_id(self.application_command_id, data, defaults)
        put_application_command_name(self.application_command_name, data, defaults)
        put_options(self.options, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        # id
        repr_parts.append(' application_command_id = ')
        repr_parts.append(repr(self.application_command_id))
        
        # application_command_name
        repr_parts.append(', application_command_name = ')
        repr_parts.append(repr(self.application_command_name))
        
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
        hash_value ^= self.application_command_id
        
        # application_command_name
        hash_value ^= hash(self.application_command_name)
        
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
        if self.application_command_id != other.application_command_id:
            return False
        
        # application_command_name
        if self.application_command_name != other.application_command_name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        return True
