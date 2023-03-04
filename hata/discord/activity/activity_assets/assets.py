__all__ = ('ActivityAssets',)

from scarletio import copy_docs

from ..activity_field_base import ActivityFieldBase

from .fields import (
    parse_image_large, parse_image_small, parse_text_large, parse_text_small, put_image_large_into,
    put_image_small_into, put_text_large_into, put_text_small_into, validate_image_large, validate_image_small,
    validate_text_large, validate_text_small
)


class ActivityAssets(ActivityFieldBase):
    """
    Represents a discord activity asset.
    
    Attributes
    ----------
    image_large : `None`, `str`
        The id of the activity's large asset to display.
    image_small : `None`, `str`
        The id of the activity's small asset to display.
    text_large : `None`, `str`
        The hover text of the large asset.
    text_small : `None`, `str`
        The hover text of the small asset.
    """
    __slots__ = ('image_large', 'image_small', 'text_large', 'text_small',)
    
    def __new__(cls, *, image_large = ..., image_small = ..., text_large = ..., text_small = ...):
        """
        Creates an activity assets instance from the given parameters.
        
        Parameters
        ----------
        image_large : `None`, `str`, Optional (Keyword only)
            The id of the activity's large asset to display.
        image_small : `None`, `str`, Optional (Keyword only)
            The id of the activity's small asset to display.
        text_large : `None`, `str`, Optional (Keyword only)
            The hover text of the large asset
        text_small : `None`, `str`, Optional (Keyword only)
            The hover text of the small asset.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # image_large
        if image_large is ...:
            image_large = None
        else:
            image_large = validate_image_large(image_large)
        
        # image_small
        if image_small is ...:
            image_small = None
        else:
            image_small = validate_image_small(image_small)
        
        # text_large
        if text_large is ...:
            text_large = None
        else:
            text_large = validate_text_large(text_large)
        
        # text_small
        if text_small is ...:
            text_small = None
        else:
            text_small = validate_text_small(text_small)
        
        self = object.__new__(cls)
        self.image_large = image_large
        self.image_small = image_small
        self.text_large = text_large
        self.text_small = text_small
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.image_large = parse_image_large(data)
        self.image_small = parse_image_small(data)
        self.text_large = parse_text_large(data)
        self.text_small = parse_text_small(data)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_image_large_into(self.image_large, data, defaults)
        put_image_small_into(self.image_small, data, defaults)
        put_text_large_into(self.text_large, data, defaults)
        put_text_small_into(self.text_small, data, defaults)
        return data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        image_large = self.image_large
        if (image_large is not None):
            repr_parts.append(' image_large = ')
            repr_parts.append(repr(image_large))
            field_added = True
        else:
            field_added = False
        
        image_small = self.image_small
        if (image_small is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' image_small = ')
            repr_parts.append(repr(image_small))
        
        text_large = self.text_large
        if (text_large is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' text_large = ')
            repr_parts.append(repr(text_large))
        
        text_small = self.text_small
        if (text_small is not None):
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' text_small = ')
            repr_parts.append(repr(text_small))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.image_large != other.image_large:
            return False
        
        if self.image_small != other.image_small:
            return False
        
        if self.text_large != other.text_large:
            return False
        
        if self.text_small != other.text_small:
            return False
        
        return True
    
    
    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        image_large = self.image_large
        if (image_large is not None):
            hash_value ^= hash(image_large)
            hash_value ^= (1 << 0)
        
        image_small = self.image_small
        if (image_small is not None):
            hash_value ^= hash(image_small)
            hash_value ^= (1 << 4)
        
        text_large = self.text_large
        if (text_large is not None):
            hash_value ^= hash(text_large)
            hash_value ^= (1 << 8)
        
        text_small = self.text_small
        if (text_small is not None):
            hash_value ^= hash(text_small)
            hash_value ^= (1 << 12)
        
        return hash_value
    
    
    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        image_large = self.image_large
        if (image_large is not None):
            return True
        
        image_small = self.image_small
        if (image_small is not None):
            return True
        
        text_large = self.text_large
        if (text_large is not None):
            return True
        
        text_small = self.text_small
        if (text_small is not None):
            return True
        
        return False
    
    
    @copy_docs(ActivityFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.image_large = self.image_large
        new.image_small = self.image_small
        new.text_large = self.text_large
        new.text_small = self.text_small
        return new
    
    
    def copy_with(self, *, image_large = ..., image_small = ..., text_large = ..., text_small = ...):
        """
        Copies the activity assets with the given fields.
        
        Parameters
        ----------
        image_large : `None`, `str`, Optional (Keyword only)
            The id of the activity's large asset to display.
        image_small : `None`, `str`, Optional (Keyword only)
            The id of the activity's small asset to display.
        text_large : `None`, `str`, Optional (Keyword only)
            The hover text of the large asset
        text_small : `None`, `str`, Optional (Keyword only)
            The hover text of the small asset.
        
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
        # image_large
        if image_large is ...:
            image_large = self.image_large
        else:
            image_large = validate_image_large(image_large)
        
        # image_small
        if image_small is ...:
            image_small = self.image_small
        else:
            image_small = validate_image_small(image_small)
        
        # text_large
        if text_large is ...:
            text_large = self.text_large
        else:
            text_large = validate_text_large(text_large)
        
        # text_small
        if text_small is ...:
            text_small = self.text_small
        else:
            text_small = validate_text_small(text_small)
        
        new = object.__new__(type(self))
        new.image_large = image_large
        new.image_small = image_small
        new.text_large = text_large
        new.text_small = text_small
        return new
