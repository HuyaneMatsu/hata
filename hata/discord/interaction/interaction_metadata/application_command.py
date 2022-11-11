__all__ = ('InteractionMetadataApplicationCommand',)

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
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        # resolved
        try:
            resolved = keyword_parameters.pop('resolved')
        except KeyError:
            pass
        else:
            self.resolved = validate_resolved(resolved)
        
        # target_id
        try:
            target_id = keyword_parameters.pop('target_id')
        except KeyError:
            pass
        else:
            self.target_id = validate_target_id(target_id)
        
        
        InteractionMetadataApplicationCommandAutocomplete._set_attributes_from_keyword_parameters(
            self, keyword_parameters
        )
    
    
    @classmethod
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.from_data)
    def from_data(cls, data, interaction_event):
        self = super(InteractionMetadataApplicationCommand, cls).from_data(data, interaction_event)
        self.resolved = parse_resolved(data, interaction_event)
        self.target_id = parse_target_id(data)
        return self
    
    
    @copy_docs(InteractionMetadataApplicationCommandAutocomplete.to_data)
    def to_data(self, *, defaults = False, interaction_event = None):
        data = InteractionMetadataApplicationCommandAutocomplete.to_data(
            self, defaults = defaults, interaction_event = interaction_event
        )
        put_resolved_into(self.resolved, data, defaults, interaction_event = interaction_event)
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
            
            repr_parts.append(' resolved=')
            repr_parts.append(repr(resolved))
        
        # target_id
        target_id = self.target_id
        if target_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' target_id=')
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
