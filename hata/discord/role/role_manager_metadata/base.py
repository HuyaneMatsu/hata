__all__ = ('RoleManagerMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder


class RoleManagerMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for role managers.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new role manager.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new role manager metadata from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Role manager metadata.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the role manager metadata to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        return {}
    
    
    def __repr__(self):
        """Returns the the role manager metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __hash__(self):
        """Returns the role manager metadata's hash."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two role manager metadatas are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def copy(self):
        """
        Copies the role manager metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the role manager metadata with the given fields.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return self.copy()
    
    
    @property
    def manager_id(self):
        """
        Returns the entity's identifier to which the role is managed by.
        
        Returns
        -------
        manager_id : `int`
        """
        return 0
    
    
    @property
    def manager(self):
        """
        Returns the entity's identifier to which the role is managed by.
        
        Returns
        -------
        manager : `None`, ``ClientUserBase``, ``Integration``
        """
        return None
    
    
    # place-holders
    
    bot_id = PlaceHolder(
        0,
        """
        The bot's identifier to which the role belongs to.
        
        Returns
        -------
        bot_id : `int`
        """
    )
    
    
    integration_id = PlaceHolder(
        0,
        """
        The integration's identifier to which the role belongs to.
        
        Returns
        -------
        integration_id : `int`
        """
    )
    
    
    purchasable = PlaceHolder(
        False,
        """
        Whether this role is available for purchase.
        
        Returns
        -------
        purchasable : `bool`
        """
    )
    
    
    subscription_listing_id = PlaceHolder(
        0,
        """
        The subscription listing's and sku's identifier to which the role belongs to.
        
        Returns
        -------
        subscription_listing_id : `int`
        """
    )
