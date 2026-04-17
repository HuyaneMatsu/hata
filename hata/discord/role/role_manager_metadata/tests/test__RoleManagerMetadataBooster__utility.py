import vampytest

from ..booster import RoleManagerMetadataBooster

from .test__RoleManagerMetadataBooster__constructor import _assert_fields_set


def test__RoleManagerMetadataBooster__copy():
    """
    Tests whether ``RoleManagerMetadataBooster.copy`` works as intended.
    """
    metadata = RoleManagerMetadataBooster()
    copy = metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataBooster__copy_with__0():
    """
    Tests whether ``RoleManagerMetadataBooster.to_data`` works as intended.
    
    Case: No fields given.
    """
    metadata = RoleManagerMetadataBooster()
    copy = metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataBooster__manager_id():
    """
    Tests whether ``RoleManagerMetadataBooster.manager_id`` works as intended.
    """
    metadata = RoleManagerMetadataBooster()
    vampytest.assert_eq(metadata.manager_id, 0)


def test__RoleManagerMetadataBooster__manager():
    """
    Tests whether ``RoleManagerMetadataBooster.manager`` works as intended.
    """
    metadata = RoleManagerMetadataBooster()
    vampytest.assert_is(metadata.manager, None)
