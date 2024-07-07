from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...integration_account import IntegrationAccount

from ..preinstanced import IntegrationExpireBehavior
from ..subscription import IntegrationMetadataSubscription


def test__IntegrationMetadataSubscription__repr():
    """
    Tests whether ``IntegrationMetadataSubscription.__new__`` works as intended.
    
    Case: All fields given.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202210090005
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
    
    vampytest.assert_instance(repr(integration_metadata), str)


def test__IntegrationMetadataSubscription__eq():
    """
    Tests whether ``IntegrationMetadataSubscription.__eq__`` works as intended.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202210090006
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    syncing = True
    
    keyword_parameters = {
        'account': account,
        'expire_behavior': expire_behavior,
        'expire_grace_period': expire_grace_period,
        'revoked': revoked,
        'role_id': role_id,
        'subscriber_count': subscriber_count,
        'synced_at': synced_at,
        'syncing': syncing,
    }
    
    integration_metadata = IntegrationMetadataSubscription(**keyword_parameters)
    
    vampytest.assert_eq(integration_metadata, integration_metadata)
    vampytest.assert_ne(integration_metadata, object())
    
    for field_name, field_value in (
        ('account', IntegrationAccount('ashy', 'pie')),
        ('expire_behavior', IntegrationExpireBehavior.remove_role),
        ('expire_grace_period', 3),
        ('revoked', False),
        ('role_id', 202210090007),
        ('subscriber_count', 420),
        ('expire_grace_period', 3),
        ('syncing', False),
    ):
        integration_metadata_test = IntegrationMetadataSubscription(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(integration_metadata, integration_metadata_test)


def test__IntegrationMetadataSubscription__hash():
    """
    Tests whether ``IntegrationMetadataSubscription.__hash__`` works as intended.
    
    Case: All fields given.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202210110000
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
    
    vampytest.assert_instance(hash(integration_metadata), int)
