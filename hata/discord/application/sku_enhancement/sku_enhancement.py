__all__ = ('SKUEnhancement',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_boost_cost, parse_guild, parse_purchase_limit,
    put_boost_cost, put_guild, put_purchase_limit,
    validate_boost_cost, validate_guild,
    validate_purchase_limit
)


class SKUEnhancement(RichAttributeErrorBaseType):
    """
    Represents an applied enhancements of an SKU.
    
    Attributes
    ----------
    boost_cost : `int`
        How much boost purchasing the SKU costs.
    
    guild : ``None | SKUEnhancementGuild``
        Guild specific enhancements granted by the SKU.
    
    purchase_limit : `int`
        The purchase limit of the SKU.
    """
    __slots__ = ('boost_cost', 'guild', 'purchase_limit')
    
    def __new__(
        cls,
        *,
        boost_cost = ...,
        guild = ...,
        purchase_limit = ...,
    ):
        """
        Creates a new user SKU enhancement instance from the given parameters.
        
        Attributes
        ----------
        boost_cost : `None | int`, Optional (Keyword only)
            How much boost purchasing the SKU costs.
        
        guild : ``None | SKUEnhancementGuild``, Optional (Keyword only)
            Guild specific enhancements granted by the SKU.
        
        purchase_limit : `None | int`, Optional (Keyword only)
            The purchase limit of the SKU.
        
        """
        # boost_cost
        if boost_cost is ...:
            boost_cost = 0
        else:
            boost_cost = validate_boost_cost(boost_cost)
        
        # guild
        if guild is ...:
            guild = None
        else:
            guild = validate_guild(guild)
        
        # purchase_limit
        if purchase_limit is ...:
            purchase_limit = 0
        else:
            purchase_limit = validate_purchase_limit(purchase_limit)
        
        # Construct
        self = object.__new__(cls)
        self.boost_cost = boost_cost
        self.guild = guild
        self.purchase_limit = purchase_limit
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        # boost_cost
        boost_cost = self.boost_cost
        if boost_cost:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' boost_cost = ')
            repr_parts.append(repr(boost_cost))
        
        # guild
        guild = self.guild
        if (guild is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' guild = ')
            repr_parts.append(repr(guild))
        
        # purchase_limit
        purchase_limit = self.purchase_limit
        if purchase_limit:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' purchase_limit = ')
            repr_parts.append(repr(purchase_limit))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # boost_cost
        hash_value ^ self.boost_cost << 4
        
        # guild
        guild = self.guild
        if (guild is not None):
            hash_value ^= hash(guild)
        
        # purchase_limit
        hash_value ^= self.purchase_limit << 12
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # boost_cost
        if self.boost_cost != other.boost_cost:
            return False
        
        # guild
        if self.guild != other.guild:
            return False
        
        # purchase_limit
        if self.purchase_limit != other.purchase_limit:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a SKU enhancement from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received SKU enhancement data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.boost_cost = parse_boost_cost(data)
        self.guild = parse_guild(data)
        self.purchase_limit = parse_purchase_limit(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the SKU enhancement to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_boost_cost(self.boost_cost, data, defaults)
        put_guild(self.guild, data, defaults)
        put_purchase_limit(self.purchase_limit, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the SKU enhancement.
        
        Returns
        -------
        new : `instance<type<self>>
        """
        new = object.__new__(type(self))
        new.boost_cost = self.boost_cost
        
        # guild
        guild = self.guild
        if (guild is not None):
            guild = guild.copy()
        new.guild = guild
        
        new.purchase_limit = self.purchase_limit
        return new
    
    
    def copy_with(
        self, 
        *,
        boost_cost = ...,
        guild = ...,
        purchase_limit = ...,
    ):
        """
        Copies the SKU enhancement with the given fields.
        
        Parameters
        ----------
        boost_cost : `None | int`, Optional (Keyword only)
            How much boost purchasing the SKU costs.
        
        guild : ``None | SKUEnhancementGuild``, Optional (Keyword only)
            Guild specific enhancements granted by the SKU.
        
        purchase_limit : `None | int`, Optional (Keyword only)
            The purchase limit of the SKU.
        
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
        # boost_cost
        if boost_cost is ...:
            boost_cost = self.boost_cost
        else:
            boost_cost = validate_boost_cost(boost_cost)
        
        # guild
        if guild is ...:
            guild = self.guild
            if (guild is not None):
                guild = guild.copy()
        else:
            guild = validate_guild(guild)
        
        # purchase_limit
        if purchase_limit is ...:
            purchase_limit = self.purchase_limit
        else:
            purchase_limit = validate_purchase_limit(purchase_limit)
        
        # Construct
        new = object.__new__(type(self))
        new.boost_cost = boost_cost
        new.guild = guild
        new.purchase_limit = purchase_limit
        return new
