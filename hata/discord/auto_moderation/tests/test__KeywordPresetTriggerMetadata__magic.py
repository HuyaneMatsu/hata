import vampytest

from .. import KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType


def test__KeywordPresetTriggerMetadata__eq_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        KeywordPresetTriggerMetadata(None),
        KeywordPresetTriggerMetadata(None),
    )


def test__KeywordPresetTriggerMetadata__eq_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        KeywordPresetTriggerMetadata(None),
        0,
    )


def test__KeywordPresetTriggerMetadata__not_eq_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `__eq__` method works as expected when passing
    objects with different values.
    """
    vampytest.assert_not_eq(
        KeywordPresetTriggerMetadata(None),
        KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur),
    )


def test__KeywordPresetTriggerMetadata__hash():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `__hash__` method works as intended
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_instance(hash(metadata), int)


def test__KeywordPresetTriggerMetadata__repr():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `__repr__` method works as intended
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_instance(repr(metadata), str)
