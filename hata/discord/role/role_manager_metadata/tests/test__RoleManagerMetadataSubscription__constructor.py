import vampytest

from ..subscription import RoleManagerMetadataSubscription


def _assert_is_every_attribute_set(metadata):
    """
    Asserts whether every attributes are set of the given role manager metadata.
    
    Parameters
    ----------
    metadata : ``RoleManagerMetadataSubscription``
        The metadata to assert.
    """
    vampytest.assert_instance(metadata, RoleManagerMetadataSubscription)


def test__RoleManagerMetadataSubscription__new__0():
    """
    Tests whether ``RoleManagerMetadataSubscription.__new__`` works as intended.
    
    Case: No fields given.
    """
    metadata = RoleManagerMetadataSubscription()
    _assert_is_every_attribute_set(metadata)


def test__RoleManagerMetadataSubscription__new__1():
    """
    Tests whether ``RoleManagerMetadataSubscription.__new__`` works as intended.
    
    Case: all fields given
    """
    integration_id = 202212170000
    purchasable = True
    subscription_listing_id = 202212170001
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
        purchasable = purchasable,
        subscription_listing_id = subscription_listing_id,
    )
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.integration_id, integration_id)
    vampytest.assert_eq(metadata.purchasable, purchasable)
    vampytest.assert_eq(metadata.subscription_listing_id, subscription_listing_id)
