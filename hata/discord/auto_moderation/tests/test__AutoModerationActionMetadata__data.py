import vampytest

from .. import AutoModerationActionMetadata


def test__AutoModerationActionMetadata__to_data__0():
    """
    Tests whether ``AutoModerationActionMetadata``'s `to_data` method works as expected.
    """
    metadata = AutoModerationActionMetadata()
    
    vampytest.assert_eq(
        metadata.to_data(),
        {},
    )


def test__AutoModerationActionMetadata__from_data__0():
    """
    Tests whether ``AutoModerationActionMetadata``'s `from_data` method works as expected.
    """
    metadata = AutoModerationActionMetadata.from_data({})
    
    vampytest.assert_eq(
        metadata,
        AutoModerationActionMetadata(),
    )
