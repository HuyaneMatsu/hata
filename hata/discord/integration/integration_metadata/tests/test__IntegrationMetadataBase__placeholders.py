from datetime import datetime as DateTime

import vampytest

from ...integration_application import IntegrationApplication

from ..base import IntegrationMetadataBase
from ..preinstanced import IntegrationExpireBehavior


def test__IntegrationMetadataBase__placeholders():
    """
    Tests whether ``IntegrationMetadataBase``'s placeholders work as intended.
    """
    integration_metadata = IntegrationMetadataBase()
    vampytest.assert_instance(integration_metadata.account, object)
    vampytest.assert_instance(integration_metadata.application, IntegrationApplication, nullable = True)
    vampytest.assert_instance(integration_metadata.expire_behavior, IntegrationExpireBehavior)
    vampytest.assert_instance(integration_metadata.expire_grace_period, int)
    vampytest.assert_instance(integration_metadata.revoked, bool)
    vampytest.assert_instance(integration_metadata.role_id, int)
    vampytest.assert_instance(integration_metadata.scopes, tuple, nullable = True)
    vampytest.assert_instance(integration_metadata.subscriber_count, int)
    vampytest.assert_instance(integration_metadata.synced_at, DateTime, nullable = True)
    vampytest.assert_instance(integration_metadata.syncing, bool)
