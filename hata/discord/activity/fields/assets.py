__all__ = ('ActivityAssets',)

from scarletio import copy_docs

from .base import ActivityFieldBase


def _assert__activity_secrets__image_large(image_large):
    """
    Asserts the `image_large` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    image_large : `None`, `str`
        The id of the activity's large asset to display.
    
    Raises
    ------
    AssertionError
        - If `image_large` is not `None`, `str`.
    """
    if (image_large is not None) and (not isinstance(image_large, str)):
        raise AssertionError(
            f'`image_large` can be `None`, `str`, got {image_large.__class__.__name__}; {image_large!r}.'
        )
    
    return True


def _assert__activity_secrets__image_small(image_small):
    """
    Asserts the `image_small` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    image_small : `None`, `str`
        The id of the activity's small asset to display.
    
    Raises
    ------
    AssertionError
        - If `image_small` is not `None`, `str`.
    """
    if (image_small is not None) and (not isinstance(image_small, str)):
        raise AssertionError(
            f'`image_small` can be `None`, `str`, got {image_small.__class__.__name__}; {image_small!r}.'
        )
    
    return True


def _assert__activity_secrets__text_large(text_large):
    """
    Asserts the `text_large` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    text_large : `None`, `str`
        The hover text of the large asset.
    
    Raises
    ------
    AssertionError
        - If `text_large` is not `None`, `str`.
    """
    if (text_large is not None) and (not isinstance(text_large, str)):
        raise AssertionError(
            f'`text_large` can be `None`, `str`, got {text_large.__class__.__name__}; {text_large!r}.'
        )
    
    return True


def _assert__activity_secrets__text_small(text_small):
    """
    Asserts the `text_small` parameter of ``ActivitySecrets.__new__`` method.
    
    Parameters
    ----------
    text_small : `None`, `str`
        The hover text of the small asset.
    
    Raises
    ------
    AssertionError
        - If `text_small` is not `None`, `str`.
    """
    if (text_small is not None) and (not isinstance(text_small, str)):
        raise AssertionError(
            f'`text_small` can be `None`, `str`, got {text_small.__class__.__name__}; {text_small!r}.'
        )
    
    return True


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
    
    def __new__(cls, *, image_large=None, image_small=None, text_large=None, text_small=None):
        """
        Creates a new ``ActivityAssets`` from the given parameters.
        
        Parameters
        ----------
        image_large : `None`, `str` = `None`, Optional (Keyword only)
            The id of the activity's large asset to display.
        image_small : `None`, `str` = `None`, Optional (Keyword only)
            The id of the activity's small asset to display.
        text_large : `None`, `str` = `None`, Optional (Keyword only)
            The hover text of the large asset
        text_small : `None`, `str` = `None`, Optional (Keyword only)
            The hover text of the small asset.
        
        Raises
        ------
        AssertionError
            - If `image_large` is neither `None` nor `str`.
            - If `image_small` is neither `None` nor `str`.
            - If `text_large` is neither `None` nor `str`.
            - If `text_small` is neither `None` nor `str`.
        """
        assert _assert__activity_secrets__image_large(image_large)
        assert _assert__activity_secrets__image_small(image_small)
        assert _assert__activity_secrets__text_large(text_large)
        assert _assert__activity_secrets__text_small(text_small)
        
        if (image_large is not None) and (not image_large):
            image_large = None
            
        if (image_small is not None) and (not image_small):
            image_small = None
            
        if (text_large is not None) and (not text_large):
            text_large = None
        
        if (text_small is not None) and (not text_small):
            text_small = None
        
        self = object.__new__(cls)
        self.image_large = image_large
        self.image_small = image_small
        self.text_large = text_large
        self.text_small = text_small
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, assets_data):
        self = object.__new__(cls)
        self.image_large = assets_data.get('large_image', None)
        self.image_small = assets_data.get('small_image', None)
        self.text_large = assets_data.get('large_text', None)
        self.text_small = assets_data.get('small_text', None)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
        assets_data = {}
        
        image_large = self.image_large
        if (image_large is not None):
            assets_data['large_image'] = image_large
        
        image_small = self.image_small
        if (image_small is not None):
            assets_data['small_image'] = image_small
        
        text_large = self.text_large
        if (text_large is not None):
            assets_data['large_text'] = text_large
        
        text_small = self.text_small
        if (text_small is not None):
            assets_data['small_text'] = text_small
        
        return assets_data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        image_large = self.image_large
        if (image_large is not None):
            repr_parts.append(' image_large=')
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
            repr_parts.append(' image_small=')
            repr_parts.append(repr(image_small))
        
        text_large = self.text_large
        if (text_large is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' text_large=')
            repr_parts.append(repr(text_large))
        
        text_small = self.text_small
        if (text_small is not None):
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' text_small=')
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
