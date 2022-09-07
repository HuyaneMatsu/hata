import vampytest

from .. import KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType


def test__KeywordPresetTriggerMetadata__to_data__0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `to_data` method works as expected.
    Defining no keyword(s).
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'presets': [],
            'allow_list': [],
        },
    )


def test__KeywordPresetTriggerMetadata__to_data__1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `to_data` method works as expected.
    Defining keyword(s).
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur, 'owo')
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'presets': [AutoModerationKeywordPresetType.slur.value],
            'allow_list': ['owo']
        },
    )


def test__KeywordPresetTriggerMetadata__from_data__0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    None value cases.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({
        'presets': None,
        'allow_list': None,
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(None),
    )


def test__KeywordPresetTriggerMetadata__from_data__1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    Missing data case.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({})
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(None),
    )


def test__KeywordPresetTriggerMetadata__from_data__2():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    Empty data case.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({
        'presets': [],
        'allow_list': [],
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(None),
    )


def test__KeywordPresetTriggerMetadata__from_data__3():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `from_data` method works as expected.
    Stuffed data case.
    """
    metadata = KeywordPresetTriggerMetadata.from_data({
        'presets': [AutoModerationKeywordPresetType.slur.value],
        'allow_list': ['owo'],
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur, 'owo'),
    )
