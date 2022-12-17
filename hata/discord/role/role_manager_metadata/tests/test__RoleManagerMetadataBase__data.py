import vampytest

from ..base import RoleManagerMetadataBase

from .test__RoleManagerMetadataBase__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataBase__from_data():
    """
    Tests whether ``RoleManagerMetadataBase.from_data`` works as intended.
    """
    data = {}
    
    metadata = RoleManagerMetadataBase.from_data(data)
    _assert_is_every_attribute_set(metadata)


def test__RoleManagerMetadataBase__to_data():
    """
    Tests whether ``RoleManagerMetadataBase.to_data`` works as intended.
    """
    metadata = RoleManagerMetadataBase()
    
    expected_data = {}
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_data
    )
