__all__ = ('ComponentMetadataMediaGallery',)

from scarletio import copy_docs

from .base import ComponentMetadataBase
from .fields import parse_items, put_items_into, validate_items


class ComponentMetadataMediaGallery(ComponentMetadataBase):
    """
    Represents the metadata of a text component used inside of a form.
    
    Attributes
    ----------
    items : `None`, `tuple` of ``MediaItem``
        The media items shown on the component.
    """
    __slots__ = ('items',)
    
    def __new__(cls, *, items = ...):
        """
        Creates a text component metadata.
        
        Parameters
        ----------
        items : `None`, `tuple` of ``MediaItem``, Optional (Keyword only)
            The media items shown on the component.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # items
        if items is ...:
            items = None
        else:
            items = validate_items(items)
        
        # Construct
        self = object.__new__(cls)
        self.items = items
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            items = keyword_parameters.pop('items', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # items
        items = self.items
        if (items is not None):
            repr_parts.append(' items = ')
            repr_parts.append(repr(items))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # items
        items = self.items
        if (items is not None):
            hash_value ^= len(items)
            
            for item in items:
                hash_value ^= hash(item)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # items
        if self.items != other.items:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.items = parse_items(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        
        put_items_into(self.items, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.items = self.items
        
        return new
    
    
    def copy_with(
        self, 
        *,
        items = ...,
    ):
        """
        Copies the text component metadata with the given fields.
        
        Parameters
        ----------
        items : `None`, `tuple` of ``MediaItem``, Optional (Keyword only)
            The media items shown on the component.
        
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
        # items
        if items is ...:
            items = self.items
        else:
            items = validate_items(items)
        
        # Construct
        new = object.__new__(type(self))
        new.items = items
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            items = keyword_parameters.pop('items', ...),
        )
