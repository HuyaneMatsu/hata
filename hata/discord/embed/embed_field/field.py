__all__ = ('EmbedField',)

from scarletio import copy_docs

from ...utils import sanitize_mentions

from ..embed_field_base import EmbedFieldBase

from .fields import (
    parse_inline, parse_name, parse_value, put_inline_into, put_name_into, put_value_into, validate_inline,
    validate_name, validate_value
)


class EmbedField(EmbedFieldBase):
    """
    Represents an embed's author.
    
    Attributes
    ----------
    inline : `bool`
        Whether this field should display inline. Defaults to `False`.
    name : `None`, `str`
        The name of the field.
    value : `None`, `str`
        The value of the field.
    """
    __slots__ = ('value', 'name', 'inline')
    
    def __new__(cls, name = ..., value = ..., inline = ...):
        """
        Creates a new embed field with the given parameters.
        
        Parameters
        ----------
        name : `None`, `str`, Optional
            The name of the field.
        value : `None`, `str`, Optional
            The value of the field.
        inline : `bool`, Optional
            Whether this field should display inline.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # inline
        if inline is ...:
            inline = False
        else:
            inline = validate_inline(inline)
        
        # name
        if name is ...:
            name = None
        else:
            name = validate_name(name)
        
        # value
        if value is ...:
            value = None
        else:
            value = validate_value(value)
        
        self = object.__new__(cls)
        self.inline = inline
        self.name = name
        self.value = value
        return self
    
        
    @copy_docs(EmbedFieldBase.__len__)
    def __len__(self):
        length = 0
        
        # name
        name = self.name
        if (name is not None):
            length += len(name)
        
        # value
        value = self.value
        if (value is not None):
            length += len(value)
        
        return length
    
    
    @copy_docs(EmbedFieldBase.__bool__)
    def __bool__(self):
        # name
        if (self.name is not None):
            return True
        
        # value
        if (self.value is not None):
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
        
        value = self.value
        if value is not None:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' value = ')
            repr_parts.append(repr(value))
        
        inline = self.inline
        if inline:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' inline = ')
            repr_parts.append(repr(inline))
    
    
    @copy_docs(EmbedFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # inline
        hash_value ^= hash(self.inline)
        
        # name
        name = self.name
        if (name is not None):
            hash_value ^= hash(name)
        
        # value
        value = self.value
        if (value is not None) and (name != value):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    @copy_docs(EmbedFieldBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # inline
        if self.inline != other.inline:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(EmbedFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.inline = parse_inline(data)
        self.name = parse_name(data)
        self.value = parse_value(data)
        return self
    
    
    @copy_docs(EmbedFieldBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        put_inline_into(self.inline, data, defaults)
        put_name_into(self.name, data, defaults)
        put_value_into(self.value, data, defaults)
        return data
    
    
    @copy_docs(EmbedFieldBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        new.inline = self.inline
        new.name = sanitize_mentions(self.name, guild)
        new.value = sanitize_mentions(self.value, guild)
        return new
    
    @copy_docs(EmbedFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.inline = self.inline
        new.name = self.name
        new.value = self.value
        return new
    
    
    def copy_with(self, *, inline = ..., name = ..., value = ...):
        """
        Copies the embed author with the given parameters.
        
        Parameters
        ----------
        inline : `bool`, Optional (Keyword only)
            Whether this field should display inline.
        name : `None`, `str`, Optional (Keyword only)
            The name of the field.
        value : `None`, `str`, Optional (Keyword only)
            The value of the field.
        
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
        # inline
        if inline is ...:
            inline = self.inline
        else:
            inline = validate_inline(inline)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # value
        if value is ...:
            value = self.value
        else:
            value = validate_value(value)
        
        new = object.__new__(type(self))
        new.inline = inline
        new.name = name
        new.value = value
        return new
    
    
    @copy_docs(EmbedFieldBase.iter_contents)
    def iter_contents(self):
        name = self.name
        if (name is not None):
            yield name
        
        value = self.value
        if (value is not None):
            yield value
