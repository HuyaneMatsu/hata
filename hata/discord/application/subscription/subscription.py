__all__ = ('Subscription',)

from ...bases import DiscordEntity
from ...core import SUBSCRIPTIONS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import create_partial_user_from_id

from .fields import (
    parse_cancelled_at, parse_country_code, parse_current_period_end, parse_current_period_start, parse_entitlement_ids,
    parse_id, parse_sku_ids, parse_status, parse_user_id, put_cancelled_at_into, put_country_code_into,
    put_current_period_end_into, put_current_period_start_into, put_entitlement_ids_into, put_id_into, put_sku_ids_into,
    put_status_into, put_user_id_into, validate_cancelled_at, validate_country_code, validate_current_period_end,
    validate_current_period_start, validate_entitlement_ids, validate_id, validate_sku_ids, validate_status,
    validate_user_id
)
from .preinstanced import SubscriptionStatus


PRECREATE_FIELDS = {
    'cancelled_at': ('cancelled_at', validate_cancelled_at),
    'country_code': ('country_code', validate_country_code),
    'current_period_end': ('current_period_end', validate_current_period_end),
    'current_period_start': ('current_period_start', validate_current_period_start),
    'entitlement_ids': ('entitlement_ids', validate_entitlement_ids),
    'sku_ids': ('sku_ids', validate_sku_ids),
    'status': ('status', validate_status),
    'user': ('user_id', validate_user_id),
    'user_id': ('user_id', validate_user_id),
}


