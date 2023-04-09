import vampytest

from ..base import ActivityMetadataBase


def test__ActivityMetadataBase__repr():
    """
    Tests whether ``ActivityMetadataBase.__repr__`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    vampytest.assert_instance(repr(activity_metadata), str)


def test__ActivityMetadataBase__hash():
    """
    Tests whether ``ActivityMetadataBase.__hash__`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    vampytest.assert_instance(hash(activity_metadata), int)


def test__ActivityMetadataBase__eq():
    """
    Tests whether ``ActivityMetadataBase.__eq__`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    vampytest.assert_eq(activity_metadata, activity_metadata)
    vampytest.assert_ne(activity_metadata, object())
