__all__ = ('InteractionComponentMetadataButton',)

from scarletio import copy_docs, include

from .base import InteractionComponentMetadataBase
from .fields import parse_custom_id, put_custom_id, validate_custom_id


ComponentType = include('ComponentType')


class InteractionComponentMetadataButton(InteractionComponentMetadataBase):
    """
    Interaction component metadata representing a button component.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was clicked (or used) by the user.
    """
    __slots__ = ('custom_id')
    
    def __new__(cls, *, custom_id = ...):
        """
        Creates a new interaction component metadata from the given fields.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was clicked (or used) by the user.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # custom_id
        if custom_id is ...:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # Construct.
        self = object.__new__(cls)
        self.custom_id = custom_id
        return self
    
    
    @classmethod
    def from_keyword_parameters(cls, keyword_parameters):
        """
        Creates a new interaction component metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Keyword parameters to build the metadata from.
        
        Returns
        -------
        self : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a keyword parameter's type is incorrect.
        ValueError
            - If a keyword parameter's value is incorrect.
        """
        return cls(
            custom_id = keyword_parameters.pop('custom_id', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # custom_id
        repr_parts.append(' custom_id = ')
        repr_parts.append(repr(self.custom_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(InteractionComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        return hash_value
    
    
    @copy_docs(InteractionComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        return True
    
    
    @copy_docs(InteractionComponentMetadataBase._match_to_component)
    def _match_to_component(self, other):
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(InteractionComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.custom_id = parse_custom_id(data)
        return self
    
    
    @copy_docs(InteractionComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_custom_id(self.custom_id, data, defaults)
        return data
    
    
    @copy_docs(InteractionComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        return new
    
    
    def copy_with(self, *, custom_id = ...):
        """
        Copies the interaction component metadata with the given fields.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was clicked (or used) by the user.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        # custom_id
        if custom_id is ...:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # Construct.
        new = object.__new__(type(self))
        new.custom_id = custom_id
        return new
    
    
    @copy_docs(InteractionComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            custom_id = keyword_parameters.pop('custom_id', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        custom_id = self.custom_id
        if (custom_id is not None):
            yield (custom_id, ComponentType.button, None)
