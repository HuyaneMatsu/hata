__all__ = ('MessageRoleSubscription',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_renewal, parse_subscription_listing_id, parse_tier_name, parse_total_months, put_renewal_into,
    put_subscription_listing_id_into, put_tier_name_into, put_total_months_into, validate_renewal,
    validate_subscription_listing_id, validate_tier_name, validate_total_months
)


class MessageRoleSubscription(RichAttributeErrorBaseType):
    """
    Data of a subscription purchase or renewal included with a roel subscription purchase message.
    
    Parameters
    ----------
    renewal : `bool`
        Whether the purchase is a renewal.
    subscription_listing_id : `int`
        The subscription listing's and sku's identifier to which the role subscription belongs to.
    tier_name : `str`
        The name of the tier the user subscribed to.
    total_months : `int`
        The total amount months the user has been subscribed.
    """
    __slots__ = ('renewal', 'subscription_listing_id', 'tier_name', 'total_months')
    
    def __new__(cls, *, renewal = ..., subscription_listing_id = ..., tier_name = ..., total_months = ...):
        """
        Creates a new message role subscription with the given fields.
        
        Parameters
        ----------
        renewal : `bool`, Optional (Keyword only)
            Whether the purchase is a renewal.
        subscription_listing_id : `int`, Optional (Keyword only)
            The subscription listing's and sku's identifier to which the role subscription belongs to.
        tier_name : `str`, Optional (Keyword only)
            The name of the tier the user subscribed to.
        total_months : `int`, Optional (Keyword only)
            The total amount months the user has been subscribed.
        
        Raises
        ------
        TypeError
            - Parameter of invalid type given.
        ValueError
            - Parameter of invalid value given.
        """
        # renewal
        if renewal is ...:
            renewal = False
        else:
            renewal = validate_renewal(renewal)
        
        # subscription_listing_id
        if subscription_listing_id is ...:
            subscription_listing_id = 0
        else:
            subscription_listing_id = validate_subscription_listing_id(subscription_listing_id)
        
        # tier_name
        if tier_name is ...:
            tier_name = ''
        else:
            tier_name = validate_tier_name(tier_name)
        
        # total_months
        if total_months is ...:
            total_months = 1
        else:
            total_months = validate_total_months(total_months)
        
        # construct
        self = object.__new__(cls)
        self.renewal = renewal
        self.subscription_listing_id = subscription_listing_id
        self.tier_name = tier_name
        self.total_months = total_months
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message role subscription instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Message role subscription data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.renewal = parse_renewal(data)
        self.subscription_listing_id = parse_subscription_listing_id(data)
        self.tier_name = parse_tier_name(data)
        self.total_months = parse_total_months(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the message role subscription to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_renewal_into(self.renewal, data, defaults)
        put_subscription_listing_id_into(self.subscription_listing_id, data, defaults)
        put_tier_name_into(self.tier_name, data, defaults)
        put_total_months_into(self.total_months, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the message role subscription's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' tier_name = ')
        repr_parts.append(repr(self.tier_name))
        
        repr_parts.append(', renewal = ')
        repr_parts.append(repr(self.renewal))
        
        subscription_listing_id = self.subscription_listing_id
        if subscription_listing_id:
            repr_parts.append(', subscription_listing_id = ')
            repr_parts.append(repr(subscription_listing_id))
        
        total_months = self.total_months
        if (total_months != 1):
            repr_parts.append(', total_months = ')
            repr_parts.append(repr(total_months))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two message role subscriptions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # renewal
        if self.renewal != other.renewal:
            return False
        
        # parse_subscription_listing_id
        if self.subscription_listing_id != other.subscription_listing_id:
            return False
        
        # tier_name
        if self.tier_name != other.tier_name:
            return False
        
        # total_months
        if self.total_months != other.total_months:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the message role subscription."""
        hash_value = 0
        
        # renewal
        hash_value ^= self.renewal
        
        # parse_subscription_listing_id
        hash_value ^= self.subscription_listing_id
        
        # tier_name
        hash_value ^= hash(self.tier_name)
        
        # total_months
        hash_value ^= self.total_months << 2
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the role subscription listing.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.renewal = self.renewal
        new.subscription_listing_id = self.subscription_listing_id
        new.tier_name = self.tier_name
        new.total_months = self.total_months
        return new
        
        
    def copy_with(self, *, renewal = ..., subscription_listing_id = ..., tier_name = ..., total_months = ...):
        """
        Copies the role subscription listing with the given fields.
        
        Parameters
        ----------
        renewal : `bool`, Optional (Keyword only)
            Whether the purchase is a renewal.
        subscription_listing_id : `int`, Optional (Keyword only)
            The subscription listing's and sku's identifier to which the role subscription belongs to.
        tier_name : `str`, Optional (Keyword only)
            The name of the tier the user subscribed to.
        total_months : `int`, Optional (Keyword only)
            The total amount months the user has been subscribed.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Parameter of invalid type given.
        ValueError
            - Parameter of invalid value given.
        """
        # renewal
        if renewal is ...:
            renewal = self.renewal
        else:
            renewal = validate_renewal(renewal)
        
        # subscription_listing_id
        if subscription_listing_id is ...:
            subscription_listing_id = self.subscription_listing_id
        else:
            subscription_listing_id = validate_subscription_listing_id(subscription_listing_id)
        
        # tier_name
        if tier_name is ...:
            tier_name = self.tier_name
        else:
            tier_name = validate_tier_name(tier_name)
        
        if total_months is ...:
            total_months = self.total_months
        else:
            total_months = validate_total_months(total_months)
        
        # Construct
        new = object.__new__(type(self))
        new.renewal = renewal
        new.subscription_listing_id = subscription_listing_id
        new.tier_name = tier_name
        new.total_months = total_months
        return new
