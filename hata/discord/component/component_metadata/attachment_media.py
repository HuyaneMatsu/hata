__all__ = ('ComponentMetadataAttachmentMedia',)

from scarletio import copy_docs

from ..media_info import MediaInfo

from .base import ComponentMetadataBase
from .fields import (
    parse_media__attachment_only, parse_spoiler, put_media__attachment_only, put_spoiler, validate_media,
    validate_spoiler
)


class ComponentMetadataAttachmentMedia(ComponentMetadataBase):
    """
    Represents the metadata of an singular attachment only media component.
    
    Attributes
    ----------
    media : ``MediaInfo``
        The media of the component.
        When sending it supports only attachments using the `attachment://<file_name>` url format.
    
    spoiler : `bool`
        Whether the media should be spoilered.
    """
    __slots__ = ('media', 'spoiler')
    
    def __new__(cls, *, media = ..., spoiler = ...):
        """
        Creates an attachment media component metadata.
        
        Parameters
        ----------
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
        self.media = media
        self.spoiler = spoiler
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            media = keyword_parameters.pop('media', ...),
            spoiler = keyword_parameters.pop('spoiler', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # media
        repr_parts.append(' media = ')
        repr_parts.append(repr(self.media))
        
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
        
        # media
        hash_value ^= hash(self.media)
        
        # spoiler
        hash_value ^= self.spoiler << 22
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
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
        self.media = parse_media__attachment_only(data)
        self.spoiler = parse_spoiler(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_media__attachment_only(self.media, data, defaults, include_internals = include_internals)
        put_spoiler(self.spoiler, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.media = self.media.copy()
        new.spoiler = self.spoiler
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        new.media = self.media.copy()
        new.spoiler = self.spoiler
        
        return new
    
    
    def copy_with(
        self, 
        *,
        media = ...,
        spoiler = ...,
    ):
        """
        Copies the attachment media component metadata with the given fields.
        
        Parameters
        ----------
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
        new.media = media
        new.spoiler = spoiler
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            media = keyword_parameters.pop('media', ...),
            spoiler = keyword_parameters.pop('spoiler', ...),
        )
