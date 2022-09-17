import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeywordPreset, AutoModerationKeywordPresetType


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` returns as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataKeywordPreset)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: `None`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__2():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: `[]`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset([])
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__3():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: `AutoModerationKeywordPresetType.slur`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationKeywordPresetType.slur)
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__4():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: `[AutoModerationKeywordPresetType.slur]`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset([AutoModerationKeywordPresetType.slur])
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__5():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s raises as expected on bad parameter.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRuleTriggerMetadataKeywordPreset(12.6)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__6():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s raises as expected on bad parameter.
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRuleTriggerMetadataKeywordPreset([12.6])


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__7():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: `AutoModerationKeywordPresetType.slur.value`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationKeywordPresetType.slur.value)
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__8():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: `[AutoModerationKeywordPresetType.slur.value]`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset([AutoModerationKeywordPresetType.slur.value])
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__9():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: *missing*.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__10():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.keyword_presets` as expected.
    Case: *None*.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None, None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__11():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.excluded_keywords` as expected.
    Case: `'owo'`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None, 'owo')
    
    vampytest.assert_eq(metadata.excluded_keywords, ('owo', ))


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__12():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` sets `.excluded_keywords` as expected.
    Case: `['owo']`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None, ['owo'])
    
    vampytest.assert_eq(metadata.excluded_keywords, ('owo', ))

def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__13():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` fails when `excluded_keywords` is given incorrectly.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRuleTriggerMetadataKeywordPreset(None, 12.6)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__14():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new::`` fails when `excluded_keywords` is given incorrectly.
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRuleTriggerMetadataKeywordPreset(None, [12.6])
