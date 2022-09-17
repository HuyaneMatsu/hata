import vampytest

from .. import AutoModerationActionMetadataBase


def test__AutoModerationActionMetadataBase__to_data__0():
    """
    Tests whether ``AutoModerationActionMetadataBase``'s `to_data` method works as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_eq(
        metadata.to_data(),
        {},
    )


def test__AutoModerationActionMetadataBase__from_data__0():
    """
    Tests whether ``AutoModerationActionMetadataBase``'s `from_data` method works as expected.
    """
    metadata = AutoModerationActionMetadataBase.from_data({})
    
    vampytest.assert_eq(
        metadata,
        AutoModerationActionMetadataBase(),
    )
