from datetime import datetime as DateTime

import vampytest

from ...integration_account import IntegrationAccount

from ..preinstanced import IntegrationExpireBehavior

from ..subscription import IntegrationMetadataSubscription


def _check_all_fields_set(integration_metadata):
    """
    Tests whether all attributes of an ``IntegrationMetadataSubscription`` are set.
    
    Parameters
    ----------
    integration_metadata : ``IntegrationMetadataSubscription``
        The integration detail to check out.
    """
    vampytest.assert_instance(integration_metadata, IntegrationMetadataSubscription)
    
    vampytest.assert_instance(integration_metadata.account, IntegrationAccount)
    vampytest.assert_instance(integration_metadata.expire_behavior, IntegrationExpireBehavior)
    vampytest.assert_instance(integration_metadata.expire_grace_period, int)
    vampytest.assert_instance(integration_metadata.revoked, bool)
    vampytest.assert_instance(integration_metadata.role_id, int)
    vampytest.assert_instance(integration_metadata.subscriber_count, int)
    vampytest.assert_instance(integration_metadata.synced_at, DateTime, nullable = True)
    vampytest.assert_instance(integration_metadata.syncing, bool)
        

def test__IntegrationMetadataSubscription__new__0():
    """
    Tests whether ``IntegrationMetadataSubscription.__new__`` works as intended.
    
    Case: No fields given.
    """
    integration_metadata = IntegrationMetadataSubscription({})
    _check_all_fields_set(integration_metadata)


def test__IntegrationMetadataSubscription__new__1():
    """
    Tests whether ``IntegrationMetadataSubscription.__new__`` works as intended.
    
    Case: All fields given.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202210090001
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9)
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
    
    integration_metadata = IntegrationMetadataSubscription(keyword_parameters)
    _check_all_fields_set(integration_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(integration_metadata.account, account)
    vampytest.assert_is(integration_metadata.expire_behavior, expire_behavior)
    vampytest.assert_eq(integration_metadata.expire_grace_period, expire_grace_period)
    vampytest.assert_eq(integration_metadata.revoked, revoked)
    vampytest.assert_eq(integration_metadata.role_id, role_id)
    vampytest.assert_eq(integration_metadata.subscriber_count, subscriber_count)
    vampytest.assert_eq(integration_metadata.synced_at, synced_at)
    vampytest.assert_eq(integration_metadata.syncing, syncing)



def test__IntegrationMetadataSubscription__from_role():
    """
    Tests whether ``IntegrationMetadataSubscription.from_role`` works as intended.
    """
    role_id = 202210090002
    
    integration_metadata = IntegrationMetadataSubscription.from_role(role_id)
    _check_all_fields_set(integration_metadata)
    vampytest.assert_eq(integration_metadata.role_id, role_id)


def test__IntegrationMetadataSubscription__create_empty():
    """
    Tests whether ``IntegrationMetadataSubscription._create_empty`` works as intended.
    """
    integration_metadata = IntegrationMetadataSubscription._create_empty()
    _check_all_fields_set(integration_metadata)
