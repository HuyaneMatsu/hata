import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeyword


def test__AutoModerationRuleTriggerMetadataKeyword__to_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword``'s `to_data` method works as expected.
    Defining no keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(None)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'keyword_filter': [],
        },
    )


def test__AutoModerationRuleTriggerMetadataKeyword__to_data__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword``'s `to_data` method works as expected.
    Defining keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword('owo')
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'keyword_filter': ['owo'],
        },
    )


def test__AutoModerationRuleTriggerMetadataKeyword__from_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword``'s `from_data` method works as expected.
    Case: `None`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword.from_data({
        'keyword_filter': None,
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeyword(None),
    )


def test__AutoModerationRuleTriggerMetadataKeyword__from_data__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword``'s `from_data` method works as expected.
    Case: *missing*.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword.from_data({})
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeyword(None),
    )


def test__AutoModerationRuleTriggerMetadataKeyword__from_data__2():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword``'s `from_data` method works as expected.
    Case: `[]`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword.from_data({
        'keyword_filter': [],
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeyword(None),
    )


def test__AutoModerationRuleTriggerMetadataKeyword__from_data__3():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword``'s `from_data` method works as expected.
    Case: `['owo']`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword.from_data({
        'keyword_filter': ['owo'],
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeyword('owo'),
    )
