from datetime import datetime as DateTime

import vampytest

from ....user import ClientUserBase, User

from ...integration_account import IntegrationAccount
from ...integration_application import IntegrationApplication

from ..integration import Integration
from ..integration_type import IntegrationType
from ..preinstanced import IntegrationExpireBehavior


def _check_integration_proxied_properties(integration):
    """
    Asserts whether all proxied properties of the integrations are accessible,
    
    Parameters
    ----------
    integration : ``Integration``
        The integration to check.
    """
    vampytest.assert_instance(integration.account, object)
    vampytest.assert_instance(integration.application, IntegrationApplication, nullable = True)
    vampytest.assert_instance(integration.expire_behavior, IntegrationExpireBehavior)
    vampytest.assert_instance(integration.revoked, bool)
    vampytest.assert_instance(integration.role_id, int)
    vampytest.assert_instance(integration.scopes, tuple, nullable = True)
    vampytest.assert_instance(integration.subscriber_count, int)
    vampytest.assert_instance(integration.synced_at, DateTime, nullable = True)
    vampytest.assert_instance(integration.syncing, bool)


def test__Integration__properties__0():
    """
    Tests whether ``Integration``'s properties work as intended.
    
    Case: none.
    """
    integration = Integration(
        integration_type = IntegrationType.none,
    )
    _check_integration_proxied_properties(integration)


def test__Integration__properties__1():
    """
    Tests whether ``Integration``'s properties work as intended.
    
    Case: discord.
    """
    account = User.precreate(202210140040, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202210140041, name = 'Koishi', bot = account)


    integration = Integration(
        integration_type = IntegrationType.discord,
        account = account,
        application = application,
    )
    _check_integration_proxied_properties(integration)
    
    vampytest.assert_is(integration.account, account)
    vampytest.assert_eq(integration.application, application)


def test__Integration__properties__2():
    """
    Tests whether ``Integration``'s properties work as intended.
    
    Case: twitch.
    """
    account = IntegrationAccount('hello', 'hell')
    expire_behavior = IntegrationExpireBehavior.kick
    expire_grace_period = 7
    revoked = True
    role_id = 202210140042
    subscriber_count = 100
    synced_at = DateTime(2016, 9, 9)
    syncing = True
    
    
    integration = Integration(
        integration_type = IntegrationType.twitch,
        account = account,
        expire_behavior = expire_behavior,
        expire_grace_period = expire_grace_period,
        revoked = revoked,
        role_id = role_id,
        subscriber_count = subscriber_count,
        synced_at = synced_at,
        syncing = syncing,
    )
    _check_integration_proxied_properties(integration)
    
    
    vampytest.assert_eq(integration.account, account)
    vampytest.assert_is(integration.expire_behavior, expire_behavior)
    vampytest.assert_eq(integration.expire_grace_period, expire_grace_period)
    vampytest.assert_eq(integration.revoked, revoked)
    vampytest.assert_eq(integration.role_id, role_id)
    vampytest.assert_eq(integration.subscriber_count, subscriber_count)
    vampytest.assert_eq(integration.synced_at, synced_at)
    vampytest.assert_eq(integration.syncing, syncing)