class Subscription(DiscordEntity):
    """
    Represents a subscription.
    
    Attributes
    ----------
    cancelled_at : `None | DateTime`
        Whether and when the subscription was cancelled.
    
    country_code : `None | str`
        `ISO3166-1` country code. Present when queried through oauth2.
    
    current_period_end : `None | Datetime`
        When the current subscription period ends.
    
    current_period_start : `None | DateTime`
        When the current subscription period started.
    
    entitlement_ids : `None | tuple<int>`
        The entitlements granted with this subscription.
    
    id : `int`
        The subscription's identifier.
    
    sku_ids : `None | tuple<int>`
        The third party stock keeping unit the subscription is linked to.
    
    status : ``SubscriptionStatus``
        The subscription's status.
    
    user_id : `int`
        The subscribed user's identifier.
    """
    __slots__ = (
        '__weakref__', 'cancelled_at', 'country_code', 'current_period_end', 'current_period_start', 'entitlement_ids',
        'sku_ids', 'status', 'user_id'
     )
    
    
    def __new__(cls, *, entitlement_ids = ..., sku_ids = ..., user_id = ...):
        """
        Creates a new partial subscription.
        
        Parameters
        ----------
        entitlement_ids : `None | iterable<int> | iterable<Entitlement>`, Optional (Keyword only)
            The entitlements granted with this subscription.
        
        sku_ids : `None | iterable<int> | iterable<SKU>`, Optional (Keyword only)
            The third party stock keeping unit the subscription is linked to.
        
        user_id : `int | ClientUserBase`, Optional (Keyword only)
            The subscribed user's identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # entitlement_ids
        if entitlement_ids is ...:
            entitlement_ids = None
        else:
            entitlement_ids = validate_entitlement_ids(entitlement_ids)
        
        # sku_ids
        if sku_ids is ...:
            sku_ids = None
        else:
            sku_ids = validate_sku_ids(sku_ids)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self.cancelled_at = None
        self.country_code = None
        self.current_period_end = None
        self.current_period_start = None
        self.entitlement_ids = entitlement_ids
        self.id = 0
        self.sku_ids = sku_ids
        self.status = SubscriptionStatus.active
        self.user_id = user_id
        return self
    
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new subscription from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Subscription data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        subscription_id = parse_id(data)
        
        try:
            self = SUBSCRIPTIONS[subscription_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = subscription_id
            self._set_attributes(data)
            SUBSCRIPTIONS[subscription_id] = self
        else:
            self._set_attributes(data)
        
        return self
    
    
    @classmethod
    def from_data_is_created(cls, data):
        """
        Creates a new subscription 
        
        Parameters
        ----------
        data : `dict<str, object>`
            Subscription data.
        
        Returns
        -------
        new : `instance<cls>`
        created : `bool`
        """
        subscription_id = parse_id(data)
        
        try:
            self = SUBSCRIPTIONS[subscription_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = subscription_id
            self._set_attributes(data)
            SUBSCRIPTIONS[subscription_id] = self
            created = True
        else:
            self._set_attributes(data)
            created = False
        
        return self, created
    
    
    def _set_attributes(self, data):
        """
        Sets the subscription's attributes from the given data. (Except `.id`.)
        
        Parameters
        ----------
        data : `dict<str, object>`
            Subscription data.
        """
        self.entitlement_ids = parse_entitlement_ids(data)
        self.sku_ids = parse_sku_ids(data)
        self.user_id = parse_user_id(data)
        
        self._update_attributes(data)
    

    
    def _update_attributes(self, data):
        """
        Updates the subscription by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Subscription data.
        """
        self.cancelled_at = parse_cancelled_at(data)
        self.country_code = parse_country_code(data)
        self.current_period_end = parse_current_period_end(data)
        self.current_period_start = parse_current_period_start(data)
        self.status = parse_status(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the attributes of the subscription and returns the changed ones within an `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Subscription data.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            The updated attributes.
            
            The returned dictionary might contain the following items:
            
            +---------------------------+-----------------------------------------------+
            | Key                       | Value                                         |
            +===========================+===============================================+
            | cancelled_at              | `None`, `DateTime`                            |
            +---------------------------+-----------------------------------------------+
            | country_code              | `None`, `str`                                 |
            +---------------------------+-----------------------------------------------+
            | current_period_end        | `None`, `DateTime`                            |
            +---------------------------+-----------------------------------------------+
            | current_period_start      | `None`, `DateTime`                            |
            +---------------------------+-----------------------------------------------+
            | status                    | ``SubscriptionStatus``                        |
            +---------------------------+-----------------------------------------------+
        """
        old_attributes = {}
        
        
        # cancelled_at
        cancelled_at = parse_cancelled_at(data)
        if self.cancelled_at != cancelled_at:
            old_attributes['cancelled_at'] = self.cancelled_at
            self.cancelled_at = cancelled_at
    
        
        # country_code
        country_code = parse_country_code(data)
        if self.country_code != country_code:
            old_attributes['country_code'] = self.country_code
            self.country_code = country_code
        
        # current_period_end
        current_period_end = parse_current_period_end(data)
        if self.current_period_end != current_period_end:
            old_attributes['current_period_end'] = self.current_period_end
            self.current_period_end = current_period_end
        
        # current_period_start
        current_period_start = parse_current_period_start(data)
        if self.current_period_start != current_period_start:
            old_attributes['current_period_start'] = self.current_period_start
            self.current_period_start = current_period_start
        
        # status
        status = parse_status(data)
        if self.status is not status:
            old_attributes['status'] = self.status
            self.status = status
        
        return old_attributes
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the subscription into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_cancelled_at_into(self.cancelled_at, data, defaults)
        put_country_code_into(self.country_code, data, defaults)
        put_current_period_end_into(self.current_period_end, data, defaults)
        put_current_period_start_into(self.current_period_start, data, defaults)
        put_entitlement_ids_into(self.entitlement_ids, data, defaults)
        put_id_into(self.id, data, defaults)
        put_sku_ids_into(self.sku_ids, data, defaults)
        put_status_into(self.status, data, defaults)
        put_user_id_into(self.user_id, data, defaults)
        
        return data
    
    
    @classmethod
    def _create_empty(cls, subscription_id):
        """
        Creates a new subscription instance with it's attribute set to their default values.
        
        Parameters
        ----------
        subscription_id : `int`
            The subscription's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.cancelled_at = None
        self.country_code = None
        self.current_period_end = None
        self.current_period_start = None
        self.entitlement_ids = None
        self.id = subscription_id
        self.sku_ids = None
        self.status = SubscriptionStatus.active
        self.user_id = 0
        return self
    
    
    @classmethod
    def precreate(cls, subscription_id, **keyword_parameters):
        """
        Creates an subscription instance.
        
        Parameters
        ----------
        subscription_id : `int`
            The subscription's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        cancelled_at : `None | DateTime`, Optional (Keyword only)
            Whether and when the subscription was cancelled.
        
        country_code : `None | str`, Optional (Keyword only)
            `ISO3166-1` country code. Present when queried through oauth2.
        
        current_period_end : `None | Datetime`, Optional (Keyword only)
            When the current subscription period ends.
        
        current_period_start : `None | DateTime`, Optional (Keyword only)
            When the current subscription period started.
        
        entitlement_ids : `None | iterable<int> | iterable<Entitlement>`, Optional (Keyword only)
            The entitlements granted with this subscription.
        
        sku_ids : `None | iterable<int> | iterable<SKU>`, Optional (Keyword only)
            The third party stock keeping unit the subscription is linked to.
        
        status : `SubscriptionStatus | int`, Optional (Keyword only)
            The subscription's status.
        
        user : `int | ClientUserBase`, Optional (Keyword only)
            Alternative for `user_id`.
        
        user_id : `int | ClientUserBase`, Optional (Keyword only)
            The subscribed user's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        subscription_id = validate_id(subscription_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = SUBSCRIPTIONS[subscription_id]
        except KeyError:
            self = cls._create_empty(subscription_id)
            SUBSCRIPTIONS[subscription_id] = self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    

    def __repr__(self):
        """Returns the subscription's representation."""
        repr_parts = ['<', type(self).__name__]
        
        subscription_id = self.id
        if subscription_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two subscriptions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two subscriptions are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self.id != other.id:
                return False
        
        # cancelled_at -> ignore, internal
        # country_code -> ignore, internal
        # current_period_end -> ignore, internal
        # current_period_start -> ignore, internal
        
        # entitlement_ids
        if self.entitlement_ids != other.entitlement_ids:
            return False
        
        # sku_ids
        if self.sku_ids != other.sku_ids:
            return False
        
        # status -> ignore, internal
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the subscription."""
        subscription_id = self.id
        if subscription_id:
            return subscription_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Calculates the subscription's hash based on their fields.
        
        This method is called by ``.__hash__`` if the channel has no ``.id`` set.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # cancelled_at -> ignore, internal
        # country_code -> ignore, internal
        # current_period_end -> ignore, internal
        # current_period_start -> ignore, internal
        
        # entitlement_ids
        entitlement_ids = self.entitlement_ids
        if (entitlement_ids is not None):
            hash_value ^= len(entitlement_ids) << 4
            
            for entitlement_id in entitlement_ids:
                hash_value ^= hash(entitlement_id)
        
        # id -> ignore, internal
        
        # sku_ids
        sku_ids = self.sku_ids
        if (sku_ids is not None):
            hash_value ^= len(sku_ids) << 4
            
            for sku_id in sku_ids:
                hash_value ^= hash(sku_id)
        
        # status -> ignore, internal
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the subscription.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.cancelled_at = None
        new.country_code = None
        new.current_period_end = None
        new.current_period_start = None
        
        entitlement_ids = self.entitlement_ids
        if (entitlement_ids is not None):
            entitlement_ids = (*entitlement_ids,)
        new.entitlement_ids = entitlement_ids
          
        new.id = 0
        
        sku_ids = self.sku_ids
        if (sku_ids is not None):
            sku_ids = (*sku_ids,)
        new.sku_ids = sku_ids 
         
        new.status = SubscriptionStatus.active
        new.user_id = self.user_id
        
        return new
    
    
    def copy_with(self, *, entitlement_ids = ..., sku_ids = ..., user_id = ...):
        """
        Copies the subscription with the given fields.
        
        Parameters
        ----------
        entitlement_ids : `None | iterable<int> | iterable<Entitlement>`, Optional (Keyword only)
            The entitlements granted with this subscription.
        
        sku_ids : `None | iterable<int> | iterable<SKU>`, Optional (Keyword only)
            The third party stock keeping unit the subscription is linked to.
        
        user_id : `int | ClientUserBase`, Optional (Keyword only)
            The subscribed user's identifier.
        
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
        # entitlement_ids
        if entitlement_ids is ...:
            entitlement_ids = self.entitlement_ids
            if (entitlement_ids is not None):
                entitlement_ids = (*entitlement_ids,)
        else:
            entitlement_ids = validate_entitlement_ids(entitlement_ids)
        
        # sku_ids
        if sku_ids is ...:
            sku_ids = self.sku_ids
            if (sku_ids is not None):
                sku_ids = (*sku_ids,)
        else:
            sku_ids = validate_sku_ids(sku_ids)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        new = object.__new__(type(self))
        new.cancelled_at = None
        new.country_code = None
        new.current_period_end = None
        new.current_period_start = None
        new.entitlement_ids = entitlement_ids
        new.id = 0
        new.sku_ids = sku_ids
        new.status = SubscriptionStatus.active
        new.user_id = user_id
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the entity is partial.
        
        Returns
        -------
        partial : `bool
        """
        return (self.id == 0)
    
    
    @property
    def user(self):
        """
        The subscribed user.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
    
    
    def iter_entitlement_ids(self):
        """
        Iterates over the entitlement identifiers of the subscription.
        
        This method is an iterable generator.
        
        Yields
        ------
        entitlement_id : `int`
        """
        entitlement_ids = self.entitlement_ids
        if (entitlement_ids is not None):
            yield from entitlement_ids
    
    
    def iter_sku_ids(self):
        """
        Iterates over the stick keeping unit identifiers of the subscription.
        
        This method is an iterable generator.
        
        Yields
        ------
        sku_id : `int`
        """
        sku_ids = self.sku_ids
        if (sku_ids is not None):
            yield from sku_ids
    
    
    @property
    def sku_id(self):
        """
        Returns the first stock keeping unit identifier of the subscription.
        
        Returns
        -------
        sku_id : `int`
        """
        sku_ids = self.sku_ids
        if sku_ids:
            return sku_ids[0]
        
        return 0
