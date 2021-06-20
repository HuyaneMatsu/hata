__all__ = ('Sticker', 'StickerPack')

from ..core import STICKERS, STICKER_PACKS
from ..bases import DiscordEntity
from ..user import ZEROUSER, User
from .. import urls as module_urls

from .preinstanced import StickerFormat, StickerType


class Sticker(DiscordEntity, immortal=True):
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
    guild_id : `int`
        The guild's identifier to what the sticker is bound to. Defaults to `0` if the sticker is not bound to any
        guild.
    name : `str`
        The sticker's name.
    pack_id : `int`
        The unique identifier number of the pack from the sticker is. Defaults to `0` if the sticker is not bound to
        any pack.
    sort_value : `int`
        Value used to sort the stickers.
    tags : None` or `frozenset` of `str`
        Tags of the sticker if applicable.
    type : ``StickerType``
        The sticker's type.
    user : ``ClientUserBase``
        The use who uploaded the emoji. Defaults to ``ZEROUSER``.
    """
    __slots__ = ('description', 'format_type', 'guild_id', 'name', 'pack_id', 'sort_value', 'tags', 'type', 'user')
    
    def __new__(cls, data):
        """
        Creates a new ``Sticker`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        """
        sticker_id = int(data['id'])
        
        try:
            self = STICKERS[sticker_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = int(data['id'])
            
            pack_id = data.get('pack_id', None)
            if pack_id is None:
                pack_id = 0
            else:
                pack_id = int(pack_id)
            self.pack_id = pack_id
            
            guild_id = data.get('guild_id', None)
            if guild_id is None:
                guild_id = 0
            else:
                guild_id = int(guild_id)
            self.guild_id = guild_id
            
            self.format_type = StickerFormat.get(data.get('format_type', 0))
            self.type = StickerType.get(data['type'])
            
            try:
                user_data = data['user']
            except KeyError:
                user = ZEROUSER
            else:
                user = User(user_data)
            self.user = user
            
            self._update_no_return(data)
        
        return self
    
    
    def _update_no_return(self, data):
        """
        Updates the stickers with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        """
        self.description = data['description']
        self.name = data['name']
        self.sort_value = data.get('sort_value', 100)
    
        tags = data.get('tags', None)
        if (tags is not None):
            tags = frozenset(tags.split(', '))
        
        self.tags = tags
    
    
    def _update(self, data):
        """
        Updates the sticker with teh given data and returns the changed attributes in `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dictionary is optional.
            
            +-----------------------+-----------------------------------+
            | Keys                  | Values                            |
            +=======================+===================================+
            | description           | ``str``                           |
            +-----------------------+-----------------------------------+
            | name                  | `str`                             |
            +-----------------------+-----------------------------------+
            | sort_value            | `int`                             |
            +-----------------------+-----------------------------------+
            | tags                  | `None`  or `frozenset` of `str`   |
            +-----------------------+-----------------------------------+
        """
        old_attributes = {}
        
        description = data['description']
        if description != self.description:
            old_attributes['description'] = self.description
            self.description = description
        
        name = data['name']
        if name != self.name:
            old_attributes['name'] = self.name
            self.name = name
        
        sort_value = data.get('sort_value', 100)
        if sort_value != self.sort_value:
            old_attributes['sort_value'] = self.sort_value
            self.sort_value = sort_value
        
        tags = data.get('tags', None)
        if (tags is not None):
            tags = frozenset(tags.split(', '))
        if tags != self.tags:
            old_attributes['tags'] = self.tags
            self.tags = tags
        
        return old_attributes
    
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


class StickerPack(DiscordEntity, immortal=True):
    """
    A sticker's pack.
    
    Attributes
    ----------
    id : `int`
        The sticker pack's identifier.
    banner_id : `int`
        The banner asset identifier of the sticker pack.
    cover_sticker_id : `int`
        The sticker's identifier, which the pack uses as it's banner.
    description : `str`
        The pack's description.
    sku_id : `int`
        The Stock Keeping Unit identifier of the sticker pack.
    stickers : `frozenset` of ``Sticker``
        The stickers of the pack.
    name : `str`
        The name of the sticker pack.
    """
    __slots__ = ('banner_id', 'cover_sticker_id', 'description', 'stickers', 'sku_id', 'name')
    
    def __new__(cls, data):
        """
        Creates a new ``StickerPack`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            sticker-pack data.
        """
        sticker_pack_id = int(data['id'])
        
        try:
            self = STICKER_PACKS[sticker_pack_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sticker_pack_id
            
            self.name = data['name']
            self.sku_id = int(data['sku_id'])
            self.cover_sticker_id = int(data['cover_sticker_id'])
            self.banner_id = int(data['banner_asset_id'])
            self.description = data['description']
            
            self.stickers = frozenset(Sticker(sticker_data) for sticker_data in data['stickers'])
        
        return self
    
    def __repr__(self):
        """Returns the sticker pack's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
