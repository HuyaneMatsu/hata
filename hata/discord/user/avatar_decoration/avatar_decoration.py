__all__ = ('AvatarDecoration', )

from ...bases import IconSlot, IconType, Slotted
from ...http.urls import build_avatar_decoration_url, build_avatar_decoration_url_as
from ...utils import DATETIME_FORMAT_CODE

from .fields import parse_expires_at, parse_sku_id, put_expires_at, put_sku_id, validate_expires_at, validate_sku_id


AVATAR_DECORATION_ASSET = IconSlot('asset', 'asset')


class AvatarDecoration(metaclass = Slotted):
    """
    Represents a user's avatar's decoration.
    
    Attributes
    ----------
    asset_hash : `int`
        The respective asset's hash in `uint128`.
    
    asset_type : ``IconType``
        The respective asset's type.
    
    expires_at : `None | DateTime`
        When the decoration expires.
    
    sku_id : `int`
        The stock keeping unit the avatar decoration is part of.
    """
    __slots__ = ('expires_at', 'sku_id',)
    
    asset = AVATAR_DECORATION_ASSET
    
    def __new__(
        cls,
        *,
        asset = ...,
        expires_at = ...,
        sku_id = ...,
    ):
        """
        Creates a new avatar decoration instance from the given parameters.
        
        Parameters
        ----------
        asset : ``None | str | Icon``, Optional (Keyword only)
            The channel's asset.
        
        expires_at : `None | DateTime`, Optional (Keyword only)
            When the decoration expires.
        
        sku_id : ``None | int | SKU``, Optional (Keyword only)
            The stock keeping unit the avatar decoration is part of.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # asset
        if asset is ...:
            asset = None
        else:
            asset = cls.asset.validate_icon(asset, allow_data = True)
        
        # expires_at
        if expires_at is ...:
            expires_at = None
        else:
            expires_at = validate_expires_at(expires_at)
        
        # sku_id
        if sku_id is ...:
            sku_id = 0
        else:
            sku_id = validate_sku_id(sku_id)
        
        # Construct
        self = object.__new__(cls)
        self.asset = asset
        self.expires_at = expires_at
        self.sku_id = sku_id
        return self
    
    
    def __repr__(self):
        """Returns the representation of the avatar decoration."""
        repr_parts = ['<', type(self).__name__]
        
        # asset
        repr_parts.append(' asset = ')
        repr_parts.append(repr(self.asset))
        
        # expires_at
        expires_at = self.expires_at
        if (expires_at is not None):
            repr_parts.append(', expires_at = ')
            repr_parts.append(format(expires_at, DATETIME_FORMAT_CODE))
        
        # sku_id
        repr_parts.append(', sku_id = ')
        repr_parts.append(repr(self.sku_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the avatar decoration's hash value."""
        hash_value = 0
        
        # asset
        hash_value ^= hash(self.asset)
        
        # expires_at
        expires_at = self.expires_at
        if (expires_at is not None):
            hash_value ^= hash(expires_at)
        
        # sku_id
        hash_value ^= self.sku_id
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two avatar decorations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # asset
        if self.asset != other.asset:
            return False
        
        # expires_at
        if self.expires_at != other.expires_at:
            return False
        
        # sku_id
        if self.sku_id != other.sku_id:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a avatar decoration from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received avatar decoration data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._set_asset(data)
        self.expires_at = parse_expires_at(data)
        self.sku_id = parse_sku_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the avatar decoration to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        type(self).asset.put_into(self.asset, data, defaults)
        put_expires_at(self.expires_at, data, defaults)
        put_sku_id(self.sku_id, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the avatar decoration.
        
        Returns
        -------
        new : `instance<type<self>>
        """
        new = object.__new__(type(self))
        new.asset_hash = self.asset_hash
        new.asset_type = self.asset_type
        new.expires_at = self.expires_at
        new.sku_id = self.sku_id
        return new
    
    
    def copy_with(
        self, 
        *,
        asset = ...,
        expires_at = ...,
        sku_id = ...,
    ):
        """
        Copies the avatar decoration and modifies the defined the defined fields of it.
        
        Parameters
        ----------
        asset : ``None | str | Icon``, Optional (Keyword only)
            The channel's asset.
        
        expires_at : `None | DateTime`, Optional (Keyword only)
            When the decoration expires.
        
        sku_id : ``None | int | SKU``, Optional (Keyword only)
            The stock keeping unit the avatar decoration is part of.
        
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
        # asset
        if asset is ...:
            asset = self.asset
        else:
            asset = type(self).asset.validate_icon(asset, allow_data = True)
        
        # expires_at
        if expires_at is ...:
            expires_at = self.expires_at
        else:
            expires_at = validate_expires_at(expires_at)
        
        # sku_id
        if sku_id is ...:
            sku_id = self.sku_id
        else:
            sku_id = validate_sku_id(sku_id)
        
        # Construct
        new = object.__new__(type(self))
        new.asset = asset
        new.expires_at = expires_at
        new.sku_id = sku_id
        return new
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates a new avatar decoration with it's default attributes set.
        
        Returns
        -------
        self `instance<cls>`
        """
        self = object.__new__(cls)
        self.asset_hash = 0
        self.asset_type = IconType.none
        self.expires_at = None
        self.sku_id = 0
        return self
    
    
    @property
    def url(self):
        """
        Returns the avatar decoration's's url. If the avatar decoration has image, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_avatar_decoration_url(self.asset_type, self.asset_hash)
    
    
    def url_as(self, ext = None, size = None):
        """
        Returns the avatar decoration's's url. If the avatar decoration has no image, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_avatar_decoration_url_as(self.asset_type, self.asset_hash, ext, size)
