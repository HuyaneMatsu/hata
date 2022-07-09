import vampytest

from .. import KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType


def test__KeywordPresetTriggerMetadata__constructor_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor returns as expected.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_instance(metadata, KeywordPresetTriggerMetadata)


def test__KeywordPresetTriggerMetadata__constructor_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: `None`.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__constructor_2():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: `[]`.
    """
    metadata = KeywordPresetTriggerMetadata([])
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__constructor_3():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: `AutoModerationKeywordPresetType.slur`.
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur)
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__constructor_4():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: `[AutoModerationKeywordPresetType.slur]`.
    """
    metadata = KeywordPresetTriggerMetadata([AutoModerationKeywordPresetType.slur])
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__constructor_5():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s raises as expected on bad parameter.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata(12.6)


def test__KeywordPresetTriggerMetadata__constructor_6():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s raises as expected on bad parameter.
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata([12.6])


def test__KeywordPresetTriggerMetadata__constructor_7():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: `AutoModerationKeywordPresetType.slur.value`.
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur.value)
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__constructor_8():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: `[AutoModerationKeywordPresetType.slur.value]`.
    """
    metadata = KeywordPresetTriggerMetadata([AutoModerationKeywordPresetType.slur.value])
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__constructor_9():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: *missing*.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__constructor_10():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.keyword_presets` as expected.
    Case: *None*.
    """
    metadata = KeywordPresetTriggerMetadata(None, None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__constructor_11():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.excluded_keywords` as expected.
    Case: `'owo'`.
    """
    metadata = KeywordPresetTriggerMetadata(None, 'owo')
    
    vampytest.assert_eq(metadata.excluded_keywords, ('owo', ))


def test__KeywordPresetTriggerMetadata__constructor_12():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor sets `.excluded_keywords` as expected.
    Case: `['owo']`.
    """
    metadata = KeywordPresetTriggerMetadata(None, ['owo'])
    
    vampytest.assert_eq(metadata.excluded_keywords, ('owo', ))

def test__KeywordPresetTriggerMetadata__constructor_13():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor fails when `excluded_keywords` is given incorrectly.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata(None, 12.6)


def test__KeywordPresetTriggerMetadata__constructor_14():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s constructor fails when `excluded_keywords` is given incorrectly.
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata(None, [12.6])
