__all__ = ('ThirdPartySKU',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_distributor, parse_id, parse_sku, put_distributor_into, put_id_into, put_sku_into, validate_distributor,
    validate_id, validate_sku
)


class ThirdPartySKU(RichAttributeErrorBaseType):
    """
    Represents a third party Stock Keeping Unit.
    
    Attributes
    ----------
    distributor : `str`
        The distributor of the SKU.
    id : `str`
        The identifier of the third party SKU.
    sku : `str`
        Stock keeping unit. Might be same as ``.id``.
    """
    __slots__ = ('distributor', 'id', 'sku')
    
    def __new__(cls, *, distributor = ..., sku_id = ..., sku = ...):
        """
        Creates an sku.
        
        Parameters
        ----------
        distributor : `str`, Optional (Keyword only)
            The distributor of the SKU.
        
        sku_id : `str`, Optional (Keyword only)
            The identifier of the third party SKU.
        
        sku : `str`, Optional (Keyword only)
            Stock keeping unit.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # distributor
        if distributor is ...:
            distributor = ''
        else:
            distributor = validate_distributor(distributor)
        
        # id
        if sku_id is ...:
            sku_id = ''
        else:
            sku_id = validate_id(sku_id)
        
        # sku
        if sku is ...:
            sku = ''
        else:
            sku = validate_sku(sku)
        
        self = object.__new__(cls)
        self.distributor = distributor
        self.id = sku_id
        self.sku = sku
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new sku with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Executable data.
        """
        self = object.__new__(cls)
        self.distributor = parse_distributor(data)
        self.id = parse_id(data)
        self.sku = parse_sku(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the sku to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        put_distributor_into(self.distributor, data, defaults)
        put_id_into(self.id, data, defaults)
        put_sku_into(self.sku, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the sku's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        repr_parts.append(', distributor = ')
        repr_parts.append(repr(self.distributor))
        
        repr_parts.append(', id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append(', sku = ')
        repr_parts.append(repr(self.sku))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two sku-s are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # distributor
        if self.distributor != other.distributor:
            return False
        
        # id
        if self.id != other.id:
            return False
        
        # sku
        if self.sku != other.sku:
            return False
        
        return True
    
    
    def __gt__(self, other):
        """Returns whether self is greater than the other sku."""
        if type(self) is not type(other):
            return NotImplemented
        
        # distributor
        self_distributor = self.distributor
        other_distributor = other.distributor
        if self_distributor > other_distributor:
            return True
        
        if self_distributor < other_distributor:
            return False
        
        # sku
        self_sku = self.sku
        other_sku = other.sku
        if self_sku > other_sku:
            return True
        
        if self_sku < other_sku:
            return False
        
        # id
        return (self.id > other.id)
    
    
    def __hash__(self):
        """Returns the sku's hash."""
        hash_value = 0
        
        # distributor
        hash_value ^= hash(self.distributor)
        
        # id
        sku_id = self.id
        hash_value ^= hash(sku_id)
        
        # sku
        sku = self.sku
        if sku != sku_id:
            hash_value ^= hash(sku)
        
        return hash_value

    
    def copy(self):
        """
        Copies the sku.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.distributor = self.distributor
        new.id = self.id
        new.sku = self.sku
        return new
    
    
    def copy_with(self, *, distributor = ..., sku_id = ..., sku = ...):
        """
        Copies the sku with the given fields.
        
        Parameters
        ----------
        distributor : `str`, Optional (Keyword only)
            The distributor of the SKU.
        
        sku_id : `str`, Optional (Keyword only)
            The identifier of the third party SKU.
        
        sku : `str`, Optional (Keyword only)
            Stock keeping unit.
        
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
        # distributor
        if distributor is ...:
            distributor = self.distributor
        else:
            distributor = validate_distributor(distributor)
        
        # id
        if sku_id is ...:
            sku_id = self.id
        else:
            sku_id = validate_id(sku_id)
        
        # sku
        if sku is ...:
            sku = self.sku
        else:
            sku = validate_sku(sku)
        
        new = object.__new__(type(self))
        new.distributor = distributor
        new.id = sku_id
        new.sku = sku
        return new
