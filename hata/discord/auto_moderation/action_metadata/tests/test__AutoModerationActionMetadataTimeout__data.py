import vampytest

from ..timeout import AutoModerationActionMetadataTimeout

from .test__AutoModerationActionMetadataTimeout__constructor import _check_is_all_attribute_set


def test__AutoModerationActionMetadataTimeout__to_data():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `to_data` method works as expected.
    """
    duration = 69
    
    metadata = AutoModerationActionMetadataTimeout(duration)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'duration_seconds': duration,
        },
    )


def test__AutoModerationActionMetadataTimeout__from_data():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `from_data` method works as expected.
    """
    duration = 69
    
    data = {
        'duration_seconds': duration,
    }
    
    metadata = AutoModerationActionMetadataTimeout.from_data(data)
    _check_is_all_attribute_set(metadata)
    vampytest.assert_eq(metadata.duration, duration)
