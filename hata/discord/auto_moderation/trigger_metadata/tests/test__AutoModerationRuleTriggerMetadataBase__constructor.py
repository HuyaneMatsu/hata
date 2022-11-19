import vampytest

from ..base import AutoModerationRuleTriggerMetadataBase


def _assert_is_every_attribute_set(metadata):
    """
    Asserts whether every attribute is set of the given trigger rule metadata.
    """
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataBase)


def test__AutoModerationRuleTriggerMetadataBase__new():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.__new__`` returns as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    _assert_is_every_attribute_set(metadata)
