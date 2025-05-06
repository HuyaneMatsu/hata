__all__ = ('ComponentMetadataThumbnailMedia',)

from scarletio import copy_docs

from ..media_info import MediaInfo

from .base import ComponentMetadataBase
from .fields import (
    parse_description, parse_media, parse_spoiler, put_description, put_media, put_spoiler, validate_description,
    validate_media, validate_spoiler
)


class ComponentMetadataThumbnailMedia(ComponentMetadataBase):
    """
    Represents the metadata of a thumbnail media component.
    
    Attributes
    ----------
    description : `None | str`
        Description of the component's media.
    
    media : ``MediaInfo``
        The media of the component.
    
    spoiler : `bool`
        Whether the media should be spoilered.
    """
    __slots__ = ('description', 'media', 'spoiler')
    
    def __new__(cls, *, description = ..., media = ..., spoiler = ...):
        """
        Creates a thumbnail media component metadata.
        
        Parameters
        ----------
        description : `None | str`, Optional (Keyword only)
            Description of the component's media.
        
        media : ``str | MediaInfo``, Optional (Keyword only)
            The media of the component.
        
        spoiler : `bool` Optional (Keyword only)
            Whether the media should be spoilered.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # media
        if media is ...:
            media = MediaInfo._create_empty()
        else:
            media = validate_media(media)
        
        # spoiler
        if spoiler is ...:
            spoiler = False
        else:
            spoiler = validate_spoiler(spoiler)
        
        # Construct
        self = object.__new__(cls)
        self.description = description
        self.media = media
        self.spoiler = spoiler
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            description = keyword_parameters.pop('description', ...),
            media = keyword_parameters.pop('media', ...),
            spoiler = keyword_parameters.pop('spoiler', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # media
        repr_parts.append(' media = ')
        repr_parts.append(repr(self.media))
        
        # description
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(repr(description))
        
        # spoiler
        spoiler = self.spoiler
        if spoiler:
            repr_parts.append(', spoiler = ')
            repr_parts.append(repr(spoiler))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # media
        hash_value ^= hash(self.media)
        
        # spoiler
        hash_value ^= self.spoiler << 20
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # description
        if self.description != other.description:
            return False
        
        # media
        if self.media != other.media:
            return False
        
        # spoiler
        if self.spoiler != other.spoiler:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.description = parse_description(data)
        self.media = parse_media(data)
        self.spoiler = parse_spoiler(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_description(self.description, data, defaults)
        put_media(self.media, data, defaults, include_internals = include_internals)
        put_spoiler(self.spoiler, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        new.description = self.description
        new.media = self.media.copy()
        new.spoiler = self.spoiler
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.description = self.description
        new.media = self.media.copy()
        new.spoiler = self.spoiler
        
        return new
    
    
    def copy_with(
        self, 
        *,
        description = ...,
        media = ...,
        spoiler = ...,
    ):
        """
        Copies the thumbnail media component metadata with the given fields.
        
        Parameters
        ----------
        description : `None | str`, Optional (Keyword only)
            Description of the component's media.
        
        media : ``str | MediaInfo``, Optional (Keyword only)
            The media of the component.
        
        spoiler : `bool` Optional (Keyword only)
            Whether the media should be spoilered.
        
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
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # media
        if media is ...:
            media = self.media.copy()
        else:
            media = validate_media(media)
        
        # spoiler
        if spoiler is ...:
            spoiler = self.spoiler
        else:
            spoiler = validate_spoiler(spoiler)
        
        # Construct
        new = object.__new__(type(self))
        new.description = description
        new.media = media
        new.spoiler = spoiler
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            description = keyword_parameters.pop('description', ...),
            media = keyword_parameters.pop('media', ...),
            spoiler = keyword_parameters.pop('spoiler', ...),
        )
