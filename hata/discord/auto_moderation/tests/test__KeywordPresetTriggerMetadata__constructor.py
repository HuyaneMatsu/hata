import vampytest

from .. import KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType


def test__KeywordPresetTriggerMetadata__new__0():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` returns as expected.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_instance(metadata, KeywordPresetTriggerMetadata)


def test__KeywordPresetTriggerMetadata__new__1():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: `None`.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__new__2():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: `[]`.
    """
    metadata = KeywordPresetTriggerMetadata([])
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__new__3():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: `AutoModerationKeywordPresetType.slur`.
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur)
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__new__4():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: `[AutoModerationKeywordPresetType.slur]`.
    """
    metadata = KeywordPresetTriggerMetadata([AutoModerationKeywordPresetType.slur])
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__new__5():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s raises as expected on bad parameter.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata(12.6)


def test__KeywordPresetTriggerMetadata__new__6():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s raises as expected on bad parameter.
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata([12.6])


def test__KeywordPresetTriggerMetadata__new__7():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: `AutoModerationKeywordPresetType.slur.value`.
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur.value)
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__new__8():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: `[AutoModerationKeywordPresetType.slur.value]`.
    """
    metadata = KeywordPresetTriggerMetadata([AutoModerationKeywordPresetType.slur.value])
    
    vampytest.assert_eq(metadata.keyword_presets, (AutoModerationKeywordPresetType.slur, ))


def test__KeywordPresetTriggerMetadata__new__9():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: *missing*.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__new__10():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.keyword_presets` as expected.
    Case: *None*.
    """
    metadata = KeywordPresetTriggerMetadata(None, None)
    
    vampytest.assert_is(metadata.keyword_presets, None)


def test__KeywordPresetTriggerMetadata__new__11():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.excluded_keywords` as expected.
    Case: `'owo'`.
    """
    metadata = KeywordPresetTriggerMetadata(None, 'owo')
    
    vampytest.assert_eq(metadata.excluded_keywords, ('owo', ))


def test__KeywordPresetTriggerMetadata__new__12():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` sets `.excluded_keywords` as expected.
    Case: `['owo']`.
    """
    metadata = KeywordPresetTriggerMetadata(None, ['owo'])
    
    vampytest.assert_eq(metadata.excluded_keywords, ('owo', ))

def test__KeywordPresetTriggerMetadata__new__13():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new__`` fails when `excluded_keywords` is given incorrectly.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata(None, 12.6)


def test__KeywordPresetTriggerMetadata__new__14():
    """
    Tests whether ``KeywordPresetTriggerMetadata.__new::`` fails when `excluded_keywords` is given incorrectly.
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordPresetTriggerMetadata(None, [12.6])
