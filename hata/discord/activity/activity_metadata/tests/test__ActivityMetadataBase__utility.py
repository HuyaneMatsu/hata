import vampytest

from ..base import ActivityMetadataBase

from .test__ActivityMetadataBase__constructor import _assert_fields_set


def test__ActivityMetadataBase__copy():
    """
    Tests whether ``ActivityMetadataBase.copy`` works as intended.
    """
    activity_metadata = ActivityMetadataBase({})
    
    copy = activity_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataBase__copy_with__0():
    """
    Tests whether ``ActivityMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataBase({})
    
    copy = activity_metadata.copy_with({})
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)
