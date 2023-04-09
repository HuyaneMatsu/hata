import vampytest

from ..base import ActivityMetadataBase

from .test__ActivityMetadataBase__constructor import _assert_fields_set


def test__ActivityMetadataBase__from_data():
    """
    Tests whether ``ActivityMetadataBase.from_data`` works as intended.
    """
    data = {}
    
    activity_metadata = ActivityMetadataBase.from_data(data)
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataBase)


def test__ActivityMetadataBase__to_data():
    """
    Tests whether ``ActivityMetadataBase.to_data`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    vampytest.assert_eq(activity_metadata.to_data(), {})


def test__ActivityMetadataBase__to_data__user():
    """
    Tests whether `ActivityMetadataBase.to_data(user = True)` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    vampytest.assert_eq(
        activity_metadata.to_data(defaults = True, user = True),
        {},
    )


def test__ActivityMetadataBase__to_data__include_internals():
    """
    Tests whether `ActivityMetadataBase.to_data(include_internals = True)` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    vampytest.assert_eq(
        activity_metadata.to_data(defaults = True, include_internals = True),
        {},
    )


def test__ActivityMetadataBase__update_attributes():
    """
    Tests whether ``ActivityMetadataBase._update_attributes`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    activity_metadata._update_attributes({})


def test__ActivityMetadataBase__difference_update_attributes():
    """
    Tests whether ``ActivityMetadataBase._difference_update_attributes`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    old_attributes = activity_metadata._difference_update_attributes({})
    vampytest.assert_eq(old_attributes, {})
