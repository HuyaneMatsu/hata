__all__ = ('Entitlement',)

from scarletio import export

from ...bases import DiscordEntity
from ...core import ENTITLEMENTS, SKUS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_application_id, parse_consumed, parse_deleted, parse_ends_at, parse_gift_code_flags, parse_guild_id, parse_id,
    parse_promotion_id, parse_sku, parse_sku_id, parse_source_type, parse_starts_at, parse_subscription_id, parse_type,
    parse_user_id, put_application_id, put_consumed, put_deleted, put_ends_at, put_gift_code_flags, put_guild_id,
    put_id, put_owner_id, put_owner_type, put_promotion_id, put_sku, put_sku_id, put_source_type, put_starts_at,
    put_subscription_id, put_type, put_user_id, validate_application_id, validate_consumed, validate_deleted,
    validate_ends_at, validate_gift_code_flags, validate_guild_id, validate_id, validate_promotion_id, validate_sku,
    validate_sku_id, validate_source_type, validate_starts_at, validate_subscription_id, validate_type,
    validate_user_id
)
from .flags import GiftCodeFlag
from .preinstanced import EntitlementOwnerType, EntitlementSourceType, EntitlementType


PRECREATE_FIELDS = {
    'application': ('application_id', validate_application_id),
    'application_id': ('application_id', validate_application_id),
    'consumed': ('consumed', validate_consumed),
    'deleted': ('deleted', validate_deleted),
    'ends_at': ('ends_at', validate_ends_at),
    'entitlement_type': ('type', validate_type),
    'gift_code_flags': ('gift_code_flags', validate_gift_code_flags),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'promotion_id': ('promotion_id', validate_promotion_id),
    'source_type': ('source_type', validate_source_type),
    'sku': ('sku', validate_sku),
    'sku_id': ('sku_id', validate_sku_id),
    'starts_at': ('starts_at', validate_starts_at),
    'subscription': ('subscription_id', validate_subscription_id),
    'subscription_id': ('subscription_id', validate_subscription_id),
    'user': ('user_id', validate_user_id),
    'user_id': ('user_id', validate_user_id),
}


