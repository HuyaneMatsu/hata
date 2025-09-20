__all__ = ('InteractionMetadataApplicationCommand',)

from warnings import warn

from scarletio import copy_docs

from ...application_command import ApplicationCommandTargetType

from .application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete
from .fields import (
    parse_target_id, parse_target_type, put_target_id, put_target_type, validate_target_id, validate_target_type
)


class InteractionMetadataApplicationCommand(InteractionMetadataApplicationCommandAutocomplete):
    """
    Interaction metadata used when the interaction was triggered by an application command.
    
    Parameters
    ----------
    application_command_id : `int`
        The represented application command's identifier number.
    
    application_command_name : `str`
        The represented application command's application_command_name.
    
    options : ``None | tuple<InteractionOption>``
        Application command option representations. Like sub-command or parameter.
    
    target_id : `int`
        The interaction's target's identifier. Applicable for context commands.
    
    target_type : ``ApplicationCommandTargetType``
        The invoked application command's target type.
    """
    __slots__ = ('target_id', 'target_type')
    
    def __new__(
        cls,
        *,
        application_command_id = ...,
        application_command_name = ...,
        name = ...,
        options = ...,
        target_id = ...,
        target_type = ...,
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
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
        target_type : ``None | int | ApplicationCommandTargetType``, Optional (Keyword only)
            The invoked application command's target type.
        
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
        
        # target_id
        if target_id is ...:
            target_id = 0
        else:
            target_id = validate_target_id(target_id)
        
        # target_type
        if target_type is ...:
            target_type = ApplicationCommandTargetType.none
        else:
            target_type = validate_target_type(target_type)
        
        # Construct
        self = InteractionMetadataApplicationCommandAutocomplete.__new__(
            cls,
            application_command_id = application_command_id,
            application_command_name = application_command_name,
            options = options,
        )
        self.target_id = target_id
        self.target_type = target_type
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            application_command_id = keyword_parameters.pop('application_command_id', ...),
            application_command_name = keyword_parameters.pop('application_command_name', ...),
            options = keyword_parameters.pop('options', ...),
            target_id = keyword_parameters.pop('target_id', ...),
            target_type = keyword_parameters.pop('target_type', ...),
        )
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._create_empty)
    def _create_empty(cls):
        self = super(InteractionMetadataApplicationCommand, cls)._create_empty()
        self.target_id = 0
        self.target_type = ApplicationCommandTargetType.none
        return self
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.copy)
    def copy(self):
        new = InteractionMetadataApplicationCommandAutocomplete.copy(self)
        new.target_id = self.target_id 
        new.target_type = self.target_type
        
        return new
    
    
    def copy_with(
        self,
        *,
        application_command_id = ...,
        application_command_name = ...,
        name = ...,
        options = ...,
        target_id = ...,
        target_type = ...,
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
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
        target_type : ``None | int | ApplicationCommandTargetType``, Optional (Keyword only)
            The invoked application command's target type.
        
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
        
        # target_id
        if target_id is ...:
            target_id = self.target_id
        else:
            target_id = validate_target_id(target_id)
        
        # target_type
        if target_type is ...:
            target_type = self.target_type
        else:
            target_type = validate_target_type(target_type)
        
        # Construct
        new = InteractionMetadataApplicationCommandAutocomplete.copy_with(
            self,
            application_command_id = application_command_id,
            application_command_name = application_command_name,
            options = options,
        )
        new.target_id = target_id
        new.target_type = target_type
        return new
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            application_command_id = keyword_parameters.pop('application_command_id', ...),
            application_command_name = keyword_parameters.pop('application_command_name', ...),
            options = keyword_parameters.pop('options', ...),
            target_id = keyword_parameters.pop('target_id', ...),
            target_type = keyword_parameters.pop('target_type', ...),
        )
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.from_data)
    def from_data(cls, data, guild_id = 0):
        self = super(InteractionMetadataApplicationCommand, cls).from_data(data, guild_id)
        self.target_id = parse_target_id(data)
        self.target_type = parse_target_type(data)
        return self
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = InteractionMetadataApplicationCommandAutocomplete.to_data(
            self, defaults = defaults, guild_id = guild_id
        )
        put_target_id(self.target_id, data, defaults)
        put_target_type(self.target_type, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        field_added = InteractionMetadataApplicationCommandAutocomplete._put_attribute_representations_into(
            self, repr_parts
        )
        
        # target_id
        target_id = self.target_id
        if target_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' target_id = ')
            repr_parts.append(repr(target_id))
        
        # target_type
        target_type = self.target_type
        if target_type:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' target_type = ')
            repr_parts.append(target_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(target_type.value))
        
        return field_added
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.__hash__)
    def __hash__(self):
        hash_value = InteractionMetadataApplicationCommandAutocomplete.__hash__(self)
        
        # target_id
        hash_value ^= self.target_id
        
        # target_type
        hash_value ^= hash(self.target_type) << 4
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not InteractionMetadataApplicationCommandAutocomplete._is_equal_same_type(self, other):
            return False
        
        # target_id
        if self.target_id != other.target_id:
            return False
        
        # target_type
        if self.target_type is not other.target_type:
            return False
        
        return True
