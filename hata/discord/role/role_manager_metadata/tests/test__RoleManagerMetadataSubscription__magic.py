import vampytest

from ..subscription import RoleManagerMetadataSubscription


def test__RoleManagerMetadataSubscription__repr():
    """
    Tests whether ``RoleManagerMetadataSubscription.__repr__`` works as intended.
    """
    integration_id = 202212170006
    purchasable = True
    subscription_listing_id = 202212170007
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
        purchasable = purchasable,
        subscription_listing_id = subscription_listing_id,
    )
    
    vampytest.assert_instance(repr(metadata), str)


def test__RoleManagerMetadataSubscription__hash():
    """
    Tests whether ``RoleManagerMetadataSubscription.__hash__`` works as intended.
    """
    integration_id = 202212170008
    purchasable = True
    subscription_listing_id = 202212170009
    
    metadata = RoleManagerMetadataSubscription(
        integration_id = integration_id,
        purchasable = purchasable,
        subscription_listing_id = subscription_listing_id,
    )
    
    vampytest.assert_instance(hash(metadata), int)


def test__RoleManagerMetadataSubscription__eq():
    """
    Tests whether ``RoleManagerMetadataSubscription.__hash__`` works as intended.
    """
    integration_id = 202212170010
    purchasable = True
    subscription_listing_id = 202212170011
    
    keyword_parameters = {
        'integration_id': integration_id,
        'purchasable': purchasable,
        'subscription_listing_id': subscription_listing_id,
    }
    
    metadata = RoleManagerMetadataSubscription(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('integration_id', 202212170012),
        ('purchasable', False),
        ('subscription_listing_id', 202212170013)
    ):
        test_metadata = RoleManagerMetadataSubscription(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
