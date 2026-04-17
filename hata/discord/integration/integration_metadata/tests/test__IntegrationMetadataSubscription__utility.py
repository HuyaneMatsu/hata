from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...integration_account import IntegrationAccount

from ..preinstanced import IntegrationExpireBehavior
from ..subscription import IntegrationMetadataSubscription

from .test__IntegrationMetadataSubscription__constructor import _assert_fields_set


def test__IntegrationMetadataSubscription__copy():
    """
    Tests whether ``IntegrationMetadataSubscription.copy`` works as intended.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202212170041
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    syncing = True
    
    integration_metadata = IntegrationMetadataSubscription(
        account = account,
        expire_behavior = expire_behavior,
        expire_grace_period = expire_grace_period,
        revoked = revoked,
        role_id = role_id,
        subscriber_count = subscriber_count,
        synced_at = synced_at,
        syncing = syncing,
    )
    
    copy = integration_metadata.copy()
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    vampytest.assert_eq(copy, integration_metadata)


def test__IntegrationMetadataSubscription__copy_with__0():
    """
    Tests whether ``IntegrationMetadataSubscription.copy_with`` works as intended.
    
    Case: No fields given.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202212170042
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    syncing = True

    integration_metadata = IntegrationMetadataSubscription(
        account = account,
        expire_behavior = expire_behavior,
        expire_grace_period = expire_grace_period,
        revoked = revoked,
        role_id = role_id,
        subscriber_count = subscriber_count,
        synced_at = synced_at,
        syncing = syncing,
    )
    
    copy = integration_metadata.copy_with()
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    vampytest.assert_eq(copy, integration_metadata)


def test__IntegrationMetadataSubscription__copy_with__1():
    """
    Tests whether ``IntegrationMetadataSubscription.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_account = IntegrationAccount('hello', 'hell')
    old_expire_behavior = IntegrationExpireBehavior.kick
    old_expire_grace_period = 7
    old_revoked = True
    old_role_id = 202212170043
    old_subscriber_count = 100
    old_synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    old_syncing = True
    new_account = IntegrationAccount('hello', 'hell')
    new_expire_behavior = IntegrationExpireBehavior.kick
    new_expire_grace_period = 7
    new_revoked = True
    new_role_id = 202212170044
    new_subscriber_count = 100
    new_synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    new_syncing = True

    integration_metadata = IntegrationMetadataSubscription(
        account = old_account,
        expire_behavior = old_expire_behavior,
        expire_grace_period = old_expire_grace_period,
        revoked = old_revoked,
        role_id = old_role_id,
        subscriber_count = old_subscriber_count,
        synced_at = old_synced_at,
        syncing = old_syncing,
    )
    
    copy = integration_metadata.copy_with(
        account = new_account,
        expire_behavior = new_expire_behavior,
        expire_grace_period = new_expire_grace_period,
        revoked = new_revoked,
        role_id = new_role_id,
        subscriber_count = new_subscriber_count,
        synced_at = new_synced_at,
        syncing = new_syncing,
    )
    
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    
    vampytest.assert_eq(copy.account, new_account)
    vampytest.assert_is(copy.expire_behavior, new_expire_behavior)
    vampytest.assert_eq(copy.expire_grace_period, new_expire_grace_period)
    vampytest.assert_eq(copy.revoked, new_revoked)
    vampytest.assert_eq(copy.role_id, new_role_id)
    vampytest.assert_eq(copy.subscriber_count, new_subscriber_count)
    vampytest.assert_eq(copy.synced_at, new_synced_at)
    vampytest.assert_eq(copy.syncing, new_syncing)


def test__IntegrationMetadataSubscription__copy_with_keyword_parameters__0():
    """
    Tests whether ``IntegrationMetadataSubscription.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202304080009
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    syncing = True

    integration_metadata = IntegrationMetadataSubscription(
        account = account,
        expire_behavior = expire_behavior,
        expire_grace_period = expire_grace_period,
        revoked = revoked,
        role_id = role_id,
        subscriber_count = subscriber_count,
        synced_at = synced_at,
        syncing = syncing,
    )
    
    copy = integration_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    vampytest.assert_eq(copy, integration_metadata)


def test__IntegrationMetadataSubscription__copy_with_keyword_parameters__1():
    """
    Tests whether ``IntegrationMetadataSubscription.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_account = IntegrationAccount('hello', 'hell')
    old_expire_behavior = IntegrationExpireBehavior.kick
    old_expire_grace_period = 7
    old_revoked = True
    old_role_id = 202304080010
    old_subscriber_count = 100
    old_synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    old_syncing = True
    new_account = IntegrationAccount('hello', 'hell')
    new_expire_behavior = IntegrationExpireBehavior.kick
    new_expire_grace_period = 7
    new_revoked = True
    new_role_id = 202304080011
    new_subscriber_count = 100
    new_synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    new_syncing = True

    integration_metadata = IntegrationMetadataSubscription(
        account = old_account,
        expire_behavior = old_expire_behavior,
        expire_grace_period = old_expire_grace_period,
        revoked = old_revoked,
        role_id = old_role_id,
        subscriber_count = old_subscriber_count,
        synced_at = old_synced_at,
        syncing = old_syncing,
    )
    
    copy = integration_metadata.copy_with_keyword_parameters({
        'account': new_account,
        'expire_behavior': new_expire_behavior,
        'expire_grace_period': new_expire_grace_period,
        'revoked': new_revoked,
        'role_id': new_role_id,
        'subscriber_count': new_subscriber_count,
        'synced_at': new_synced_at,
        'syncing': new_syncing,
        
    })
    
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    
    vampytest.assert_eq(copy.account, new_account)
    vampytest.assert_is(copy.expire_behavior, new_expire_behavior)
    vampytest.assert_eq(copy.expire_grace_period, new_expire_grace_period)
    vampytest.assert_eq(copy.revoked, new_revoked)
    vampytest.assert_eq(copy.role_id, new_role_id)
    vampytest.assert_eq(copy.subscriber_count, new_subscriber_count)
    vampytest.assert_eq(copy.synced_at, new_synced_at)
    vampytest.assert_eq(copy.syncing, new_syncing)
