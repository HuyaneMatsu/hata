__all__ = ('EmbedImage',)

from scarletio import copy_docs

from ..embed_field_base import EmbedFieldBase, EmbedMediaFlag

from .fields import (
    parse_flags, parse_height, parse_proxy_url, parse_url, parse_width, put_flags, put_height,
    put_proxy_url, put_url, put_width, validate_url
)


class EmbedImage(EmbedFieldBase):
    """
    Represents an embed's image.
    
    Attributes
    ----------
    flags : ``EmbedMediaFlag``
        The embed image's flags.
    
    height : `int`
        The height of the image. Defaults to `0`.
    
    proxy_url : `None | str`
        A proxied url of the image.
    
    url : `None | str`
        The url of the image.
    
    width : `int`
        The width of the image. Defaults to `0`.
    """
    __slots__ = ('flags', 'height', 'proxy_url', 'url', 'width',)
    
    def __new__(cls, url = ...):
        """
        Creates a new embed field with the given parameters.
        
        Parameters
        ----------
        url : `None | str`, Optional
            The url of the image. Can be http(s) or attachment.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # url
        if url is ...:
            url = None
        else:
            url = validate_url(url)
        
        self = object.__new__(cls)
        self.flags = EmbedMediaFlag()
        self.height = 0
        self.proxy_url = None
        self.url = url
        self.width = 0
        return self
    
    
    @copy_docs(EmbedFieldBase.__bool__)
    def __bool__(self):
        # url
        if self.url is not None:
            return True
        
        return False
    
    
    @copy_docs(EmbedFieldBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts.append(' url = ')
        url = self.url
        if url is None:
            repr_parts.append('null')
        else:
            repr_parts.append(repr(url))
        
        width = self.width
        height = self.height
        if width or height:
            repr_parts.append(', size = ')
            repr_parts.append(str(self.width))
            repr_parts.append('x')
            repr_parts.append(str(self.height))
    
    
    @copy_docs(EmbedFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # url
        url = self.url
        if (url is not None):
            hash_value ^= hash(url)
        
        return hash_value
    
    
    @copy_docs(EmbedFieldBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # url
        if self.url != other.url:
            return False
        
        # proxy_url -> ignore
        if (self.proxy_url is not None) and (other.proxy_url is not None):
            # flags
            if self.flags != other.flags:
                return False
            
            # height
            if self.height != other.height:
                return False
            
            # width
            if self.width != other.width:
                return False
        
        return True
    
    
    @classmethod
    @copy_docs(EmbedFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.flags = parse_flags(data)
        self.height = parse_height(data)
        self.url = parse_url(data)
        self.proxy_url = parse_proxy_url(data)
        self.width = parse_width(data)
        return self
    
    
    @copy_docs(EmbedFieldBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_url(self.url, data, defaults)
        
        if include_internals:
            put_flags(self.flags, data, defaults)
            put_height(self.height, data, defaults)
            put_proxy_url(self.proxy_url, data, defaults)
            put_width(self.width, data, defaults)
        
        return data
    
    
    @copy_docs(EmbedFieldBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        new.flags = self.flags
        new.height = self.height
        new.proxy_url = self.proxy_url
        new.url = self.url
        new.width = self.width
        return new
    
    
    @copy_docs(EmbedFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.flags = self.flags
        new.height = self.height
        new.proxy_url = self.proxy_url
        new.url = self.url
        new.width = self.width
        return new
    
    
    def copy_with(self, *, url = ...):
        """
        Copies the embed image with the given parameters.
        
        Parameters
        ----------
        url : `None`, `str`, Optional (Keyword only)
            The url of the image. Can be http(s) or attachment.
        
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
        # url
        if url is ...:
            flags = self.flags
            url = self.url
            height = self.height
            proxy_url = self.proxy_url
            width = self.width
        
        else:
            flags = EmbedMediaFlag()
            url = validate_url(url)
            height = 0
            proxy_url = None
            width = 0
        
        new = object.__new__(type(self))
        new.flags = flags
        new.height = height
        new.proxy_url = proxy_url
        new.url = url
        new.width = width
        return new
