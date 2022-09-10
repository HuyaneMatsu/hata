import vampytest

from .. import ActivityMetadataCustom


def test__ActivityMetadataCustom__new__0():
    """
    Tests whether ``ActivityMetadataCustom.__new__`` works as intended.
    """
    activity_metadata = ActivityMetadataCustom({})
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataCustom)
    
    vampytest.assert_is(activity_metadata.created_at, None)
    vampytest.assert_is(activity_metadata.emoji, None)
    vampytest.assert_is(activity_metadata.state, None)
    

def test__ActivityMetadataCustom__new__1():
    """
    Tests whether ``ActivityMetadataCustom.__new__`` wont touch the`keyword_parameters` parameter.
    """
    keyword_parameters = {'name': ''}
    keyword_parameters_copy = keyword_parameters.copy()
    
    ActivityMetadataCustom(keyword_parameters)
    
    vampytest.assert_eq(keyword_parameters, keyword_parameters_copy)
