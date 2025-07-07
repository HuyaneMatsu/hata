__all__ = ('InteractionMetadataApplicationCommand',)


from scarletio import copy_docs

from ...application_command import ApplicationCommandTargetType

from .application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete
from .fields import (
    parse_resolved, parse_target_id, parse_target_type, put_resolved, put_target_id, put_target_type,
    validate_resolved, validate_target_id, validate_target_type
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
    
    resolved : ``None | Resolved``
        Contains the received entities.
    
    target_id : `int`
        The interaction's target's identifier. Applicable for context commands.
    
    target_type : ``ApplicationCommandTargetType``
        The invoked application command's target type.
    """
    __slots__ = ('resolved', 'target_id', 'target_type')
    
    
    def __new__(
        cls,
        *,
        application_command_id = ...,
        name = ...,
        options = ...,
        resolved = ...,
        target_id = ...,
        target_type = ...,
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
        
        resolved : ``None | Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
        target_type : `ApplicationCommandTargetType | None | int`, Optional (Keyword only)
            The invoked application command's target type.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
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
        
        # target_type
        if target_type is ...:
            target_type = ApplicationCommandTargetType.none
        else:
            target_type = validate_target_type(target_type)
        
        # Construct
        self = InteractionMetadataApplicationCommandAutocomplete.__new__(
            cls,
            application_command_id = application_command_id,
            name = name,
            options = options,
        )
        self.resolved = resolved
        self.target_id = target_id
        self.target_type = target_type
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._create_empty)
    def _create_empty(cls):
        self = super(InteractionMetadataApplicationCommand, cls)._create_empty()
        self.resolved = None
        self.target_id = 0
        self.target_type = ApplicationCommandTargetType.none
        return self
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.copy)
    def copy(self):
        new = InteractionMetadataApplicationCommandAutocomplete.copy(self)
        
        resolved = self.resolved
        if (resolved is not None):
            resolved = resolved.copy()
        new.resolved = resolved
        
        new.target_id = self.target_id 
        new.target_type = self.target_type
        
        return new
    
    
    def copy_with(
        self,
        *,
        application_command_id = ...,
        name = ...,
        options = ...,
        resolved = ...,
        target_id = ...,
        target_type = ...,
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
        
        resolved : ``None | Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
        target_type : `ApplicationCommandTargetType | None | int`, Optional (Keyword only)
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
        
        # target_type
        if target_type is ...:
            target_type = self.target_type
        else:
            target_type = validate_target_type(target_type)
        
        # Construct
        new = InteractionMetadataApplicationCommandAutocomplete.copy_with(
            self,
            application_command_id = application_command_id,
            name = name,
            options = options,
        )
        new.resolved = resolved
        new.target_id = target_id
        new.target_type = target_type
        return new
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.from_data)
    def from_data(cls, data, guild_id = 0):
        self = super(InteractionMetadataApplicationCommand, cls).from_data(data, guild_id)
        self.resolved = parse_resolved(data, guild_id)
        self.target_id = parse_target_id(data)
        self.target_type = parse_target_type(data)
        return self
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = InteractionMetadataApplicationCommandAutocomplete.to_data(
            self, defaults = defaults, guild_id = guild_id
        )
        put_resolved(self.resolved, data, defaults, guild_id = guild_id)
        put_target_id(self.target_id, data, defaults)
        put_target_type(self.target_type, data, defaults)
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
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            hash_value ^= hash(resolved)
        
        # target_id
        hash_value ^= self.target_id
        
        # target_type
        hash_value ^= hash(self.target_type) << 4
        
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
        
        # target_type
        if self.target_type is not other.target_type:
            return False
        
        return True
