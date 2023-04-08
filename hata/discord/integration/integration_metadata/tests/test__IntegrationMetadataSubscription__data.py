from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ...integration_account import IntegrationAccount

from ..preinstanced import IntegrationExpireBehavior
from ..subscription import IntegrationMetadataSubscription

from .test__IntegrationMetadataSubscription__constructor import _assert_fields_set


def test__IntegrationMetadataSubscription__from_data__0():
    """
    Tests whether ``IntegrationMetadataSubscription.from_data`` works as intended.
    
    Case: non-discord integration.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202210090003
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9)
    syncing = True
    
    data = {
        'account': account.to_data(),
        'expire_behavior': expire_behavior.value,
        'expire_grace_period': expire_grace_period,
        'revoked': revoked,
        'role_id': str(role_id),
        'subscriber_count': subscriber_count,
        'synced_at': datetime_to_timestamp(synced_at),
        'syncing': syncing,
    }
    
    
    integration_metadata = IntegrationMetadataSubscription.from_data(data)
    
    _assert_fields_set(integration_metadata)
    
    vampytest.assert_eq(integration_metadata.account, account)
    vampytest.assert_is(integration_metadata.expire_behavior, expire_behavior)
    vampytest.assert_eq(integration_metadata.expire_grace_period, expire_grace_period)
    vampytest.assert_eq(integration_metadata.revoked, revoked)
    vampytest.assert_eq(integration_metadata.role_id, role_id)
    vampytest.assert_eq(integration_metadata.subscriber_count, subscriber_count)
    vampytest.assert_eq(integration_metadata.synced_at, synced_at)
    vampytest.assert_eq(integration_metadata.syncing, syncing)


def test__IntegrationMetadataSubscription__to_data():
    """
    Tests whether ``IntegrationMetadataSubscription.to_data`` works as intended.
    
    Case: defaults.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202210090004
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9)
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
    
    expected_data = {
        'account': account.to_data(),
        'expire_behavior': expire_behavior.value,
        'expire_grace_period': expire_grace_period,
        'revoked': revoked,
        'role_id': str(role_id),
        'subscriber_count': subscriber_count,
        'synced_at': datetime_to_timestamp(synced_at),
        'syncing': syncing,
    }
    
    vampytest.assert_eq(
        integration_metadata.to_data(
            defaults = True,
        ),
        expected_data,
    )
