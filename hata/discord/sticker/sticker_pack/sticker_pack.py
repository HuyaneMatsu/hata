__all__ = ('StickerPack', )

from scarletio import export

from ...bases import DiscordEntity
from ...core import STICKER_PACKS
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_banner_id, parse_cover_sticker_id, parse_description, parse_id, parse_name, parse_sku_id, parse_stickers,
    put_banner_id_into, put_cover_sticker_id_into, put_description_into, put_id_into, put_name_into, put_sku_id_into,
    put_stickers_into, validate_banner_id, validate_cover_sticker_id, validate_description, validate_id, validate_name,
    validate_sku_id, validate_stickers
)


PRECREATE_FIELDS = {
    'banner_id': ('banner_id', validate_banner_id),
    'cover_sticker': ('cover_sticker_id', validate_cover_sticker_id),
    'cover_sticker_id': ('cover_sticker_id', validate_cover_sticker_id),
    'description': ('description', validate_description),
    'name': ('name', validate_name),
    'sku_id': ('sku_id', validate_sku_id),
    'stickers': ('stickers', validate_stickers),
}


@export
class StickerPack(DiscordEntity, immortal = True):
    """
    A sticker's pack.
    
    Attributes
    ----------
    banner_id : `int`
        The banner asset identifier of the sticker pack.
    cover_sticker_id : `int`
        The sticker's identifier, which the pack uses as it's banner. Defaults to `0` if not applicable.
    description : `str`
        The pack's description.
    id : `int`
        The sticker pack's identifier.
    name : `str`
        The name of the sticker pack.
    sku_id : `int`
        The Stock Keeping Unit identifier of the sticker pack.
    stickers : `None`, `frozenset` of ``Sticker``
        The stickers of the pack.
    """
    __slots__ = ('banner_id', 'cover_sticker_id', 'description', 'name', 'sku_id', 'stickers')
    
    
    def __new__(
        cls,
        *,
        banner_id = ...,
        cover_sticker_id = ...,
        description = ...,
        name = ...,
        sku_id = ...,
        stickers = ...,
    ):
        """
        Creates a new partial sticker pack.
        
        Parameters
        ----------
        banner_id : `int`, Optional (Keyword only)
            The banner asset identifier of the sticker pack.
        cover_sticker_id : `int`, ``Sticker``, Optional (Keyword only)
            The sticker's identifier, which the pack uses as it's banner.
        description : `None`, `str`, Optional (Keyword only)
            The pack's description.
        name : `str`, Optional (Keyword only)
            The name of the sticker pack.
        sku_id : `int`, Optional (Keyword only)
            The Stock Keeping Unit identifier of the sticker pack.
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers of the pack.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # banner_id
        if banner_id is ...:
            banner_id = 0
        else:
            banner_id = validate_banner_id(banner_id)
        
        # cover_sticker_id
        if cover_sticker_id is ...:
            cover_sticker_id = 0
        else:
            cover_sticker_id = validate_cover_sticker_id(cover_sticker_id)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # sku_id
        if sku_id is ...:
            sku_id = 0
        else:
            sku_id = validate_sku_id(sku_id)
        
        # stickers
        if stickers is ...:
            stickers = None
        else:
            stickers = validate_stickers(stickers)
        
        # Construct
        
        self = object.__new__(cls)
        self.banner_id = banner_id
        self.cover_sticker_id = cover_sticker_id
        self.description = description
        self.id = 0
        self.name = name
        self.sku_id = sku_id
        self.stickers = stickers
        return self
    
    
    @classmethod
    def from_data(cls, data, *, force_update = False):
        """
        Creates a new ``StickerPack`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            sticker-pack data.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker should be updated.
        
        Returns
        -------
        self : `instance<cls>`
        """
        sticker_pack_id = parse_id(data)
        
        try:
            self = STICKER_PACKS[sticker_pack_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sticker_pack_id
            self._set_attributes(data)
            STICKER_PACKS[sticker_pack_id] = self
        
        else:
            if force_update:
                self._set_attributes(data)
        
        return self
    
    
    def _set_attributes(self, data):
        """
        Sets the sticker pack's attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Sticker-pack data.
        """
        self.banner_id = parse_banner_id(data)
        self.cover_sticker_id = parse_cover_sticker_id(data)
        self.description = parse_description(data)
        self.name = parse_name(data)
        self.sku_id = parse_sku_id(data)
        self.stickers = parse_stickers(data)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the sticker pack to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_banner_id_into(self.banner_id, data, defaults)
        put_cover_sticker_id_into(self.cover_sticker_id, data, defaults)
        put_description_into(self.description, data, defaults)
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        put_sku_id_into(self.sku_id, data, defaults)
        put_stickers_into(self.stickers, data, defaults)
        return data
    
    
    @classmethod
    def precreate(cls, sticker_pack_id, **keyword_parameters):
        """
        Precreates the sticker pack with the given parameters. When the sticker pack is loaded, the precreated one
        will be picked up and its fields will be populated.
        
        > Since sticker-packs are not bound to any other objects, it cannot be determined whether they are up-to-date.
        > Meaning their attributes are not locked if the sticker is already loaded and can be changed with `.precreate`.
        
        Parameters
        ----------
        sticker_pack_id : `int`
            The sticker pack's id.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the sticker pack.
        
        Other Parameters
        ----------------
        banner_id : `int`, Optional (Keyword only)
            The banner asset identifier of the sticker pack.
        cover_sticker : `int`, ``Sticker``, Optional (Keyword only)
            Alternative for `cover_sticker_id`.
        cover_sticker_id : `int`, ``Sticker``, Optional (Keyword only)
            The sticker's identifier, which the pack uses as it's banner.
        description : `None`, `str`, Optional (Keyword only)
            The pack's description.
        name : `str`, Optional (Keyword only)
            The name of the sticker pack.
        sku_id : `int`, Optional (Keyword only)
            The Stock Keeping Unit identifier of the sticker pack.
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers of the pack.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - A parameter's type is incorrect.
            - Extra parameters given.
        ValueError
            - A parameter's value is incorrect.
        """
        sticker_pack_id = validate_id(sticker_pack_id)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = STICKER_PACKS[sticker_pack_id]
        except KeyError:
            self = cls._create_empty(sticker_pack_id)
            STICKER_PACKS[sticker_pack_id] = self
        else:
            if not self.partial:
                return self
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, sticker_pack_id):
        """
        Creates a sticker pack with its default field values set.
        
        Parameters
        ----------
        sticker_pack_id : `int`
            The identifier of the sticker pack.
        
        Returns
        -------
        sticker_pack : `instance<cls>`
        """
        self = object.__new__(cls)
        self.banner_id = 0
        self.cover_sticker_id = 0
        self.description = None
        self.id = sticker_pack_id
        self.name = ''
        self.sku_id = 0
        self.stickers = None
        return self
    
    
    def __repr__(self):
        """Returns the sticker pack's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        emoji_id = self.id
        if emoji_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two sticker packs are equal"""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two sticker packs are not equal"""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two sticker packs are equal. Type of `other` must match type of `self`.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other sticker ack to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return (self_id == other_id)
        
        # banner_id
        if self.banner_id != other.banner_id:
            return False
        
        # cover_sticker_id
        if self.cover_sticker_id != other.cover_sticker_id:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # sku_id
        if self.sku_id != other.sku_id:
            return False
        
        # stickers
        if self.stickers != other.stickers:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the sticker pack's hash."""
        emoji_id = self.id
        if emoji_id:
            return emoji_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial sticker pack's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # banner_id
        hash_value ^= hash(self.banner_id)
        
        # cover_sticker_id
        hash_value ^= hash(self.cover_sticker_id)
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # name
        hash_value ^= hash(self.name)
        
        # sku_id
        hash_value ^= hash(self.sku_id)
        
        # stickers
        stickers = self.stickers
        if (stickers is not None):
            hash_value ^= len(stickers)
            
            for sticker in stickers:
                hash_value ^= hash(sticker)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the sticker pack.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.banner_id = self.banner_id
        new.cover_sticker_id = self.cover_sticker_id
        new.description = self.description
        new.id = 0
        new.name = self.name
        new.sku_id = self.sku_id
        stickers = self.stickers
        if (stickers is not None):
            stickers = frozenset(iter(stickers))
        new.stickers = stickers
        return new
    
    
    def copy_with(
        self,
        *,
        banner_id = ...,
        cover_sticker_id = ...,
        description = ...,
        name = ...,
        sku_id = ...,
        stickers = ...,
    ):
        """
        Copies the sticker pack with the given fields.
        
        Parameters
        ----------
        banner_id : `int`, Optional (Keyword only)
            The banner asset identifier of the sticker pack.
        cover_sticker_id : `int`, ``Sticker``, Optional (Keyword only)
            The sticker's identifier, which the pack uses as it's banner.
        description : `None`, `str`, Optional (Keyword only)
            The pack's description.
        name : `str`, Optional (Keyword only)
            The name of the sticker pack.
        sku_id : `int`, Optional (Keyword only)
            The Stock Keeping Unit identifier of the sticker pack.
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers of the pack.
        
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
        # banner_id
        if banner_id is ...:
            banner_id = self.banner_id
        else:
            banner_id = validate_banner_id(banner_id)
        
        # cover_sticker_id
        if cover_sticker_id is ...:
            cover_sticker_id = self.cover_sticker_id
        else:
            cover_sticker_id = validate_cover_sticker_id(cover_sticker_id)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # sku_id
        if sku_id is ...:
            sku_id = self.sku_id
        else:
            sku_id = validate_sku_id(sku_id)
        
        # stickers
        if stickers is ...:
            stickers = self.stickers
            if (stickers is not None):
                stickers = frozenset(iter(stickers))
        else:
            stickers = validate_stickers(stickers)
        
        # Construct
        
        new = object.__new__(type(self))
        new.banner_id = banner_id
        new.cover_sticker_id = cover_sticker_id
        new.description = description
        new.id = 0
        new.name = name
        new.sku_id = sku_id
        new.stickers = stickers
        return new
    
    
    banner_url = property(module_urls.sticker_pack_banner)
    
    
    @property
    def partial(self):
        """
        Returns whether the sticker pack is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return self.id == 0
    
    
    def iter_stickers(self):
        """
        Iterates over the stickers of the sticker pack.
        
        This method is an iterable generator.
        
        Yields
        ------
        sticker : ``Sticker``
        """
        stickers = self.stickers
        if (stickers is not None):
            yield from stickers
    
    
    def has_sticker(self, sticker):
        """
        Returns whether the sticker pack contains the given sticker.
        
        Parameters
        ----------
        sticker : ``Sticker``
            The sticker to check for.
        
        Returns
        -------
        has_sticker : `bool`
        """
        stickers = self.stickers
        if (stickers is None):
            return False
        
        return (sticker in stickers)
