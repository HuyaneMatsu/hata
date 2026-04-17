__all__ = ('MediaItem',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_description, parse_media, parse_spoiler, put_description, put_media, put_spoiler, validate_description,
    validate_media, validate_spoiler
)


class MediaItem(RichAttributeErrorBaseType):
    """
    Represents a media's item.
    
    Attributes
    ----------
    description : `None | str`
        The media item's description.
    
    media : ``MediaInfo``
        The item's media.
    
    spoiler : `bool`
        Whether the media should be spoilered.
    """
    __slots__ = ('description', 'media', 'spoiler')
    
    def __new__(cls, media, *, description = ..., spoiler = ...):
        """
        Creates a new media item with the given parameters.
        
        Parameters
        ----------
        media : ``str | MediaInfo``
            The item's media.
        
        description : `None | str`, Optional (Keyword only)
            The item's description.
        
        spoiler : `bool`, Optional (Keyword only)
            Whether the media should be spoilered.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # media
        media = validate_media(media)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # spoiler
        if spoiler is ...:
            spoiler = False
        else:
            spoiler = validate_spoiler(spoiler)
        
        # construct
        self = object.__new__(cls)
        self.description = description
        self.spoiler = spoiler
        self.media = media
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # media
        repr_parts.append(' media = ')
        repr_parts.append(repr((self.media)))
        
        # description
        description = self.description
        if description is not None:
            repr_parts.append(', description = ')
            repr_parts.append(repr(description))
        
        # spoiler
        spoiler = self.spoiler
        if spoiler:
            repr_parts.append(', spoiler = ')
            repr_parts.append(repr(spoiler))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # media
        hash_value ^= hash(self.media)
        
        # spoiler
        hash_value ^= self.spoiler << 11
        
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # description
        if self.description != other.description:
            return False
        
        # spoiler
        if self.spoiler != other.spoiler:
            return False
        
        # media
        if self.media != other.media:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new media item instance from the given json data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create media item from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.description = parse_description(data)
        self.media = parse_media(data)
        self.spoiler = parse_spoiler(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Returns the media item as a json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_description(self.description, data, defaults)
        put_media(self.media, data, defaults, include_internals = include_internals)
        put_spoiler(self.spoiler, data, defaults)
        return data
    
    
    def copy(self):
        """
        Copies the media item.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.description = self.description
        new.media = self.media.copy()
        new.spoiler = self.spoiler
        return new
    
    
    def copy_with(self, *, description = ..., media = ..., spoiler = ...):
        """
        Copies the media item with the given parameters.
        
        Parameters
        ----------
        description : `None | str`, Optional (Keyword only)
            The item's description.
        
        media : ``str | MediaInfo``, Optional (Keyword only)
            The item's media.
        
        spoiler : `bool`, Optional (Keyword only)
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
    
    
    @property
    def url(self):
        """
        Returns the media's url.
        
        Returns
        -------
        url : `str`
        """
        return self.media.url
