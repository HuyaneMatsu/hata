import vampytest

from ..base import ActivityMetadataBase


def _assert_fields_set(activity_metadata):
    """
    Asserts whether every fields are set of the given activity metadata.
    
    Parameters
    ----------
    activity_metadata : ``ActivityMetadataBase``
        The activity metadata to check.
    """
    vampytest.assert_instance(activity_metadata, ActivityMetadataBase)


def test__ActivityMetadataBase__new__no_fields():
    """
    Tests whether ``ActivityMetadataBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataBase()
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_is(activity_metadata.created_at, None)
    vampytest.assert_is(activity_metadata.emoji, None)
    vampytest.assert_is(activity_metadata.state, None)


def test__ActivityMetadataBase__from_keyword_parameters__no_fields():
    """
    Tests whether ``ActivityMetadataBase.from_keyword_parameters`` works as intended.
    """
    activity_metadata = ActivityMetadataBase.from_keyword_parameters({})
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_is(activity_metadata.created_at, None)
    vampytest.assert_is(activity_metadata.emoji, None)
    vampytest.assert_is(activity_metadata.state, None)
    

def test__ActivityMetadataBase__from_keyword_parameters__all_fields():
    """
    Tests whether ``ActivityMetadataBase.from_keyword_parameters`` wont touch the`keyword_parameters` parameter.
    """
    keyword_parameters = {
        'name': 'ara',
    }
    keyword_parameters_copy = keyword_parameters.copy()
    
    activity_metadata = ActivityMetadataBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(keyword_parameters, keyword_parameters_copy)


def test__ActivityMetadataBase__from_keyword_parameters__empty_name():
    """
    Tests whether ``ActivityMetadataBase.from_keyword_parameters`` will yeet empty name.
    """
    keyword_parameters = {
        'name': ''
    }
    
    activity_metadata = ActivityMetadataBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(keyword_parameters, {})
