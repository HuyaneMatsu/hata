import vampytest

from .. import ActivityMetadataBase


def test__ActivityMetadataBase__new__0():
    """
    Tests whether ``ActivityMetadataBase.__new__`` works as intended.
    """
    activity_metadata = ActivityMetadataBase({})
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataBase)


def test__ActivityMetadataBase__new__1():
    """
    Tests whether ``ActivityMetadataBase.__new__`` pop empty name from it's `keyword_parameters` parameter.
    """
    keyword_parameters = {'name': ''}
    ActivityMetadataBase(keyword_parameters)
    
    vampytest.assert_eq(keyword_parameters, {})
