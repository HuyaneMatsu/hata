__all__ = ('InteractionMetadataMessageComponent',)

from scarletio import copy_docs

from ...component import Component, ComponentType

from .base import InteractionMetadataBase
from .fields import (
    parse_component_type, parse_custom_id, parse_resolved, parse_values, put_component_type, put_custom_id,
    put_resolved, put_values, validate_component_type, validate_custom_id, validate_resolved, validate_values
)


class InteractionMetadataMessageComponent(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Parameters
    ----------
    component_type : ``ComponentType``
        The used component's type.
    
    custom_id : `None`, `str`
        Component or form interaction's custom identifier.
    
    resolved : ``None | Resolved``
        Contains the received entities.
    
    values : `None | tuple<str>`
        Values selected by the user.
    """
    __slots__ = ('component_type', 'custom_id', 'resolved', 'values')
    
    def __new__(
        cls,
        *,
        component_type = ...,
        custom_id = ...,
        resolved = ...,
        values = ...,
    ):
        """
        Creates a new interaction metadata from the given parameters.
        
        Parameters
        ----------
        component_type : ``ComponentType``, Optional (Keyword only)
            The used component's type.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Component or form interaction's custom identifier.
        
        resolved : ``None | Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        values : `None | tuple<str>`, Optional (Keyword only)
            Values selected by the user. Applicable for component interactions.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # component_type
        if component_type is ...:
            component_type = ComponentType.none
        else:
            component_type = validate_component_type(component_type)
        
        # custom_id
        if custom_id is ...:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # resolved
        if resolved is ...:
            resolved = None
        else:
            resolved = validate_resolved(resolved)
        
        # values
        if values is ...:
            values = None
        else:
            values = validate_values(values)
        
        # Construct
        self = object.__new__(cls)
        self.component_type = component_type
        self.custom_id = custom_id
        self.resolved = resolved
        self.values = values
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.component_type = ComponentType.none
        self.custom_id = None
        self.resolved = None
        self.values = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.component_type = self.component_type
        new.custom_id = self.custom_id
        
        resolved = self.resolved
        if (resolved is not None):
            resolved = resolved.copy()
        new.resolved = resolved
        
        values = self.values
        if (values is not None):
            values = (*values,)
        new.values = values
        
        return new
    
    def copy_with(
        self,
        *,
        component_type = ...,
        custom_id = ...,
        resolved = ...,
        values = ...,
    ):
        """
        Copies the interaction metadata with the given fields.
        
        Parameters
        ----------
        component_type : ``ComponentType``, Optional (Keyword only)
            The used component's type.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Component or form interaction's custom identifier.
        
        resolved : ``None | Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        values : `None | tuple<str>`, Optional (Keyword only)
            Values selected by the user. Applicable for component interactions.
        
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
        # component_type
        if component_type is ...:
            component_type = self.component_type
        else:
            component_type = validate_component_type(component_type)
        
        # custom_id
        if custom_id is ...:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # resolved
        if resolved is ...:
            resolved = self.resolved
            if (resolved is not None):
                resolved = resolved.copy()
        else:
            resolved = validate_resolved(resolved)
        
        # values
        if values is ...:
            values = self.values
            if (values is not None):
                values = (*values,)
        else:
            values = validate_values(values)
        
        # Construct
        new = object.__new__(type(self))
        new.component_type = component_type
        new.custom_id = custom_id
        new.resolved = resolved
        new.values = values
        return new
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, guild_id = 0):
        self = object.__new__(cls)
        self.component_type = parse_component_type(data)
        self.custom_id = parse_custom_id(data)
        self.resolved = parse_resolved(data, guild_id)
        self.values = parse_values(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = {}
        put_component_type(self.component_type, data, defaults)
        put_custom_id(self.custom_id, data, defaults)
        put_resolved(self.resolved, data, defaults, guild_id = guild_id)
        put_values(self.values, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        # component_type
        repr_parts.append(' component_type = ')
        repr_parts.append(repr(self.component_type))
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id = ')
            repr_parts.append(repr(custom_id))
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            repr_parts.append(', resolved = ')
            repr_parts.append(repr(resolved))
        
        # values
        values = self.values
        if (values is not None):
            repr_parts.append(', values = ')
            repr_parts.append(repr(values))
        
        return True
    
    
    @copy_docs(InteractionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # component_type
        hash_value ^= self.component_type.value
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            hash_value ^= hash(resolved)
        
        # values
        values = self.values
        if (values is not None):
            hash_value ^= len(values)
            
            for option in values:
                hash_value ^= hash(option)
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataBase.__eq__)
    def __eq__(self, other):
        other_type = type(other)
        if other_type is type(self):
            return self._is_equal_same_type(other)
        
        # Compare with components.
        if issubclass(other_type, Component):
            # Check `type` before `custom_id`
            
            # type
            if self.component_type is not other.type:
                return False
            
            # custom_id
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        return NotImplemented
    
    
    @copy_docs(InteractionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # component_type
        if self.component_type is not other.component_type:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # resolved
        if self.resolved != other.resolved:
            return False
        
        # values
        if self.values != other.values:
            return False
        
        return True
