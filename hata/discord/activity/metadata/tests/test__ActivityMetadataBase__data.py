import vampytest

from .. import ActivityMetadataBase


def test__ActivityMetadataBase__from_data():
    """
    Tests whether ``ActivityMetadataBase.from_data`` works as intended.
    """
    activity_metadata = ActivityMetadataBase.from_data({})
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataBase)


def test__ActivityMetadataBase__to_data():
    """
    Tests whether ``ActivityMetadataBase.to_data`` works as intended.
    """
    activity_metadata = ActivityMetadataBase({})
    
    vampytest.assert_eq(activity_metadata.to_data(), {})


def test__ActivityMetadataBase__to_data_user():
    """
    Tests whether ``ActivityMetadataBase.to_data_user`` works as intended.
    """
    activity_metadata = ActivityMetadataBase({})
    
    vampytest.assert_eq(activity_metadata.to_data(), {})


def test__ActivityMetadataBase__to_data_full():
    """
    Tests whether ``ActivityMetadataBase.to_data_full`` works as intended.
    """
    activity_metadata = ActivityMetadataBase({})
    
    vampytest.assert_eq(activity_metadata.to_data_full(), {})


def test__ActivityMetadataBase__update_attributes():
    """
    Tests whether ``ActivityMetadataBase._update_attributes`` works as intended.
    """
    activity_metadata = ActivityMetadataBase({})
    activity_metadata._update_attributes({})


def test__ActivityMetadataBase__difference_update_attributes():
    """
    Tests whether ``ActivityMetadataBase._difference_update_attributes`` works as intended.
    """
    activity_metadata = ActivityMetadataBase({})
    old_attributes = activity_metadata._difference_update_attributes({})
    vampytest.assert_eq(old_attributes, {})
