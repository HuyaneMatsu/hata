__all__ = ('InteractionComponentMetadataSection',)

from scarletio import copy_docs

from .base import InteractionComponentMetadataBase
from .fields import (
    parse_components, parse_thumbnail, put_components, put_thumbnail, validate_components__section, validate_thumbnail
)


class InteractionComponentMetadataSection(InteractionComponentMetadataBase):
    """
    Interaction component metadata representing a section component.
    
    Attributes
    ----------
    components : ``None | tuple<InteractionComponent>``
        Sub-components nested inside.
    
    thumbnail : ``None | InteractionComponent``
        The thumbnail or other accessory (button) of a section component.
    """
    __slots__ = ('components', 'thumbnail')
    
    def __new__(cls, *, components = ..., thumbnail = ...):
        """
        Creates a new interaction component metadata from the given fields.
        
        Parameters
        ----------
        components : ``None | iterable<InteractionComponent>``, Optional (Keyword only)
            Sub-components nested inside.
        
        thumbnail : ``None | InteractionComponent``, Optional (Keyword only)
            The thumbnail or other accessory (button) of a section component.
        
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
            components = validate_components__section(components)
        
        # thumbnail
        if thumbnail is ...:
            thumbnail = None
        else:
            thumbnail = validate_thumbnail(thumbnail)
        
        # Construct.
        self = object.__new__(cls)
        self.components = components
        self.thumbnail = thumbnail
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
            components = keyword_parameters.pop('components', ...),
            thumbnail = keyword_parameters.pop('thumbnail', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # components
        repr_parts.append(' components = ')
        repr_parts.append(repr(self.components))
        
        # thumbnail
        repr_parts.append(', thumbnail = ')
        repr_parts.append(repr(self.thumbnail))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(InteractionComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components)
            
            for component in components:
                hash_value ^= hash(component)
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            hash_value ^= hash(thumbnail)
        
        return hash_value
    
    
    @copy_docs(InteractionComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # components
        if self.components != other.components:
            return False
        
        # thumbnail
        if self.thumbnail != other.thumbnail:
            return False
        
        return True
    
    
    @copy_docs(InteractionComponentMetadataBase._match_to_component)
    def _match_to_component(self, other):
        # components
        self_components = self.components
        other_components = other.components
        
        if (self_components is None) != (other_components is None):
            return False
        
        if (
            (self_components is not None) and
            (
                (len(self_components) != len(other_components)) or
                (not all(
                    self_component % other_component
                    for self_component, other_component
                    in zip(self_components, other_components)
                ))
            )
        ):
            return False
        
        # thumbnail
        self_thumbnail = self.thumbnail
        other_thumbnail = other.thumbnail
        
        if (self_thumbnail is None) != (other_thumbnail is None):
            return False
        
        if (self_thumbnail is not None) and (not (self_thumbnail % other_thumbnail)):
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(InteractionComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.components = parse_components(data)
        self.thumbnail = parse_thumbnail(data)
        return self
    
    
    @copy_docs(InteractionComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_components(self.components, data, defaults)
        put_thumbnail(self.thumbnail, data, defaults)
        return data
    
    
    @copy_docs(InteractionComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # components
        components = self.components
        if (components is not None):
            components = (*(component.copy() for component in components),)
        new.components = components
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            thumbnail = thumbnail.copy()
        new.thumbnail = thumbnail
        
        return new
    
    
    def copy_with(self, *, components = ..., thumbnail = ...):
        """
        Copies the interaction component metadata with the given fields.
        
        Parameters
        ----------
        components : ``None | iterable<InteractionComponent>``, Optional (Keyword only)
            Sub-components nested inside.
        
        thumbnail : ``None | InteractionComponent``, Optional (Keyword only)
            The thumbnail or other accessory (button) of a section component.
        
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
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = (*(component.copy() for component in components),)
        else:
            components = validate_components__section(components)
        
        # thumbnail
        if thumbnail is ...:
            thumbnail = self.thumbnail
            if (thumbnail is not None):
                thumbnail = thumbnail.copy()
        else:
            thumbnail = validate_thumbnail(thumbnail)
        
        # Construct.
        new = object.__new__(type(self))
        new.components = components
        new.thumbnail = thumbnail
        return new
    
    
    @copy_docs(InteractionComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            components = keyword_parameters.pop('components', ...),
            thumbnail = keyword_parameters.pop('thumbnail', ...),
        )
    
    
    @copy_docs(InteractionComponentMetadataBase.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        components = self.components
        if (components is not None):
            for component in components:
                yield from component.iter_custom_ids_and_values()
        
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            yield from thumbnail.iter_custom_ids_and_values()
