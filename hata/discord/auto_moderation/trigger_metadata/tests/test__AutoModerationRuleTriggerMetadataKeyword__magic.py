import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeyword


def test__AutoModerationRuleTriggerMetadataKeyword__eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__eq__`` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationRuleTriggerMetadataKeyword(None),
        AutoModerationRuleTriggerMetadataKeyword(None),
    )


def test__AutoModerationRuleTriggerMetadataKeyword__eq__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__eq__`` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadataKeyword(None),
        0,
    )


def test__AutoModerationRuleTriggerMetadataKeyword__not_eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__eq__`` method works as expected when passing
    objects with different values.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadataKeyword(None),
        AutoModerationRuleTriggerMetadataKeyword('owo'),
    )


def test__AutoModerationRuleTriggerMetadataKeyword__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__hash__`` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(None)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataKeyword__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__repr__`` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(None)
    
    vampytest.assert_instance(repr(metadata), str)
