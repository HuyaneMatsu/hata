__all__ = ('Sticker', )

from ..bases import DiscordEntity
from .preinstanced import StickerFormat, StickerType

from .. import urls as module_urls

class Sticker(DiscordEntity):
    """
    Represents a ``Message``'s sticker.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the sticker.
    description : `str`
        The sticker's description.
    format_type : ``StickerFormat``
        The sticker's formats type.
    name : `str`
        The sticker's name.
    pack_id : `int`
        The unique identifier number of the pack from the sticker is.
    sort_value : `int`
        Value used to sort the stickers.
    tags : None` or `list` of `str`
        Tags of the sticker if applicable.
    type : ``StickerType``
        The sticker's type.
    """
    __slots__ = ('description', 'format_type', 'name', 'pack_id', 'sort_value', 'tags', 'type')
    
    def __new__(cls, data):
        """
        Creates a new ``MessageSticker`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message sticker data.
        """
        # use `__new__`, since we might switch to caching stickers.
        self = object.__new__(cls)
        self.id = int(data['id'])
        
        self.description = data['description']
        self.name = data['name']
        
        pack_id = data.get('pack_id', None)
        if pack_id is None:
            pack_id = 0
        else:
            pack_id = int(pack_id)
        
        self.pack_id = pack_id
        
        tags = data.get('tags', None)
        if tags is not None:
            tags = tags.split(', ')
        self.tags = tags
        
        self.format_type = StickerFormat.get(data.get('format_type', 0))
        self.type = StickerType.get(data['type'])
        self.sort_value = data.get('sort_value', 100)
        
        return self
    
    def __str__(self):
        """Returns the sticker's name."""
        return self.name
    
    def __repr__(self):
        """Returns the sticker's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
    
    url = property(module_urls.sticker_url)
    url_as = module_urls.sticker_url_as
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value > other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id > other.id:
                return True
        
        return False
    
    def __ge__(self, other):
        """Returns whether self is greater or equal to other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value > other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id >= other.id:
                return True
        
        return False
    
    def __le__(self, other):
        """Returns whether self is less or equal to other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value < other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id <= other.id:
                return True
        
        return False

    def __lt__(self, other):
        """Returns whether self is less than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value < other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id < other.id:
                return True
        
        return False
