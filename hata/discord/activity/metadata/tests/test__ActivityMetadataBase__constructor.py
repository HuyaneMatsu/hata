import vampytest

from .. import CustomActivityMetadata


def test__CustomActivityMetadata__new__0():
    """
    Tests whether ``CustomActivityMetadata.__new__`` works as intended.
    """
    activity_metadata = CustomActivityMetadata({})
    
    vampytest.assert_instance(activity_metadata, CustomActivityMetadata)
    
    vampytest.assert_is(activity_metadata.created_at, None)
    vampytest.assert_is(activity_metadata.emoji, None)
    vampytest.assert_is(activity_metadata.state, None)
    

def test__CustomActivityMetadata__new__1():
    """
    Tests whether ``CustomActivityMetadata.__new__`` wont touch the`keyword_parameters` parameter.
    """
    keyword_parameters = {'name': ''}
    keyword_parameters_copy = keyword_parameters.copy()
    
    CustomActivityMetadata(keyword_parameters)
    
    vampytest.assert_eq(keyword_parameters, keyword_parameters_copy)
