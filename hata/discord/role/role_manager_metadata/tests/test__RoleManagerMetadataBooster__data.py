import vampytest

from ..booster import RoleManagerMetadataBooster

from .test__RoleManagerMetadataBooster__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataBooster__from_data():
    """
    Tests whether ``RoleManagerMetadataBooster.from_data`` works as intended.
    """
    data = {}
    
    metadata = RoleManagerMetadataBooster.from_data(data)
    _assert_is_every_attribute_set(metadata)


def test__RoleManagerMetadataBooster__to_data():
    """
    Tests whether ``RoleManagerMetadataBooster.to_data`` works as intended.
    """
    metadata = RoleManagerMetadataBooster()
    
    expected_data = {'premium_subscriber': None}
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_data
    )
