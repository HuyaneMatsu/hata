__all__ = ('StickerPack', )

from ..core import STICKER_PACKS
from ..bases import DiscordEntity

from .sticker import Sticker


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
        The sticker's identifier, which the pack uses as it's banner. Defaults to `0` if not applicable.
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
            self._set_attributes(data)
        
        return self
    
    
    def __repr__(self):
        """Returns the sticker pack's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
    
    
    def _set_attributes(self, data):
        """
        Sets the sticker pack's attributes.

        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker-pack data.
        """
        self.name = data['name']
        self.sku_id = int(data['sku_id'])
        
        cover_sticker_id = data.get('cover_sticker_id', None)
        if cover_sticker_id is None:
            cover_sticker_id = 0
        else:
            cover_sticker_id = int(cover_sticker_id)
        self.cover_sticker_id = cover_sticker_id
        
        self.banner_id = int(data['banner_asset_id'])
        self.description = data['description']
        self.stickers = frozenset(Sticker(sticker_data) for sticker_data in data['stickers'])
    
    
    @classmethod
    def _create_and_update(cls, data):
        """
        Updates if exists the sticker pack, created if not.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            sticker-pack data.
            
        Returns
        -------
        self : ``StickerPack``
        """
        sticker_pack_id = int(data['id'])
        
        try:
            self = STICKER_PACKS[sticker_pack_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sticker_pack_id
        
        self._set_attributes(data)
        
        return self
