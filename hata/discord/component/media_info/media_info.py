__all__ = ('MediaInfo', )

from scarletio import RichAttributeErrorBaseType

from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_content_type, parse_height, parse_proxy_url, parse_url, parse_width, put_content_type, put_height,
    put_proxy_url, put_url, put_width, validate_content_type, validate_height, validate_proxy_url, validate_url,
    validate_width
)


PRECREATE_FIELDS = {
    'content_type': ('content_type', validate_content_type),
    'height': ('height', validate_height),
    'proxy_url': ('proxy_url', validate_proxy_url),
    'url': ('url', validate_url),
    'width': ('width', validate_width),
}


class MediaInfo(RichAttributeErrorBaseType):
    """
    Represents a media information of a ``MediaItem`` or of a few components that may support embedding it.
    
    Attributes
    ----------
    content_type : `None | str`
        The media info's media type.
    
    height : `int`
        The height of the media info if applicable.
        
        > Defaults to `0`.
    
    proxy_url : `str`
        Proxied url of the media info.
    
    url : `str`
        The media info's url.
    
    width : `int`
        The media info's width if applicable.
        
        > Defaults to `0`.
    """
    __slots__ = ('content_type', 'height', 'proxy_url', 'url', 'width')
    
    
    def __new__(cls, url):
        """
        Creates a new media info.
        
        Parameters
        ----------
        url : `str`.
            The media's url.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        url = validate_url(url)
        
        # Construct
        self = object.__new__(cls)
        self.content_type = None
        self.height = 0
        self.proxy_url = None
        self.url = url
        self.width = 0
        return self
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty media info.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.content_type = None
        self.height = 0
        self.proxy_url = None
        self.url = ''
        self.width = 0
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a media info from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create form.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.content_type = parse_content_type(data)
        self.height = parse_height(data)
        self.proxy_url = parse_proxy_url(data)
        self.url = parse_url(data)
        self.width = parse_width(data)
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__,]
        
        # url
        repr_parts.append(' url = ')
        repr_parts.append(repr(self.url))
        
        # Extra if image
        width = self.width
        height = self.height
        if width and height:
            repr_parts.append(',  = ')
            repr_parts.append(repr(width))
            repr_parts.append('x')
            repr_parts.append(repr(height))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_proxy_url = self.proxy_url
        other_proxy_url = other.proxy_url
        if (self_proxy_url is not None) and (other_proxy_url is not None):
            # proxy_url
            if self.proxy_url != other.proxy_url:
                return False
            
            # content_type
            if self.content_type != other.content_type:
                return False
            
            # height
            if self.height != other.height:
                return False
            
            # width
            if self.width != other.width:
                return False
        
        # url
        if self.url != other.url:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # proxy_url
        proxy_url = self.proxy_url
        if (proxy_url is not None):
            hash_value ^= hash(proxy_url)
            
            # content_type
            content_type = self.content_type
            if (content_type is not None):
                hash_value ^= hash(content_type)
            
            # height
            hash_value ^= self.height << 16
            
            # width
            hash_value ^= self.width << 8
        
        # url
        hash_value ^= hash(self.url)
        
        return hash_value
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Serializes the media info.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_url(self.url, data, defaults)
        
        if include_internals:
            put_content_type(self.content_type, data, defaults)
            put_height(self.height, data, defaults)
            put_width(self.width, data, defaults)
            put_proxy_url(self.proxy_url, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the media info.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.content_type = None
        new.height = 0
        new.proxy_url = None
        new.url = self.url
        new.width = 0
        return new
    
    
    def copy_with(self, *, url = ...):
        """
        Copies the media info with the given fields.
        
        Parameters
        ----------
        url : `str`, Optional (Keyword only)
            The media's url.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        # url
        if url is ...:
            url = self.url
        else:
            url = validate_url(url)
        
        # Construct
        new = object.__new__(type(self))
        new.content_type = None
        new.height = 0
        new.proxy_url = None
        new.url = url
        new.width = 0
        return new
    
    
    @classmethod
    def precreate(
        cls,
        **keyword_parameters,
    ):
        """
        Precreates the media info. The only difference between ``.__new__`` and ``.precreate`` here is that
        ``.precreate`` allows passing internal fields as well.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        content_type : `None | str`, Optional (Keyword only)
            The media info's media type.
        
        height : `int`, Optional (Keyword only)
            The height of the media info if applicable.
        
        proxy_url : `None | str`, Optional (Keyword only)
            Proxied url of the media info.
        
        url : `str`, Optional (Keyword only)
            The media info's url.
        
        width : `int`, Optional (Keyword only)
            The media info's width if applicable.
        
        Returns
        -------
        self : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        
        else:
            processed = None
        
        # Construct
        self = cls._create_empty()
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