@export
class Entitlement(DiscordEntity):
    """
    Represent that a user or guild has access to a premium offer.
    
    Attributes
    ----------
    _sku : ``None | SKU``
        The stock keeping unit the entitlement grants access to.
    
    application_id : `int`
        The entitlement's owner application's identifier.
    
    consumed : `bool`
        Whether the entitlement is already consumed.
        Not applicable for subscriptions.
    
    deleted : `bool`
        Whether the entitlement is deleted.
    
    ends_at : `None | DateTime`
        When the entitlement ends.
    
    gift_code_flags : ``GiftCodeFlag``
        The flags of the gift code the entitlement is created from.
    
    guild_id : `int`
        The guild's identifier that was granted access to the stock keeping unit.
    
    id : `int`
        The unique identifier number of the entitlement.
    
    promotion_id : `int`
        The identifier of the promotion the entitlement is from.
    
    source_type : ``EntitlementSourceType``
        Where the entitlement is from.
    
    sku_id : `int`
        The stock keeping unit's identifier the this entitlement grants access to.
    
    starts_at : `None | DateTime`
        When the entitlement starts.
    
    subscription_id : `int`
        The subscription's identifier the entitlement is part of.
    
    type : ``EntitlementType``
        The entitlement's type.
    
    user_id : `int`
        The user's identifier that was granted access to the stock keeping unit.
    
    Notes
    -----
    Entitlement instances are weakreferable.
    """
    __slots__ = (
        '__weakref__', '_sku', 'application_id', 'consumed', 'deleted', 'ends_at', 'guild_id', 'gift_code_flags',
        'promotion_id', 'source_type', 'sku_id', 'starts_at', 'subscription_id', 'type', 'user_id'
    )
    
    def __new__(cls, *, guild_id = ..., sku_id = ..., user_id = ...):
        """
        Creates a new partial entitlement.
        
        Parameters
        ----------
        guild_id : ``None | int | Guild``, Optional (Keyword only)
            The guild's identifier that was granted access to the stock keeping unit.
    
        sku_id : ``None | int | SKU``, Optional (Keyword only)
            The stock keeping unit's identifier the this entitlement grants access to.
        
        user_id : ``None | int | ClientUserBase``, Optional (Keyword only)
            The user's identifier that was granted access to the stock keeping unit.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # sku_id
        if sku_id is ...:
            sku_id = 0
        else:
            sku_id = validate_sku_id(sku_id)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self._sku = None
        self.application_id = 0
        self.consumed = False
        self.deleted = False
        self.ends_at = None
        self.gift_code_flags = GiftCodeFlag()
        self.guild_id = guild_id
        self.id = 0
        self.promotion_id = 0
        self.source_type = EntitlementSourceType.none
        self.sku_id = sku_id
        self.starts_at = None
        self.subscription_id = 0
        self.type = EntitlementType.none
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new entitlement from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Entitlement data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        entitlement_id = parse_id(data)
        
        try:
            self = ENTITLEMENTS[entitlement_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = entitlement_id
            self._set_attributes(data)
            ENTITLEMENTS[entitlement_id] = self
        else:
            self._set_attributes(data)
        
        return self
    
    
    @classmethod
    def from_data_is_created(cls, data):
        """
        Creates a new entitlement 
        
        Parameters
        ----------
        data : `dict<str, object>`
            Entitlement data.
        
        Returns
        -------
        new : `instance<cls>`
        created : `bool`
        """
        entitlement_id = parse_id(data)
        
        try:
            self = ENTITLEMENTS[entitlement_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = entitlement_id
            self._set_attributes(data)
            ENTITLEMENTS[entitlement_id] = self
            created = True
        else:
            self._set_attributes(data)
            created = False
        
        return self, created
    
    
    def _set_attributes(self, data):
        """
        Sets the entitlement's attributes from the given data. (Except `.id`.)
        
        Parameters
        ----------
        data : `dict<str, object>`
            Entitlement data.
        """
        self._sku = parse_sku(data)
        self.application_id = parse_application_id(data)
        self.gift_code_flags = parse_gift_code_flags(data)
        self.guild_id = parse_guild_id(data)
        self.promotion_id = parse_promotion_id(data)
        self.source_type = parse_source_type(data)
        self.sku_id = parse_sku_id(data)
        self.subscription_id = parse_subscription_id(data)
        self.type = parse_type(data)
        self.user_id = parse_user_id(data)
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the entitlement by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Entitlement data.
        """
        self.consumed = parse_consumed(data)
        self.deleted = parse_deleted(data)
        self.ends_at = parse_ends_at(data)
        self.starts_at = parse_starts_at(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the attributes of the entitlement and returns the changed ones within an `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Entitlement data.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            The updated attributes.
            
            The returned dictionary might contain the following items:
            
            +---------------------------+-----------------------------------------------+
            | Key                       | Value                                         |
            +===========================+===============================================+
            | consumed                  | `bool`                                        |
            +---------------------------+-----------------------------------------------+
            | deleted                   | `bool`                                        |
            +---------------------------+-----------------------------------------------+
            | ends_at                   | `None | DateTime`                             |
            +---------------------------+-----------------------------------------------+
            | starts_at                 | `None | DateTime`                             |
            +---------------------------+-----------------------------------------------+
        """
        old_attributes = {}
        
        # consumed
        consumed = parse_consumed(data)
        if self.consumed != consumed:
            old_attributes['consumed'] = self.consumed
            self.consumed = consumed
        
        # deleted
        deleted = parse_deleted(data)
        if self.deleted != deleted:
            old_attributes['deleted'] = self.deleted
            self.deleted = deleted
        
        # ends_at
        ends_at = parse_ends_at(data)
        if self.ends_at != ends_at:
            old_attributes['ends_at'] = self.ends_at
            self.ends_at = ends_at
        
        # starts_at
        starts_at = parse_starts_at(data)
        if self.starts_at != starts_at:
            old_attributes['starts_at'] = self.starts_at
            self.starts_at = starts_at
        
        return old_attributes
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the entitlement into a json serializable object.
        
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
        
        put_sku_id(self.sku_id, data, defaults)
        
        if include_internals:
            put_application_id(self.application_id, data, defaults)
            put_consumed(self.consumed, data, defaults)
            put_deleted(self.deleted, data, defaults)
            put_ends_at(self.ends_at, data, defaults)
            put_gift_code_flags(self.gift_code_flags, data, defaults)
            put_guild_id(self.guild_id, data, defaults)
            put_id(self.id, data, defaults)
            put_promotion_id(self.promotion_id, data, defaults)
            put_sku(self._sku, data, defaults)
            put_source_type(self.source_type, data, defaults)
            put_starts_at(self.starts_at, data, defaults)
            put_subscription_id(self.subscription_id, data, defaults)
            put_type(self.type, data, defaults)
            put_user_id(self.user_id, data, defaults)
        else:
            put_owner_id(self.owner_id, data, defaults)
            put_owner_type(self.owner_type, data, defaults)
        
        return data
    
    
    @classmethod
    def _create_empty(cls, entitlement_id):
        """
        Creates a new entitlement instance with it's attribute set to their default values.
        
        Parameters
        ----------
        entitlement_id : `int`
            The entitlement's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._sku = None
        self.application_id = 0
        self.consumed = False
        self.deleted = False
        self.ends_at = None
        self.gift_code_flags = GiftCodeFlag()
        self.guild_id = 0
        self.id = entitlement_id
        self.promotion_id = 0
        self.source_type = EntitlementSourceType.none
        self.sku_id = 0
        self.starts_at = None
        self.subscription_id = 0
        self.type = EntitlementType.none
        self.user_id = 0
        return self
    

    @classmethod
    def precreate(cls, entitlement_id, **keyword_parameters):
        """
        Creates an entitlement instance.
        
        Parameters
        ----------
        entitlement_id : `int`
            The entitlement's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        application : ``None | int | Application``, Optional (Keyword only)
            Alternative for `application_id`.
        
        application_id : ``None | int | Application``, Optional (Keyword only)
            The entitlement's owner application's identifier.
        
        consumed : `None | bool`, Optional (Keyword only)
            Whether the entitlement is already consumed.
        
        deleted : `None | bool`, Optional (Keyword only)
            Whether the entitlement is deleted.
        
        ends_at : `None | DateTime`, Optional (Keyword only)
            When the entitlement ends.
        
        entitlement_type : ``None | int | EntitlementType``, Optional (Keyword only)
            The entitlement's type.
        
        gift_code_flags : ``None | int | GiftCodeFlag``, Optional (Keyword only)
            The flags of the gift code the entitlement is created from.
        
        guild : ``None | int | Guild``, Optional (Keyword only)
            Alternative for `guild_id`.
        
        guild_id : ``None | int | Guild``, Optional (Keyword only)
            The guild's identifier that was granted access to the stock keeping unit.
        
        promotion_id : `int`, Optional (Keyword only)
            The identifier of the promotion the entitlement is from.
        
        source_type : ``None | int | EntitlementSourceType``, Optional (Keyword only)
            Where the entitlement is from.
        
        sku : ``None | SKU``, Optional (Keyword only)
            The stock keeping unit the entitlement grants access to.
        
        sku_id : ``None | int | SKU``, Optional (Keyword only)
            The stock keeping unit's identifier the this entitlement grants access to.
    
        starts_at : `None | DateTime`, Optional (Keyword only)
            When the entitlement starts.
        
        subscription : `None | int`, Optional (Keyword only)
            Alternative for `subscription_id`.
        
        subscription_id : `None | int`, Optional (Keyword only)
            The subscription's identifier the entitlement is part of.
        
        user : ``None | int | ClientUserBase``, Optional (Keyword only)
            Alternative for `user_id`.
        
        user_id : ``None | int | ClientUserBase``, Optional (Keyword only)
            The user's identifier that was granted access to the stock keeping unit.
        
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
        entitlement_id = validate_id(entitlement_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = ENTITLEMENTS[entitlement_id]
        except KeyError:
            self = cls._create_empty(entitlement_id)
            ENTITLEMENTS[entitlement_id] = self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def __repr__(self):
        """Returns the entitlement's representation."""
        repr_parts = ['<', type(self).__name__]
        
        entitlement_id = self.id
        if entitlement_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' sku_id = ')
        repr_parts.append(repr(self.sku_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two entitlements are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two entitlements are not equal."""
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
        
        # _sku -> ignore, internal
        # application_id -> ignore, internal
        # consumed -> ignore, internal
        # deleted -> ignore, internal
        # ends_at -> ignore, internal
        # gift_code_flags -> ignore, internal
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # promotion_id -> ignore, internal
        # source_type -> ignore, internal
        
        # sku_id
        if self.sku_id != other.sku_id:
            return False
        
        # starts_at -> ignore, internal
        # subscription_id -> ignore, internal
        # type -> ignore, internal
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the entitlement."""
        entitlement_id = self.id
        if entitlement_id:
            return entitlement_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Calculates the entitlement's hash based on their fields.
        
        This method is called by ``.__hash__`` if the channel has no ``.id`` set.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # _sku -> ignore, internal
        # application_id -> ignore, internal
        # consumed -> ignore, internal
        # deleted -> ignore, internal
        # ends_at -> ignore, internal
        # gift_code_flags -> ignore, internal
        
        # guild_id
        hash_value ^= self.guild_id
        
        # id -> ignore, internal
        # promotion_id -> ignore, internal
        # source_type -> ignore, internal
        
        # sku_id
        hash_value ^= self.sku_id
        
        # starts_at -> ignore, internal
        # subscription_id -> ignore, internal
        # type -> ignore, internal
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the entitlement.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._sku = None
        new.application_id = 0
        new.consumed = False
        new.deleted = False
        new.ends_at = None
        new.gift_code_flags = GiftCodeFlag()
        new.guild_id = self.guild_id
        new.id = 0
        new.promotion_id = 0
        new.source_type = EntitlementSourceType.none
        new.sku_id = self.sku_id
        new.starts_at = None
        new.subscription_id = 0
        new.type = EntitlementType.none
        new.user_id = self.user_id
        return new
    
    
    def copy_with(self, *, guild_id = ..., sku_id = ..., user_id = ...):
        """
        Copies the entitlement with the given fields.
        
        Parameters
        ----------
        guild_id : ``None | int | Guild``, Optional (Keyword only)
            The guild's identifier that was granted access to the stock keeping unit.
    
        sku_id : ``None | int | SKU``, Optional (Keyword only)
            The stock keeping unit's identifier the this entitlement grants access to.
        
        user_id : ``None | int | ClientUserBase``, Optional (Keyword only)
            The user's identifier that was granted access to the stock keeping unit.
        
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
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # sku_id
        if sku_id is ...:
            sku_id = self.sku_id
        else:
            sku_id = validate_sku_id(sku_id)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        new = object.__new__(type(self))
        new._sku = None
        new.application_id = 0
        new.consumed = False
        new.deleted = False
        new.ends_at = None
        new.gift_code_flags = GiftCodeFlag()
        new.guild_id = guild_id
        new.id = 0
        new.promotion_id = 0
        new.source_type = EntitlementSourceType.none
        new.sku_id = sku_id
        new.starts_at = None
        new.subscription_id = 0
        new.type = EntitlementType.none
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
    def owner_id(self):
        """
        Returns the entitlement's owner's identifier.
        It is either its ``.guild_id`` or ``.user_id``.
        
        Returns
        -------
        owner_id : `int`
        """
        guild_id = self.guild_id
        if guild_id:
            return guild_id
        
        user_id = self.user_id
        if user_id:
            return user_id
        
        return 0
    
    
    @property
    def owner_type(self):
        """
        Returns the entitlement's owner type.
        
        Returns
        -------
        owner_type : ``EntitlementOwnerType``
        """
        if self.guild_id:
            return EntitlementOwnerType.guild
        
        if self.user_id:
            return EntitlementOwnerType.user
        
        return EntitlementOwnerType.none
    
    
    @property
    def sku(self):
        sku = self._sku
        if (sku is not None):
            return sku
        
        sku_id = self.sku_id
        if not sku_id:
            return None
        
        try:
            sku = SKUS[sku_id]
        except KeyError:
            return None
        
        self._sku = sku
        return sku
    
    @sku.setter
    def sku(self, sku):
        self._sku = sku
        self.sku_id = 0 if (sku is None) else sku.id 
