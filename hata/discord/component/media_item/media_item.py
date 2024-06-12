__all__ = ('MediaItem',)

from scarletio import RichAttributeErrorBaseType

from ...utils import url_cutter

from .fields import (
    parse_description, parse_spoiler, parse_url, put_description_into, put_spoiler_into, put_url_into,
    validate_description, validate_spoiler, validate_url,
)


class MediaItem(RichAttributeErrorBaseType):
    """
    Represents a media's item.
    
    Attributes
    ----------
    description : `None`, `str`
        The media item's description.
    spoiler : `bool`
        Whether the media should be spoilered.
    url : `str`
        The media's url.
    """
    __slots__ = ('description', 'spoiler', 'url')
    
    def __new__(cls, url, *, description = ..., spoiler = ...):
        """
        Creates a new media item with the given parameters.
        
        Parameters
        ----------
        url : `str`
            The media's url.
        description : `None`, `str`, Optional (Keyword only)
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
        # url
        url = validate_url(url)
        
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
        self.url = url
        return self
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # url
        repr_parts.append(' url = ')
        repr_parts.append(repr(url_cutter(self.url)))
        
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
        """Returns the media item's hash value."""
        hash_value = 0
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # spoiler
        hash_value ^= self.spoiler
        
        # url
        hash_value ^= hash(self.url)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two media items are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # description
        if self.description != other.description:
            return False
        
        # spoiler
        if self.spoiler != other.spoiler:
            return False
        
        # url
        if self.url != other.url:
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
        self.spoiler = parse_spoiler(data)
        self.url = parse_url(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Returns the media item as a json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_description_into(self.description, data, defaults)
        put_spoiler_into(self.spoiler, data, defaults)
        put_url_into(self.url, data, defaults)
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
        new.spoiler = self.spoiler
        new.url = self.url
        return new
    
    
    def copy_with(self, *, description = ..., spoiler = ..., url = ...):
        """
        Copies the media item with the given parameters.
        
        Parameters
        ----------
        description : `None`, `str`, Optional (Keyword only)
            The item's description.
        spoiler : `bool`, Optional (Keyword only)
            Whether the media should be spoilered.
        url : `str`, Optional (Keyword only)
            The media's url.
        
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
        
        # spoiler
        if spoiler is ...:
            spoiler = self.spoiler
        else:
            spoiler = validate_spoiler(spoiler)
        
        # url
        if url is ...:
            url = self.url
        else:
            url = validate_url(url)
        
        # Construct
        new = object.__new__(type(self))
        new.description = description
        new.spoiler = spoiler
        new.url = url
        return new
