__all__ = ('EmbedAuthor',)

import warnings

from scarletio import copy_docs

from ...utils import sanitize_mentions, url_cutter

from ..embed_field_base import EmbedFieldBase

from .fields import (
    parse_icon_proxy_url, parse_icon_url, parse_name, parse_url, put_icon_proxy_url_into, put_icon_url_into,
    put_name_into, put_url_into, validate_icon_url, validate_name, validate_url
)


class EmbedAuthor(EmbedFieldBase):
    """
    Represents an embed's author.
    
    Attributes
    ----------
    icon_url : `None`, `str`
        Url of the author's icon.
    icon_proxy_url : `None`, `str`
        A proxied url to the url of the author's icon.
    name : `None`, `str`
        The name of the author.
    url : `None`, `str`
        The url of the author.
    """
    __slots__ = ('icon_url', 'icon_proxy_url', 'name', 'url')
    
    def __new__(cls, name = ..., icon_url = ..., url = ...):
        """
        Creates a new embed field with the given parameters.
        
        Parameters
        ----------
        name : `None`, `str`, Optional
            The name of the author.
        icon_url: `None`, `str`, Optional
            An url of the author's icon. Can be http(s) or attachment.
        url : `None`, `str`, Optional
            The url of the author.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # icon_url
        if icon_url is ...:
            icon_url = None
        else:
            icon_url = validate_icon_url(icon_url)
        
        # name
        if name is ...:
            name = None
        else:
            name = validate_name(name)
        
        # url
        if url is ...:
            url = None
        else:
            url = validate_url(url)
        
        self = object.__new__(cls)
        self.icon_url = icon_url
        self.icon_proxy_url = None
        self.name = name
        self.url = url
        return self
    
        
    @copy_docs(EmbedFieldBase.__len__)
    def __len__(self):
        length = 0
        
        # name
        name = self.name
        if (name is not None):
            length += len(name)
        
        return length
    
    
    @copy_docs(EmbedFieldBase.__bool__)
    def __bool__(self):
        # icon_url
        if (self.icon_url is not None):
            return True
        
        # name
        if self.name is not None:
            return True
        
        # url
        if self.url is not None:
            return True
        
        return False
    
    
    @copy_docs(EmbedFieldBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        field_added = False
        
        name = self.name
        if name is not None:
            field_added = True
            repr_parts.append(' name = ')
            repr_parts.append(repr(self.name))
        
        icon_url = self.icon_url
        if icon_url is not None:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' icon_url = ')
            repr_parts.append(repr(url_cutter(icon_url)))
        
        url = self.url
        if url is not None:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' url = ')
            repr_parts.append(repr(url_cutter(url)))
    
    
    @copy_docs(EmbedFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # icon_url
        icon_url = self.icon_url
        if (icon_url is not None):
            hash_value ^= hash(icon_url)
        
        # name
        name = self.name
        if (name is not None):
            hash_value ^= hash(name)
        
        # url
        url = self.url
        if (url is not None):
            hash_value ^= hash(url)
        
        return hash_value
    
    
    @copy_docs(EmbedFieldBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # icon_url
        if self.icon_url != other.icon_url:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # url
        if self.url != other.url:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(EmbedFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.icon_url = parse_icon_url(data)
        self.icon_proxy_url = parse_icon_proxy_url(data)
        self.name = parse_name(data)
        self.url = parse_url(data)
        return self
    
    
    @copy_docs(EmbedFieldBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_icon_url_into(self.icon_url, data, defaults)
        put_name_into(self.name, data, defaults)
        put_url_into(self.url, data, defaults)
        
        if include_internals:
            put_icon_proxy_url_into(self.icon_proxy_url, data, defaults)
        
        return data
    
    
    @copy_docs(EmbedFieldBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        new.icon_url = self.icon_url
        new.icon_proxy_url = self.icon_proxy_url
        new.name = sanitize_mentions(self.name, guild)
        new.url = self.url
        return new
    
    
    @copy_docs(EmbedFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.icon_url = self.icon_url
        new.icon_proxy_url = self.icon_proxy_url
        new.name = self.name
        new.url = self.url
        return new
    
    
    def copy_with(self, *, icon_url = ..., name = ..., url = ...):
        """
        Copies the embed author with the given parameters.
        
        Parameters
        ----------
        icon_url : `None`, `str`, Optional (Keyword only)
            An url of the author's icon. Can be http(s) or attachment.
        name : `None`, `str`, Optional (Keyword only)
            The name of the author.
        url : `None`, `str`, Optional (Keyword only)
            The url of the author.
        
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
        # icon_url
        if icon_url is ...:
            icon_url = self.icon_url
            icon_proxy_url = self.icon_proxy_url
        else:
            icon_url = validate_icon_url(icon_url)
            icon_proxy_url = None
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # url
        if url is ...:
            url = self.url
        else:
            url = validate_url(url)
        
        new = object.__new__(type(self))
        new.icon_url = icon_url
        new.icon_proxy_url = icon_proxy_url
        new.name = name
        new.url = url
        return new
    
    
    @copy_docs(EmbedFieldBase.iter_contents)
    def iter_contents(self):
        name = self.name
        if (name is not None):
            yield name
    
    
    @property
    def proxy_icon_url(self):
        """
        Deprecated and will be removed in 2023 august. Please use ``.icon_proxy_url``.
        """
        warnings.warn(
            (
                f'`{type(self).__name__}.proxy_icon_url` is deprecated and will be removed in 2023 august. '
                f'Please use `.icon_proxy_url` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
    
        return self.icon_proxy_url
