__all__ = ('ComponentMetadataTextDisplay',)

from scarletio import copy_docs

from ...utils import sanitize_mentions

from .base import ComponentMetadataBase
from .fields import parse_content, put_content, validate_content


class ComponentMetadataTextDisplay(ComponentMetadataBase):
    """
    Represents the metadata of a text component used inside of a form.
    
    Attributes
    ----------
    content : `None | str`
        The content shown on the component.
    """
    __slots__ = ('content',)
    
    def __new__(cls, *, content = ...):
        """
        Creates a text component metadata.
        
        Parameters
        ----------
        content : `None | str`, Optional (Keyword only)
            The content shown on the component.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # content
        if content is ...:
            content = None
        else:
            content = validate_content(content)
        
        # Construct
        self = object.__new__(cls)
        self.content = content
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            content = keyword_parameters.pop('content', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # content
        content = self.content
        if (content is not None):
            repr_parts.append(' content = ')
            repr_parts.append(repr(content))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # content
        content = self.content
        if (content is not None):
            hash_value ^= hash(content)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # content
        if self.content != other.content:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.content = parse_content(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_content(self.content, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        # content
        new.content = sanitize_mentions(self.content, guild)
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # content
        new.content = self.content
        
        return new
    
    
    def copy_with(
        self, 
        *,
        content = ...,
    ):
        """
        Copies the text component metadata with the given fields.
        
        Parameters
        ----------
        content : `None | str`, Optional (Keyword only)
            The content shown on the component.
        
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
        # content
        if content is ...:
            content = self.content
        else:
            content = validate_content(content)
        
        # Construct
        new = object.__new__(type(self))
        new.content = content
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            content = keyword_parameters.pop('content', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.iter_contents)
    def iter_contents(self):
        content = self.content
        if (content is not None):
            yield content
