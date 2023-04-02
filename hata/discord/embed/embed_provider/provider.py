__all__ = ('EmbedProvider',)

from scarletio import copy_docs

from ...utils import sanitize_mentions, url_cutter

from ..embed_field_base import EmbedFieldBase

from .fields import parse_name, parse_url, put_name_into, put_url_into, validate_name, validate_url


class EmbedProvider(EmbedFieldBase):
    """
    Represents an embed's provider.
    
    Attributes
    ----------
    name : `None`, `str`
        The name of the provider.
    url : `None`, `str`
        The url of the provider.
    """
    __slots__ = ('name', 'url')
    
    def __new__(cls, name = ..., url = ...):
        """
        Creates a new embed field with the given parameters.
        
        Parameters
        ----------
        name : `None`, `str`, Optional
            The name of the provider.
        url : `None`, `str`, Optional
            The url of the provider.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
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
        
        url = self.url
        if url is not None:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' url = ')
            repr_parts.append(repr(url_cutter(url)))
    
    
    @copy_docs(EmbedFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
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
        self.name = parse_name(data)
        self.url = parse_url(data)
        return self
    
    
    @copy_docs(EmbedFieldBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_name_into(self.name, data, defaults)
        put_url_into(self.url, data, defaults)
        
        return data
    
    
    @copy_docs(EmbedFieldBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        new.name = sanitize_mentions(self.name, guild)
        new.url = self.url
        return new
    
    
    @copy_docs(EmbedFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.name = self.name
        new.url = self.url
        return new
    
    
    def copy_with(self, *, name = ..., url = ...):
        """
        Copies the embed provider with the given parameters.
        
        Parameters
        ----------
        name : `None`, `str, Optional (Keyword only)
            The name of the provider.
        url : `None`, `str`, Optional (Keyword only)
            The url of the provider.
        
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
        new.name = name
        new.url = url
        return new
    
    
    @copy_docs(EmbedFieldBase.iter_contents)
    def iter_contents(self):
        name = self.name
        if (name is not None):
            yield name
