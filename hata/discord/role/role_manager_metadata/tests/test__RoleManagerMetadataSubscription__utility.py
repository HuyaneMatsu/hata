import vampytest

from ....integration import Integration

from ..subscription import RoleManagerMetadataSubscription

from .test__RoleManagerMetadataSubscription__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataSubscription__copy():
    """
    Tests whether ``RoleManagerMetadataSubscription.copy`` works as intended.
    """
    integration_id = 202212170014
    purchasable = True
    subscription_listing_id = 202212170015
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
        purchasable = purchasable,
        subscription_listing_id = subscription_listing_id,
    )
    copy = metadata.copy()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataSubscription__copy_with__0():
    """
    Tests whether ``RoleManagerMetadataSubscription.to_data`` works as intended.
    
    Case: No fields given.
    """
    integration_id = 202212170016
    purchasable = True
    subscription_listing_id = 202212170017
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
        purchasable = purchasable,
        subscription_listing_id = subscription_listing_id,
    )
    copy = metadata.copy_with()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataSubscription__copy_with__1():
    """
    Tests whether ``RoleManagerMetadataSubscription.to_data`` works as intended.
    
    Case: All fields given.
    """
    old_integration_id = 202212170018
    new_integration_id = 202212170019
    old_purchasable = True
    new_purchasable = True
    old_subscription_listing_id = 202212170020
    new_subscription_listing_id = 202212170021
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = old_integration_id,
        purchasable = old_purchasable,
        subscription_listing_id = old_subscription_listing_id,
    )
    copy = metadata.copy_with(
        integration_id = new_integration_id,
        purchasable = new_purchasable,
        subscription_listing_id = new_subscription_listing_id,
    )
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_is_not(copy, metadata)
    
    vampytest.assert_eq(copy.integration_id, new_integration_id)
    vampytest.assert_eq(copy.purchasable, new_purchasable)
    vampytest.assert_eq(copy.subscription_listing_id, new_subscription_listing_id)


def test__RoleManagerMetadataSubscription__manager_id():
    """
    Tests whether ``RoleManagerMetadataSubscription.manager_id`` works as intended.
    """
    integration_id = 202212170022
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
    )
    vampytest.assert_eq(metadata.manager_id, integration_id)


def test__RoleManagerMetadataSubscription__manager():
    """
    Tests whether ``RoleManagerMetadataSubscription.manager`` works as intended.
    """
    integration_id = 202212170023
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
    )
    vampytest.assert_is(metadata.manager, Integration.precreate(integration_id))
