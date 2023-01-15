__all__ = ('RoleManagerMetadataSubscription',)

from scarletio import copy_docs

from .integration import RoleManagerMetadataIntegration
from .fields import (
    parse_purchasable, parse_subscription_listing_id, put_purchasable_into, put_subscription_listing_id_into,
    validate_purchasable, validate_subscription_listing_id
)


class RoleManagerMetadataSubscription(RoleManagerMetadataIntegration):
    """
    Role manager metadata of a role managed by a subscription integration.
    
    Attributes
    ----------
    integration_id : `int`
        The manager integration's identifier.
    purchasable : `bool`
        Whether this role is available for purchase.
    subscription_listing_id : `int`
        The subscription listing's and sku's identifier to which the role belongs to.
    """
    __slots__ = ('purchasable', 'subscription_listing_id')
    
    def __new__(cls, *, integration_id = ..., purchasable = ..., subscription_listing_id = ...):
        """
        Creates a new role manager.
        
        Parameters
        ----------
        integration_id : `int`, ``Integration``, Optional (Keyword only)
            The manager integration's identifier.
        purchasable : `bool`, Optional (Keyword only)
            Whether this role is available for purchase.
        subscription_listing_id : `int`, Optional (Keyword only)
            The subscription listing's and sku's identifier to which the role belongs to.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # purchasable
        if purchasable is ...:
            purchasable = True
        else:
            purchasable = validate_purchasable(purchasable)
        
        # subscription_listing_id
        if subscription_listing_id is ...:
            subscription_listing_id = 0
        else:
            subscription_listing_id = validate_subscription_listing_id(subscription_listing_id)
        
        self = RoleManagerMetadataIntegration.__new__(cls, integration_id = integration_id)
        self.purchasable = purchasable
        self.subscription_listing_id = subscription_listing_id
        return self
    
    
    @classmethod
    @copy_docs(RoleManagerMetadataIntegration.from_data)
    def from_data(cls, data):
        self = super(RoleManagerMetadataSubscription, cls).from_data(data)
        self.purchasable = parse_purchasable(data)
        self.subscription_listing_id = parse_subscription_listing_id(data)
        return self
    
    
    @copy_docs(RoleManagerMetadataIntegration.to_data)
    def to_data(self, *, defaults = False):
        data = RoleManagerMetadataIntegration.to_data(self)
        put_purchasable_into(self.purchasable, data, defaults)
        put_subscription_listing_id_into(self.subscription_listing_id, data, defaults)
        return data
    
    
    @copy_docs(RoleManagerMetadataIntegration.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' integration_id = ')
        repr_parts.append(repr(self.integration_id))
        
        repr_parts.append(', purchasable = ')
        repr_parts.append(repr(self.purchasable))
        
        repr_parts.append(', subscription_listing_id = ')
        repr_parts.append(repr(self.subscription_listing_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(RoleManagerMetadataIntegration.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # integration_id
        hash_value ^= self.integration_id
        
        # purchasable
        hash_value ^= self.purchasable
        
        # subscription_listing_id
        hash_value ^= self.subscription_listing_id
        
        return hash_value
    
    
    @copy_docs(RoleManagerMetadataIntegration.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # integration_id
        if self.integration_id != other.integration_id:
            return False
        
        # purchasable
        if self.purchasable != other.purchasable:
            return False
        
        # subscription_listing_id
        if self.subscription_listing_id != other.subscription_listing_id:
            return False
        
        return True
    
    
    @copy_docs(RoleManagerMetadataIntegration.copy)
    def copy(self):
        new = RoleManagerMetadataIntegration.copy(self)
        new.purchasable = self.purchasable
        new.subscription_listing_id = self.subscription_listing_id
        return new
    
    
    def copy_with(self, *, integration_id = ..., purchasable = ..., subscription_listing_id = ...):
        """
        Copies the role manager metadata with the given fields.
        
        Parameters
        ----------
        integration_id : `int`, ``Integration``, Optional (Keyword only)
            The manager integration's identifier.
        purchasable : `bool`, Optional (Keyword only)
            Whether this role is available for purchase.
        subscription_listing_id : `int`, Optional (Keyword only)
            The subscription listing's and sku's identifier to which the role belongs to.
        
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
        # purchasable
        if purchasable is ...:
            purchasable = self.purchasable
        else:
            purchasable = validate_purchasable(purchasable)
        
        # subscription_listing_id
        if subscription_listing_id is ...:
            subscription_listing_id = self.subscription_listing_id
        else:
            subscription_listing_id = validate_subscription_listing_id(subscription_listing_id)
        
        new = RoleManagerMetadataIntegration.copy_with(self, integration_id = integration_id)
        new.purchasable = purchasable
        new.subscription_listing_id = subscription_listing_id
        return new
