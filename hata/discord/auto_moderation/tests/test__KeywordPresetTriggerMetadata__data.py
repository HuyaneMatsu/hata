import vampytest

from .. import KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType


def test__KeywordPresetTriggerMetadata__to_data_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `to_data` method works as expected.
    Defining no keyword(s).
    """
    metadata = KeywordPresetTriggerMetadata(keyword_presets=None)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'presets': [],
        },
    )


def test__KeywordPresetTriggerMetadata__to_data_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `to_data` method works as expected.
    Defining keyword(s).
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'presets': [AutoModerationKeywordPresetType.slur.value],
        },
    )


def test__KeywordPresetTriggerMetadata__from_data_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    Case: `None`.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({
        'presets': None,
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(keyword_presets=None),
    )


def test__KeywordPresetTriggerMetadata__from_data_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    Case: *missing*.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({})
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(None),
    )


def test__KeywordPresetTriggerMetadata__from_data_2():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    Case: `[]`.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({
        'presets': [],
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(None),
    )


def test__KeywordPresetTriggerMetadata__from_data_3():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    Case: `['owo']`.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({
        'presets': [AutoModerationKeywordPresetType.slur.value],
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(keyword_presets=AutoModerationKeywordPresetType.slur),
    )
