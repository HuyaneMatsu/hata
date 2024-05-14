__all__ = ('InteractionMetadataApplicationCommand',)

from warnings import warn

from scarletio import copy_docs

from .application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete
from .fields import (
    parse_resolved, parse_target_id, put_resolved_into, put_target_id_into, validate_resolved, validate_target_id
)


class InteractionMetadataApplicationCommand(InteractionMetadataApplicationCommandAutocomplete):
    """
    Interaction metadata used when the interaction was triggered by an application command.
    
    Parameters
    ----------
    id : `int`
        The represented application command's identifier number.
    
    name : `str`
        The represented application command's name.
    
    options : `None`, `tuple` of ``InteractionOption``
        Application command option representations. Like sub-command or parameter.
    
    resolved : `None`, ``Resolved``
        Contains the received entities.
    
    target_id : `int`
        The interaction's target's identifier. Applicable for context commands.
    """
    __slots__ = ('resolved', 'target_id')
    
    
    def __new__(
        cls,
        *,
        application_command_id = ...,
        id = ...,
        name = ...,
        options = ...,
        resolved = ...,
        target_id = ...,
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
        
        resolved : `None`, ``Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
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
        
        # resolved
        if resolved is ...:
            resolved = None
        else:
            resolved = validate_resolved(resolved)
        
        # target_id
        if target_id is ...:
            target_id = 0
        else:
            target_id = validate_target_id(target_id)
        
        # Construct
        self = InteractionMetadataApplicationCommandAutocomplete.__new__(
            cls,
            application_command_id = application_command_id,
            name = name,
            options = options,
        )
        self.resolved = resolved
        self.target_id = target_id
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._create_empty)
    def _create_empty(cls):
        self = super(InteractionMetadataApplicationCommand, cls)._create_empty()
        self.resolved = None
        self.target_id = 0
        return self
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.copy)
    def copy(self):
        new = InteractionMetadataApplicationCommandAutocomplete.copy(self)
        
        resolved = self.resolved
        if (resolved is not None):
            resolved = resolved.copy()
        new.resolved = resolved
        
        new.target_id = self.target_id 
        
        return new
    
    
    def copy_with(
        self,
        *,
        application_command_id = ...,
        id = ...,
        name = ...,
        options = ...,
        resolved = ...,
        target_id = ...,
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
        
        resolved : `None`, ``Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
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
        
        # resolved
        if resolved is ...:
            resolved = self.resolved
            if (resolved is not None):
                resolved = resolved.copy()
        else:
            resolved = validate_resolved(resolved)
        
        # target_id
        if target_id is ...:
            target_id = self.target_id
        else:
            target_id = validate_target_id(target_id)
        
        # Construct
        new = InteractionMetadataApplicationCommandAutocomplete.copy_with(
            self,
            application_command_id = application_command_id,
            name = name,
            options = options,
        )
        new.resolved = resolved
        new.target_id = target_id
        return new
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.from_data)
    def from_data(cls, data, guild_id = 0):
        self = super(InteractionMetadataApplicationCommand, cls).from_data(data, guild_id)
        self.resolved = parse_resolved(data, guild_id)
        self.target_id = parse_target_id(data)
        return self
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = InteractionMetadataApplicationCommandAutocomplete.to_data(
            self, defaults = defaults, guild_id = guild_id
        )
        put_resolved_into(self.resolved, data, defaults, guild_id = guild_id)
        put_target_id_into(self.target_id, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        field_added = InteractionMetadataApplicationCommandAutocomplete._put_attribute_representations_into(
            self, repr_parts
        )
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' resolved = ')
            repr_parts.append(repr(resolved))
        
        # target_id
        target_id = self.target_id
        if target_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' target_id = ')
            repr_parts.append(repr(target_id))
        
        return field_added
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.__hash__)
    def __hash__(self):
        hash_value = InteractionMetadataApplicationCommandAutocomplete.__hash__(self)
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            hash_value ^= hash(resolved)
        
        # target_id
        hash_value ^= self.target_id
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not InteractionMetadataApplicationCommandAutocomplete._is_equal_same_type(self, other):
            return False
        
        # resolved
        if self.resolved != other.resolved:
            return False
        
        # target_id
        if self.target_id != other.target_id:
            return False
        
        return True
