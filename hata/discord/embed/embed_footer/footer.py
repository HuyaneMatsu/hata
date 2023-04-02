__all__ = ('EmbedFooter',)

import warnings

from scarletio import copy_docs

from ...utils import sanitize_mentions, url_cutter

from ..embed_field_base import EmbedFieldBase

from .fields import (
    parse_icon_proxy_url, parse_icon_url, parse_text, put_icon_proxy_url_into, put_icon_url_into, put_text_into,
    validate_icon_url, validate_text
)


class EmbedFooter(EmbedFieldBase):
    """
    Represents an embed's footer.
    
    Attributes
    ----------
    icon_url :`None`, `str`
        Url of the embed footer's icon.
    icon_proxy_url : `None`, `str`
        A proxied url of the embed footer's icon.
    text : `None`, `str`
        The embed footer's text.
    """
    __slots__ = ('icon_url', 'icon_proxy_url', 'text')
    
    def __new__(cls, text = ..., icon_url = ...):
        """
        Creates a new embed field with the given parameters.
        
        Parameters
        ----------
        text : `None`, `str`, Optional
            The footer's text.
        icon_url : `None`, `str`, Optional
            An url of the footer's icon. Can be http(s) or attachment.
        
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
        
        # text
        if text is ...:
            text = None
        else:
            text = validate_text(text)
        
        self = object.__new__(cls)
        self.icon_url = icon_url
        self.icon_proxy_url = None
        self.text = text
        return self
    
    
    @copy_docs(EmbedFieldBase.__len__)
    def __len__(self):
        length = 0
        
        # text
        text = self.text
        if (text is not None):
            length += len(text)
        
        return length
    
    
    @copy_docs(EmbedFieldBase.__bool__)
    def __bool__(self):
        # icon_url
        if (self.icon_url is not None):
            return True
        
        # text
        if self.text is not None:
            return True
        
        return False
    
    
    @copy_docs(EmbedFieldBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        field_added = False
        
        text = self.text
        if text is not None:
            field_added = True
            repr_parts.append(' text = ')
            repr_parts.append(repr(self.text))
        
        icon_url = self.icon_url
        if icon_url is not None:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' icon_url = ')
            repr_parts.append(repr(url_cutter(icon_url)))
    
    
    @copy_docs(EmbedFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # icon_url
        icon_url = self.icon_url
        if (icon_url is not None):
            hash_value ^= hash(icon_url)
        
        # text
        text = self.text
        if (text is not None):
            hash_value ^= hash(text)
        
        return hash_value
    
    
    @copy_docs(EmbedFieldBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # icon_url
        if self.icon_url != other.icon_url:
            return False
        
        # text
        if self.text != other.text:
            return False
        

        return True
    
    
    @classmethod
    @copy_docs(EmbedFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.icon_url = parse_icon_url(data)
        self.icon_proxy_url = parse_icon_proxy_url(data)
        self.text = parse_text(data)
        return self
    
    
    @copy_docs(EmbedFieldBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_icon_url_into(self.icon_url, data, defaults)
        put_text_into(self.text, data, defaults)
        
        if include_internals:
            put_icon_proxy_url_into(self.icon_proxy_url, data, defaults)
        
        return data
    
    
    @copy_docs(EmbedFieldBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        new.icon_url = self.icon_url
        new.icon_proxy_url = self.icon_proxy_url
        new.text = sanitize_mentions(self.text, guild)
        return new
    
    
    @copy_docs(EmbedFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.icon_url = self.icon_url
        new.icon_proxy_url = self.icon_proxy_url
        new.text = self.text
        return new
    
    
    def copy_with(self, *, icon_url = ..., text = ...):
        """
        Copies the embed footer with the given parameters.
        
        Parameters
        ----------
        icon_url : `None`, `str`, Optional (Keyword only)
            An url of the footer's icon. Can be http(s) or attachment.
        text : `None`, `str`, Optional (Keyword only)
            The footer's text.
        
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
        
        # text
        if text is ...:
            text = self.text
        else:
            text = validate_text(text)
        
        new = object.__new__(type(self))
        new.icon_url = icon_url
        new.icon_proxy_url = icon_proxy_url
        new.text = text
        return new
    
    
    @copy_docs(EmbedFieldBase.iter_contents)
    def iter_contents(self):
        text = self.text
        if (text is not None):
            yield text
    
    
    @property
    def proxy_icon_url(self):
        """
        Deprecated and will be removed in 2023 august. Please use ``.icon_proxy_url``.
        """
        warnings.warn(
            (
                f'`{type(self).__text__}.proxy_icon_url` is deprecated and will be removed in 2023 august. '
                f'Please use `.icon_proxy_url` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
    
        return self.icon_proxy_url
