import vampytest

from ..base import RoleManagerMetadataBase

from .test__RoleManagerMetadataBase__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataBase__copy():
    """
    Tests whether ``RoleManagerMetadataBase.copy`` works as intended.
    """
    metadata = RoleManagerMetadataBase()
    copy = metadata.copy()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataBase__copy_with__0():
    """
    Tests whether ``RoleManagerMetadataBase.to_data`` works as intended.
    
    Case: No fields given.
    """
    metadata = RoleManagerMetadataBase()
    copy = metadata.copy_with()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataBase__manager_id():
    """
    Tests whether ``RoleManagerMetadataBase.manager_id`` works as intended.
    """
    metadata = RoleManagerMetadataBase()
    vampytest.assert_eq(metadata.manager_id, 0)


def test__RoleManagerMetadataBase__manager():
    """
    Tests whether ``RoleManagerMetadataBase.manager`` works as intended.
    """
    metadata = RoleManagerMetadataBase()
    vampytest.assert_is(metadata.manager, None)
