import vampytest

from .. import AutoModerationRuleTriggerMetadata


def test__AutoModerationRuleTriggerMetadata__eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationRuleTriggerMetadata(),
        AutoModerationRuleTriggerMetadata(),
    )


def test__AutoModerationRuleTriggerMetadata__eq__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadata(),
        0,
    )


def test__AutoModerationRuleTriggerMetadata__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s `__hash__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadata()
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadata__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s `__repr__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadata()
    
    vampytest.assert_instance(repr(metadata), str)
