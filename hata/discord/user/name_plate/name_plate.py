__all__ = ('NamePlate',)

from ...bases import Slotted
from ...http.urls import build_name_plate_url
from ...utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_asset_path, parse_name, parse_expires_at, parse_palette, parse_sku_id, put_asset_path, put_expires_at,
    put_name, put_palette, put_sku_id, validate_asset_path, validate_expires_at, validate_name, validate_palette,
    validate_sku_id
)
from .preinstanced import Palette


class NamePlate(metaclass = Slotted):
    """
    Represents a user's name's plate in a user listing.
    
    Attributes
    ----------
    asset_path : `str`
        Middle part of the path to the name plate's asset.
    
    expires_at : `None | DateTime`
        When the name plate expires.
    
    name : `str`
        The name plate's system name.
    
    palette : ``Palette``
        The dominant color of the name plate.
    
    sku_id : `int`
        The stock keeping unit the name plate is part of.
    """
    __slots__ = ('asset_path', 'expires_at', 'name', 'palette', 'sku_id',)
    
    def __new__(cls, *, asset_path = ..., expires_at = ..., name = ..., palette = ..., sku_id = ...):
        """
        Creates a new user name plate instance from the given parameters.
        
        Attributes
        ----------
        asset_path : `None | str`, Optional (Keyword only)
            Middle part of the path to the name plate's asset.
        
        expires_at : `None | DateTime`, Optional (Keyword only)
            When the name plate expires.
        
        name : `None | str`, Optional (Keyword only)
            The name plate's system name.
        
        palette : ``None | str | Palette``, Optional (Keyword only)
            The dominant color of the name plate.
        
        sku_id : `None | int`, Optional (Keyword only)
            The stock keeping unit the name plate is part of.
        """
        # asset_path
        if asset_path is ...:
            asset_path = ''
        else:
            asset_path = validate_asset_path(asset_path)
        
        # expires_at
        if expires_at is ...:
            expires_at = None
        else:
            expires_at = validate_expires_at(expires_at)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # palette
        if palette is ...:
            palette = Palette.black
        else:
            palette = validate_palette(palette)
        
        # sku_id
        if sku_id is ...:
            sku_id = 0
        else:
            sku_id = validate_sku_id(sku_id)
        
        # Construct
        self = object.__new__(cls)
        self.asset_path = asset_path
        self.expires_at = expires_at
        self.name = name
        self.palette = palette
        self.sku_id = sku_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # asset_path
        repr_parts.append(' asset_path = ')
        repr_parts.append(repr(self.asset_path))
        
        # expires_at
        expires_at = self.expires_at
        if (expires_at is not None):
            repr_parts.append(', expires_at = ')
            repr_parts.append(format(expires_at, DATETIME_FORMAT_CODE))
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # palette
        palette = self.palette
        repr_parts.append(', palette = ')
        repr_parts.append(palette.name)
        repr_parts.append(' ~ ')
        repr_parts.append(palette.value)
        
        # sku_id
        repr_parts.append(', sku_id = ')
        repr_parts.append(repr(self.sku_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # asset_path
        hash_value ^= hash(self.asset_path)
        
        # expires_at
        expires_at = self.expires_at
        if (expires_at is not None):
            hash_value ^= hash(expires_at)
        
        # name
        hash_value ^= hash(self.name)
        
        # palette
        hash_value ^= hash(self.palette)
        
        # sku_id
        hash_value ^= self.sku_id
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # asset_path
        if self.asset_path != other.asset_path:
            return False
        
        # expires_at
        if self.expires_at != other.expires_at:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # palette
        if self.palette != other.palette:
            return False
        
        # sku_id
        if self.sku_id != other.sku_id:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a name plate from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received name plate data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.asset_path = parse_asset_path(data)
        self.expires_at = parse_expires_at(data)
        self.name = parse_name(data)
        self.palette = parse_palette(data)
        self.sku_id = parse_sku_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the name plate to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_asset_path(self.asset_path, data, defaults)
        put_expires_at(self.expires_at, data, defaults)
        put_name(self.name, data, defaults)
        put_palette(self.palette, data, defaults)
        put_sku_id(self.sku_id, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the name plate.
        
        Returns
        -------
        new : `instance<type<self>>
        """
        new = object.__new__(type(self))
        new.asset_path = self.asset_path
        new.expires_at = self.expires_at
        new.name = self.name
        new.palette = self.palette
        new.sku_id = self.sku_id
        return new
    
    
    def copy_with(
        self, 
        *,
        asset_path = ...,
        expires_at = ...,
        name = ...,
        palette = ...,
        sku_id = ...,
    ):
        """
        Copies the name plate with the given fields.
        
        Parameters
        ----------
        asset_path : `None | str`, Optional (Keyword only)
            Middle part of the path to the name plate's asset.
        
        expires_at : `None | DateTime`, Optional (Keyword only)
            When the name plate expires.
        
        name : `None | str`, Optional (Keyword only)
            The name plate's system name.
        
        palette : ``None | str | Palette``, Optional (Keyword only)
            The dominant color of the name plate.
        
        sku_id : `None | int`, Optional (Keyword only)
            The stock keeping unit the name plate is part of.
        
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
        # asset_path
        if asset_path is ...:
            asset_path = self.asset_path
        else:
            asset_path = validate_asset_path(asset_path)
        
        # expires_at
        if expires_at is ...:
            expires_at = self.expires_at
        else:
            expires_at = validate_expires_at(expires_at)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # palette
        if palette is ...:
            palette = self.palette
        else:
            palette = validate_palette(palette)
        
        # sku_id
        if sku_id is ...:
            sku_id = self.sku_id
        else:
            sku_id = validate_sku_id(sku_id)
        
        # Construct
        new = object.__new__(type(self))
        new.asset_path = asset_path
        new.expires_at = expires_at
        new.name = name
        new.palette = palette
        new.sku_id = sku_id
        return new
    
    
    @property
    def url(self):
        """
        Returns the name plate's asset's url.
        
        Returns
        -------
        url : `str`
        """
        return build_name_plate_url(self.asset_path)
