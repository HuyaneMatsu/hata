__all__ = ('InteractionMetadataFormSubmit',)

from scarletio import copy_docs

from .base import InteractionMetadataBase
from .fields import (
    parse_custom_id, parse_components, put_custom_id, put_components, validate_custom_id, validate_components
)


class InteractionMetadataFormSubmit(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Parameters
    ----------
    components : `None`, `tuple` of ``InteractionComponent``
        Submitted component values of a form submit interaction.
    
    custom_id : `None`, `str`
        Component or form interaction's custom identifier.
    """
    __slots__ = ('components', 'custom_id')
    
    def __new__(
        cls,
        *,
        components = ...,
        custom_id = ...,
    ):
        """
        Creates a new interaction metadata from the given parameters.
        
        Parameters
        ----------
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Submitted component values of a form submit interaction.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Component or form interaction's custom identifier.

        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # components
        if components is ...:
            components = None
        else:
            components = validate_components(components)
        
        # custom_id
        if custom_id is ...:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # Construct
        self = object.__new__(cls)
        self.components = components
        self.custom_id = custom_id
        return self
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.components = None
        self.custom_id = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        components = self.components
        if (components is not None):
            components = (*(option.copy() for option in components),)
        new.components = components
        
        new.custom_id = self.custom_id
        
        return new
    
    
    
    def copy_with(
        self,
        *,
        components = ...,
        custom_id = ...,
    ):
        """
        Copies the interaction metadata with the given fields.
        
        Parameters
        ----------
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Submitted component values of a form submit interaction.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Component or form interaction's custom identifier.
        
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
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = (*(option.copy() for option in components),)
        else:
            components = validate_components(components)
        
        # custom_id
        if custom_id is ...:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # Construct
        new = object.__new__(type(self))
        new.components = components
        new.custom_id = custom_id
        return new
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, guild_id = 0):
        self = object.__new__(cls)
        self.components = parse_components(data)
        self.custom_id = parse_custom_id(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, guild_id = 0):
        data = {}
        put_components(self.components, data, defaults)
        put_custom_id(self.custom_id, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        
        # components
        components = self.components
        if (components is not None):
            repr_parts.append(' components = ')
            repr_parts.append(repr(components))
            
            field_added = False
        else:
            field_added = True
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' custom_id = ')
            repr_parts.append(repr(custom_id))
        
        return field_added
    
    
    @copy_docs(InteractionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components)
            
            for option in components:
                hash_value ^= hash(option)
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # components
        if self.components != other.components:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        return True
