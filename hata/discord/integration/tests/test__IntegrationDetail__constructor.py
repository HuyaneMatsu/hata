import vampytest

from .. import IntegrationDetail, IntegrationExpireBehavior


def test__IntegrationDetail__new():
    """
    Tests whether ``IntegrationDetail``'s ``__new__`` method works as intended.
    """
    data = {
        'expire_behavior': IntegrationExpireBehavior.kick.value,
        'expire_grace_period': 1,
        'revoked': True,
        'role_id': None,
        'subscriber_count': 69,
        'synced_at': None,
        'syncing': False,
    }
    integration_detail = IntegrationDetail(data)
    
    vampytest.assert_is(integration_detail.expire_behavior, IntegrationExpireBehavior.kick)
    vampytest.assert_eq(integration_detail.expire_grace_period, 1)
    vampytest.assert_eq(integration_detail.revoked, True)
    vampytest.assert_eq(integration_detail.role_id, 0)
    vampytest.assert_eq(integration_detail.subscriber_count, 69)
    vampytest.assert_is(integration_detail.synced_at, None)
    vampytest.assert_eq(integration_detail.syncing, False)
