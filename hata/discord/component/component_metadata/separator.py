__all__ = ('ComponentMetadataSeparator',)

from scarletio import copy_docs

from .constants import SEPARATOR_SPACING_SIZE_DEFAULT
from .base import ComponentMetadataBase
from .fields import (
    parse_divider, parse_spacing_size, put_divider_into, put_spacing_size_into, validate_divider, validate_spacing_size
)


class ComponentMetadataSeparator(ComponentMetadataBase):
    """
    Represents the metadata of a separator component used inside of a form.
    
    Attributes
    ----------
    divider : `bool`
        Whether the separator should contain a divider.
    spacing_size : ``SeparatorSpacingSize``
        The separator's spacing's size.
    """
    __slots__ = ('divider', 'spacing_size')
    
    def __new__(
        cls,
        *,
        divider = ...,
        spacing_size = ...,
    ):
        """
        Creates a separator component metadata.
        
        Parameters
        ----------
        divider : `bool`, Optional (Keyword only)
            Whether the separator should contain a divider.
        spacing_size : ``SeparatorSpacingSize``, `int`, Optional (Keyword only)
            The separator's spacing's size.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # divider
        if divider is ...:
            divider = True
        else:
            divider = validate_divider(divider)
        
        # spacing_size
        if spacing_size is ...:
            spacing_size = SEPARATOR_SPACING_SIZE_DEFAULT
        else:
            spacing_size = validate_spacing_size(spacing_size)
        
        # Construct
        self = object.__new__(cls)
        self.divider = divider
        self.spacing_size = spacing_size
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            divider = keyword_parameters.pop('divider', ...),
            spacing_size = keyword_parameters.pop('spacing_size', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # divider
        divider = self.divider
        if divider:
            repr_parts.append(' divider = ')
            repr_parts.append(repr(divider))
            
            field_added = True
        else:
            field_added = False
        
        # spacing_size
        spacing_size = self.spacing_size
        if (spacing_size is not SEPARATOR_SPACING_SIZE_DEFAULT):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' spacing_size = ')
            repr_parts.append(spacing_size.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(spacing_size.value))
            
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # divider
        hash_value ^= self.divider
        
        # spacing_size
        hash_value ^= self.spacing_size.value << 1
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # divider
        if self.divider != other.divider:
            return False
        
        # spacing_size
        if self.spacing_size is not other.spacing_size:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.divider = parse_divider(data)
        self.spacing_size = parse_spacing_size(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        
        put_divider_into(self.divider, data, defaults)
        put_spacing_size_into(self.spacing_size, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.divider = self.divider
        new.spacing_size = self.spacing_size
        
        return new
    
    
    def copy_with(
        self, 
        *,
        divider = ...,
        spacing_size = ...,
    ):
        """
        Copies the separator component metadata with the given fields.
        
        Parameters
        ----------
        divider : `bool`, Optional (Keyword only)
            Whether the separator should contain a divider.
        spacing_size : ``SeparatorSpacingSize``, `int`, Optional (Keyword only)
            The separator's spacing's size.
        
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
        # divider
        if divider is ...:
            divider = self.divider
        else:
            divider = validate_divider(divider)
        
        # spacing_size
        if spacing_size is ...:
            spacing_size = self.spacing_size
        else:
            spacing_size = validate_spacing_size(spacing_size)
        
        # Construct
        new = object.__new__(type(self))
        new.divider = divider
        new.spacing_size = spacing_size
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            divider = keyword_parameters.pop('divider', ...),
            spacing_size = keyword_parameters.pop('spacing_size', ...),
        )
