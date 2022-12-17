import vampytest

from ..subscription import RoleManagerMetadataSubscription

from .test__RoleManagerMetadataSubscription__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataSubscription__from_data():
    """
    Tests whether ``RoleManagerMetadataSubscription.from_data`` works as intended.
    """
    integration_id = 202212170002
    purchasable = True
    subscription_listing_id = 202212170003
    
    data = {
        'integration_id': str(integration_id),
        'available_for_purchase': None,
        'subscription_listing_id': str(subscription_listing_id),
    }
    
    metadata = RoleManagerMetadataSubscription.from_data(data)
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.integration_id, integration_id)
    vampytest.assert_eq(metadata.purchasable, purchasable)
    vampytest.assert_eq(metadata.subscription_listing_id, subscription_listing_id)


def test__RoleManagerMetadataSubscription__to_data():
    """
    Tests whether ``RoleManagerMetadataSubscription.to_data`` works as intended.
    """
    integration_id = 202212170004
    purchasable = True
    subscription_listing_id = 202212170005
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
        purchasable = purchasable,
        subscription_listing_id = subscription_listing_id,
    )
    
    expected_data = {
        'integration_id': str(integration_id),
        'available_for_purchase': None,
        'subscription_listing_id': str(subscription_listing_id),
    }
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_data
    )
