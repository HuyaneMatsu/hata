__all__ = ('AvatarDecoration', )

from ...bases import IconSlot, IconType, Slotted

from .fields import parse_sku_id, put_sku_id_into, validate_sku_id


AVATAR_DECORATION_ASSET = IconSlot('asset', 'asset', None, None)


class AvatarDecoration(metaclass = Slotted):
    """
    Represents a user's profile at a guild.
    
    Attributes
    ----------
    asset_hash : `int`
        The respective asset's hash in `uint128`.
    
    asset_type : ``IconType``
        The respective asset's type.
    
    sku_id : `int`
        The stock keeping unit the avatar decoration is part of.
    """
    __slots__ = ('sku_id',)
    
    asset = AVATAR_DECORATION_ASSET
    
    def __new__(
        cls,
        *,
        asset = ...,
        sku_id = ...,
    ):
        """
        Creates a new avatar decoration instance from the given parameters.
        
        Parameters
        ----------
        asset : `None`, ``Icon``, `str`, Optional (Keyword only)
            The channel's asset.
        
        sku_id : `int`, `None`, ``SKU``, Optional (Keyword only)
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
        
        # sku_id
        if sku_id is ...:
            sku_id = 0
        else:
            sku_id = validate_sku_id(sku_id)
        
        # Construct
        self = object.__new__(cls)
        self.asset = asset
        self.sku_id = sku_id
        return self
    
    
    def __repr__(self):
        """Returns the representation of the avatar decoration."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' asset = ')
        repr_parts.append(repr(self.asset))
        
        sku_id = self.sku_id
        if sku_id:
            repr_parts.append(', sku_id = ')
            repr_parts.append(repr(sku_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the avatar decoration's hash value."""
        hash_value = 0
        
        # asset
        hash_value ^= hash(self.asset)
        
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
        data : `dict` of (`str`, `object`) items
            Received avatar decoration data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._set_asset(data)
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
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        type(self).asset.put_into(self.asset, data, defaults)
        put_sku_id_into(self.sku_id, data, defaults)
        
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
        new.sku_id = self.sku_id
        return new
    
    
    def copy_with(
        self, 
        *,
        asset = ...,
        sku_id = ...,
    ):
        """
        Copies the avatar decoration and modifies the defined the defined fields of it.
        
        Parameters
        ----------
        asset : `None`, ``Icon``, `str`, Optional (Keyword only)
            The channel's asset.
        
        sku_id : `int`, `None`, ``SKU``, Optional (Keyword only)
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
        
        # sku_id
        if sku_id is ...:
            sku_id = self.sku_id
        else:
            sku_id = validate_sku_id(sku_id)
        
        # Construct
        new = object.__new__(type(self))
        new.asset = asset
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
        self.sku_id = 0
        return self
