import vampytest

from ..base import AutoModerationActionMetadataBase

from .test__AutoModerationActionMetadataBase__constructor import _assert_fields_set


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
    data = {}
    
    metadata = AutoModerationActionMetadataBase.from_data(data)
    _assert_fields_set(metadata)
