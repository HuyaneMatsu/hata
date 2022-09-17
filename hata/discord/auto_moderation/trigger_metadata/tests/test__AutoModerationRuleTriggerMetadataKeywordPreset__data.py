import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeywordPreset, AutoModerationKeywordPresetType


def test__AutoModerationRuleTriggerMetadataKeywordPreset__to_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `to_data` method works as expected.
    Defining no keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'presets': [],
            'allow_list': [],
        },
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__to_data__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `to_data` method works as expected.
    Defining keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationKeywordPresetType.slur, 'owo')
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'presets': [AutoModerationKeywordPresetType.slur.value],
            'allow_list': ['owo']
        },
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__from_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `from_data` method works as expected.
    None value cases.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset.from_data({
        'presets': None,
        'allow_list': None,
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeywordPreset(None),
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__from_data__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `from_data` method works as expected.
    Missing data case.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset.from_data({})
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeywordPreset(None),
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__from_data__2():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `from_data` method works as expected.
    Empty data case.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset.from_data({
        'presets': [],
        'allow_list': [],
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeywordPreset(None),
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__from_data__3():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `from_data` method works as expected.
    Stuffed data case.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset.from_data({
        'presets': [AutoModerationKeywordPresetType.slur.value],
        'allow_list': ['owo'],
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationKeywordPresetType.slur, 'owo'),
    )
