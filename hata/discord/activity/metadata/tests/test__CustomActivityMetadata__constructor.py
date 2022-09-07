import vampytest

from .. import CustomActivityMetadata


def test__CustomActivityMetadata__new__1():
    """
    Tests whether ``CustomActivityMetadata.__new__`` works as intended.
    """
    activity_metadata = CustomActivityMetadata({})
    
    vampytest.assert_instance(activity_metadata, CustomActivityMetadata)


def test__CustomActivityMetadata__new():
    """
    Tests whether ``CustomActivityMetadata.__new__`` works as intended.
    
    Case: should not remove empty `name` field.
    """
    keyword_parameters = {'name': ''}
    keyword_parameters_copy = keyword_parameters.copy()
    
    activity_metadata = CustomActivityMetadata(keyword_parameters)
    
    vampytest.assert_instance(activity_metadata, CustomActivityMetadata)
    vampytest.assert_eq(keyword_parameters, keyword_parameters_copy)
