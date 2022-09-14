import vampytest

from .. import ActivityMetadataCustom


def test__ActivityMetadataCustom__new__1():
    """
    Tests whether ``ActivityMetadataCustom.__new__`` works as intended.
    """
    activity_metadata = ActivityMetadataCustom({})
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataCustom)


def test__ActivityMetadataCustom__new():
    """
    Tests whether ``ActivityMetadataCustom.__new__`` works as intended.
    
    Case: should not remove empty `name` field.
    """
    keyword_parameters = {'name': ''}
    keyword_parameters_copy = keyword_parameters.copy()
    
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataCustom)
    vampytest.assert_eq(keyword_parameters, keyword_parameters_copy)
