__all__ = ('IntegrationMetadataSubscription',)

from scarletio import copy_docs

from ...core import ROLES

from ..integration_account import IntegrationAccount

from .constants import EXPIRE_GRACE_PERIOD_DEFAULT, SUBSCRIBER_COUNT_DEFAULT
from .fields import (
    parse_expire_behavior, parse_expire_grace_period, parse_revoked, parse_role_id, parse_subscriber_count,
    parse_synced_at, parse_syncing, put_expire_behavior_into, put_expire_grace_period_into, put_revoked_into,
    put_role_id_into, put_subscriber_count_into, put_synced_at_into, put_syncing_into, validate_expire_behavior,
    validate_expire_grace_period, validate_revoked, validate_role_id, validate_subscriber_count, validate_synced_at,
    validate_syncing, validate_account, parse_account, put_account_into
)
from .preinstanced import IntegrationExpireBehavior

from .base import IntegrationMetadataBase


class IntegrationMetadataSubscription(IntegrationMetadataBase):
    """
    Metadata of a linked subscription integration.
    
    Attributes
    ----------
    account : ``IntegrationAccount``
        The integration's respective account.
    expire_behavior : ``IntegrationExpireBehavior``
        The behavior of expiring subscription.
    expire_grace_period : `int`
        The grace period in days for expiring subscribers.
    revoked : `bool`
        Whether the integration is removed.
    role_id : `int`
        The role's identifier what the integration uses for subscribers.
    subscriber_count : `int`
        How many subscribers the integration has.
    synced_at : `None`, `datetime`
        When the integration was last synced.
    syncing : `bool`
        Whether the integration syncing.
    """
    __slots__ = (
        'account', 'expire_behavior', 'expire_grace_period', 'revoked', 'role_id', 'subscriber_count', 'synced_at',
        'syncing'
    )
    
    @copy_docs(IntegrationMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # account
        try:
            account = keyword_parameters.pop('account')
        except KeyError:
            account = IntegrationAccount._create_empty()
        else:
            account = validate_account(account)
        
        # expire_behavior
        try:
            expire_behavior = keyword_parameters.pop('expire_behavior')
        except KeyError:
            expire_behavior = IntegrationExpireBehavior.remove_role
        else:
            expire_behavior = validate_expire_behavior(expire_behavior)
        
        # expire_grace_period
        try:
            expire_grace_period = keyword_parameters.pop('expire_grace_period')
        except KeyError:
            expire_grace_period = EXPIRE_GRACE_PERIOD_DEFAULT
        else:
            expire_grace_period = validate_expire_grace_period(expire_grace_period)
        
        # revoked
        try:
            revoked = keyword_parameters.pop('revoked')
        except KeyError:
            revoked = False
        else:
            revoked = validate_revoked(revoked)
        
        # role_id
        try:
            role_id = keyword_parameters.pop('role_id')
        except KeyError:
            role_id = 0
        else:
            role_id = validate_role_id(role_id)
        
        # subscriber_count
        try:
            subscriber_count = keyword_parameters.pop('subscriber_count')
        except KeyError:
            subscriber_count = SUBSCRIBER_COUNT_DEFAULT
        else:
            subscriber_count = validate_subscriber_count(subscriber_count)
        
        # synced_at
        try:
            synced_at = keyword_parameters.pop('synced_at')
        except KeyError:
            synced_at = None
        else:
            synced_at = validate_synced_at(synced_at)
        
        # syncing
        try:
            syncing = keyword_parameters.pop('syncing')
        except KeyError:
            syncing = False
        else:
            syncing = validate_syncing(syncing)
        
        self = object.__new__(cls)
        self.account = account
        self.expire_behavior = expire_behavior
        self.expire_grace_period = expire_grace_period
        self.revoked = revoked
        self.role_id = role_id
        self.subscriber_count = subscriber_count
        self.synced_at = synced_at
        self.syncing = syncing
        return self
    
    
    @classmethod
    def from_role(cls, role_id):
        """
        Creates a linked integration metadata.
        
        Parameters
        ----------
        role_id : ``Role``
            The respective role's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = cls._create_empty()
        self.role_id = role_id
        return self
        
    
    @classmethod
    @copy_docs(IntegrationMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.account = parse_account(data)
        self.expire_behavior = parse_expire_behavior(data)
        self.expire_grace_period = parse_expire_grace_period(data)
        self.revoked = parse_revoked(data)
        self.role_id = parse_role_id(data)
        self.subscriber_count = parse_subscriber_count(data)
        self.synced_at = parse_synced_at(data)
        self.syncing = parse_syncing(data)
        return self
    
    
    @copy_docs(IntegrationMetadataBase.to_data)
    def to_data(self, defaults = False):
        data = {}
        
        put_account_into(self.account, data, defaults)
        put_expire_behavior_into(self.expire_behavior, data, defaults)
        put_expire_grace_period_into(self.expire_grace_period, data, defaults)
        put_revoked_into(self.revoked, data, defaults)
        put_role_id_into(self.role_id, data, defaults)
        put_subscriber_count_into(self.subscriber_count, data, defaults)
        put_synced_at_into(self.synced_at, data, defaults)
        put_syncing_into(self.syncing, data, defaults)
        
        return data
    
    
    @copy_docs(IntegrationMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<', self.__class__.__name__,
        ]
        
        role_id = self.role_id
        if role_id:
            try:
                role = ROLES[role_id]
            except KeyError:
                pass
            else:
                repr_parts.append(' role=')
                repr_parts.append(repr(role))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(IntegrationMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.account != other.account:
            return False
        
        if self.expire_behavior != other.expire_behavior:
            return False
        
        if self.expire_grace_period != other.expire_grace_period:
            return False
        
        if self.revoked != other.revoked:
            return False
        
        if self.role_id != other.role_id:
            return False
        
        if self.subscriber_count != other.subscriber_count:
            return False
        
        if self.synced_at != other.synced_at:
            return False
        
        if self.syncing != other.syncing:
            return False
        
        return True
    
    
    @copy_docs(IntegrationMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # account
        hash_value ^= hash(self.account)
        
        # expire_behavior
        hash_value ^= self.expire_behavior.value
        
        # expire_grace_period
        hash_value ^= self.expire_grace_period << 4
        
        # revoked
        hash_value ^= self.revoked << 8
        
        # role_id
        hash_value ^= self.role_id
        
        # subscriber_count
        hash_value ^= self.subscriber_count << 12
        
        # synced_at
        synced_at = self.synced_at
        if (synced_at is not None):
            hash_value ^= hash(synced_at)
        
        # syncing
        hash_value ^= self.syncing << 20
        
        return hash_value
    
    
    @classmethod
    @copy_docs(IntegrationMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.account = IntegrationAccount._create_empty()
        self.expire_behavior = IntegrationExpireBehavior.remove_role
        self.expire_grace_period = EXPIRE_GRACE_PERIOD_DEFAULT
        self.revoked = False
        self.role_id = 0
        self.subscriber_count = SUBSCRIBER_COUNT_DEFAULT
        self.synced_at = None
        self.syncing = False
        return self
    
    
    @copy_docs(IntegrationMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.account = self.account
        new.expire_behavior = self.expire_behavior
        new.expire_grace_period = self.expire_grace_period
        new.revoked = self.revoked
        new.role_id = self.role_id
        new.subscriber_count = self.subscriber_count
        new.synced_at = self.synced_at
        new.syncing = self.syncing
        return new
    
    
    @copy_docs(IntegrationMetadataBase.copy_with)
    def copy_with(self, keyword_parameters):
        # account
        try:
            account = keyword_parameters.pop('account')
        except KeyError:
            account = self.account
        else:
            account = validate_account(account)
        
        # expire_behavior
        try:
            expire_behavior = keyword_parameters.pop('expire_behavior')
        except KeyError:
            expire_behavior = self.expire_behavior
        else:
            expire_behavior = validate_expire_behavior(expire_behavior)
        
        # expire_grace_period
        try:
            expire_grace_period = keyword_parameters.pop('expire_grace_period')
        except KeyError:
            expire_grace_period = self.expire_grace_period
        else:
            expire_grace_period = validate_expire_grace_period(expire_grace_period)
        
        # revoked
        try:
            revoked = keyword_parameters.pop('revoked')
        except KeyError:
            revoked = self.revoked
        else:
            revoked = validate_revoked(revoked)
        
        # role_id
        try:
            role_id = keyword_parameters.pop('role_id')
        except KeyError:
            role_id = self.role_id
        else:
            role_id = validate_role_id(role_id)
        
        # subscriber_count
        try:
            subscriber_count = keyword_parameters.pop('subscriber_count')
        except KeyError:
            subscriber_count = self.subscriber_count
        else:
            subscriber_count = validate_subscriber_count(subscriber_count)
        
        # synced_at
        try:
            synced_at = keyword_parameters.pop('synced_at')
        except KeyError:
            synced_at = self.synced_at
        else:
            synced_at = validate_synced_at(synced_at)
        
        # syncing
        try:
            syncing = keyword_parameters.pop('syncing')
        except KeyError:
            syncing = self.syncing
        else:
            syncing = validate_syncing(syncing)
        
        new = object.__new__(type(self))
        new.account = account
        new.expire_behavior = expire_behavior
        new.expire_grace_period = expire_grace_period
        new.revoked = revoked
        new.role_id = role_id
        new.subscriber_count = subscriber_count
        new.synced_at = synced_at
        new.syncing = syncing
        return new
