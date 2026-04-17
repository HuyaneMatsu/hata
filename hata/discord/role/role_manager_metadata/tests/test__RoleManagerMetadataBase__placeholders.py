import vampytest

from ..base import RoleManagerMetadataBase


def test__RoleManagerMetadataBase__placeholders():
    """
    Tests whether ``RoleManagerMetadataBase``'s placeholders works as intended.
    """
    metadata = RoleManagerMetadataBase()
    vampytest.assert_instance(metadata.bot_id, int)
    vampytest.assert_instance(metadata.integration_id, int)
    vampytest.assert_instance(metadata.subscription_listing_id, int)
    vampytest.assert_instance(metadata.purchasable, bool)
