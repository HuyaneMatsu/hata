import vampytest

from ..timeout import AutoModerationActionMetadataTimeout


def _check_is_all_attribute_set(metadata):
    """
    Asserts whether all attributes are set of the given auto moderation action metadata.
    
    Parameters
    ----------
    metadata : ``AutoModerationActionMetadataTimeout``
        The action metadata to test.
    """
    vampytest.assert_instance(metadata, AutoModerationActionMetadataTimeout)
    vampytest.assert_instance(metadata.duration, int)


def test__AutoModerationActionMetadataTimeout__new__0():
    """
    Tests whether ``AutoModerationActionMetadataTimeout.__new__`` works as intended.
    
    Case: no parameters.
    """
    metadata = AutoModerationActionMetadataTimeout()
    _check_is_all_attribute_set(metadata)


def test__AutoModerationActionMetadataTimeout__new__1():
    """
    Tests whether ``AutoModerationActionMetadataTimeout.__new__`` works as intended.
    
    Case: parameters.
    """
    duration = 69
    
    metadata = AutoModerationActionMetadataTimeout(duration)
    _check_is_all_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.duration, duration)
