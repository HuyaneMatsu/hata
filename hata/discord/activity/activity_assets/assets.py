__all__ = ('ActivityAssets',)

from scarletio import copy_docs

from ..activity_field_base import ActivityFieldBase

from .fields import (
    parse_image_large, parse_image_small, parse_text_large, parse_text_small, parse_url_large, parse_url_small,
    put_image_large, put_image_small, put_text_large, put_text_small, put_url_large, put_url_small,
    validate_image_large, validate_image_small, validate_text_large, validate_text_small, validate_url_large,
    validate_url_small
)


class ActivityAssets(ActivityFieldBase):
    """
    Represents a discord activity asset.
    
    Attributes
    ----------
    image_large : `None | str`
        The id of the activity's large asset to display.
    
    image_small : `None | str`
        The id of the activity's small asset to display.
    
    text_large : `None | str`
        The hover text of the large asset.
    
    text_small : `None | str`
        The hover text of the small asset.
    
    url_large : `None | str`
        Url to open when the user clicks on the large asset image.
    
    url_small : `None | str`
        Url to open when the user clicks on the small asset image.
    """
    __slots__ = ('image_large', 'image_small', 'text_large', 'text_small', 'url_large', 'url_small',)
    
    def __new__(
        cls,
        *,
        image_large = ...,
        image_small = ...,
        text_large = ...,
        text_small = ...,
        url_large = ...,
        url_small = ...,
    ):
        """
        Creates an activity assets instance from the given parameters.
        
        Parameters
        ----------
        image_large : `None | str`, Optional (Keyword only)
            The id of the activity's large asset to display.
        
        image_small : `None | str`, Optional (Keyword only)
            The id of the activity's small asset to display.
        
        text_large : `None | str`, Optional (Keyword only)
            The hover text of the large asset
        
        text_small : `None | str`, Optional (Keyword only)
            The hover text of the small asset.
        
        url_large : `None | str`, Optional (Keyword only)
            Url to open when the user clicks on the large asset image.
        
        url_small : `None | str`, Optional (Keyword only)
            Url to open when the user clicks on the small asset image.
        
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
        
        # url_large
        if url_large is ...:
            url_large = None
        else:
            url_large = validate_url_large(url_large)
        
        # url_small
        if url_small is ...:
            url_small = None
        else:
            url_small = validate_url_small(url_small)
        
        # Construct
        self = object.__new__(cls)
        self.image_large = image_large
        self.image_small = image_small
        self.text_large = text_large
        self.text_small = text_small
        self.url_large = url_large
        self.url_small = url_small
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.image_large = parse_image_large(data)
        self.image_small = parse_image_small(data)
        self.text_large = parse_text_large(data)
        self.text_small = parse_text_small(data)
        self.url_large = parse_url_large(data)
        self.url_small = parse_url_small(data)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_image_large(self.image_large, data, defaults)
        put_image_small(self.image_small, data, defaults)
        put_text_large(self.text_large, data, defaults)
        put_text_small(self.text_small, data, defaults)
        put_url_large(self.url_large, data, defaults)
        put_url_small(self.url_small, data, defaults)
        return data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            type(self).__name__,
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
        
        url_large = self.url_large
        if (url_large is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' url_large = ')
            repr_parts.append(repr(url_large))
        
        url_small = self.url_small
        if (url_small is not None):
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' url_small = ')
            repr_parts.append(repr(url_small))
        
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
        
        if self.url_large != other.url_large:
            return False
        
        if self.url_small != other.url_small:
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
        
        url_large = self.url_large
        if (url_large is not None):
            hash_value ^= hash(url_large)
            hash_value ^= (1 << 16)
        
        url_small = self.url_small
        if (url_small is not None):
            hash_value ^= hash(url_small)
            hash_value ^= (1 << 20)
        
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
        
        url_large = self.url_large
        if (url_large is not None):
            return True
        
        url_small = self.url_small
        if (url_small is not None):
            return True
        
        return False
    
    
    @copy_docs(ActivityFieldBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.image_large = self.image_large
        new.image_small = self.image_small
        new.text_large = self.text_large
        new.text_small = self.text_small
        new.url_large = self.url_large
        new.url_small = self.url_small
        return new
    
    
    def copy_with(
        self,
        *,
        image_large = ...,
        image_small = ...,
        text_large = ...,
        text_small = ...,
        url_large = ...,
        url_small = ...,
    ):
        """
        Copies the activity assets with the given fields.
        
        Parameters
        ----------
        image_large : `None | str`, Optional (Keyword only)
            The id of the activity's large asset to display.
        
        image_small : `None | str`, Optional (Keyword only)
            The id of the activity's small asset to display.
        
        text_large : `None | str`, Optional (Keyword only)
            The hover text of the large asset
        
        text_small : `None | str`, Optional (Keyword only)
            The hover text of the small asset.
        
        url_large : `None | str`, Optional (Keyword only)
            Url to open when the user clicks on the large asset image.
        
        url_small : `None | str`, Optional (Keyword only)
            Url to open when the user clicks on the small asset image.
        
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
        
        # url_large
        if url_large is ...:
            url_large = self.url_large
        else:
            url_large = validate_url_large(url_large)
        
        # url_small
        if url_small is ...:
            url_small = self.url_small
        else:
            url_small = validate_url_small(url_small)
        
        # Construct
        new = object.__new__(type(self))
        new.image_large = image_large
        new.image_small = image_small
        new.text_large = text_large
        new.text_small = text_small
        new.url_large = url_large
        new.url_small = url_small
        return new
