import vampytest

from .. import AutoModerationActionMetadataTimeout


def test__AutoModerationActionMetadataTimeout__to_data():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `to_data` method works as expected.
    """
    metadata = AutoModerationActionMetadataTimeout(0)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'duration_seconds': 0,
        },
    )

    
def test__AutoModerationActionMetadataTimeout__from_data():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `from_data` method works as expected.
    """
    metadata = AutoModerationActionMetadataTimeout.from_data({
        'duration_seconds': 0,
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationActionMetadataTimeout(0),
    )
