import vampytest

from ..keyword import AutoModerationRuleTriggerMetadataKeyword

from .test__AutoModerationRuleTriggerMetadataKeyword__constructor import _assert_is_every_attribute_set


def test__AutoModerationRuleTriggerMetadataKeyword__copy():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.copy`` works as intended.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(
        keywords,
        regex_patterns,
        excluded_keywords = excluded_keywords,
    )
    
    copy = metadata.copy()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataKeyword__copy_with__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.copy_with`` works as intended.
    
    Case: No fields.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(
        keywords,
        regex_patterns,
        excluded_keywords = excluded_keywords,
    )
    
    copy = metadata.copy_with()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataKeyword__copy_with__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_excluded_keywords = ['find', 'way',  'your']
    new_excluded_keywords = ['flower', 'other', 'the']
    old_keywords = ['Howling', 'Moon']
    new_keywords = ['suika']
    old_regex_patterns = ['apple', 'peach']
    new_regex_patterns = ['suwako']
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(
        old_keywords,
        old_regex_patterns,
        excluded_keywords = old_excluded_keywords,
    )
    
    copy = metadata.copy_with(
        excluded_keywords = new_excluded_keywords,
        keywords = new_keywords,
        regex_patterns = new_regex_patterns,
    )
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_is_not(metadata, copy)
    
    vampytest.assert_eq(copy.excluded_keywords, tuple(new_excluded_keywords))
    vampytest.assert_eq(copy.keywords, tuple(new_keywords))
    vampytest.assert_eq(copy.regex_patterns, tuple(new_regex_patterns))


def test__AutoModerationRuleTriggerMetadataKeyword__iter_excluded_keywords():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.iter_excluded_keywords`` works as intended.
    """
    old_excluded_keywords = ['find', 'way',  'your']
    
    for input_keyword_presents, expected_output in (
        (None, []),
        (old_excluded_keywords, old_excluded_keywords),
    ):
        metadata = AutoModerationRuleTriggerMetadataKeyword(excluded_keywords = input_keyword_presents)
        vampytest.assert_eq([*metadata.iter_excluded_keywords()], expected_output)


def test__AutoModerationRuleTriggerMetadataKeyword__iter_keywords():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.iter_keywords`` works as intended.
    """
    keyword_presents = ['koishi', 'orin']
    
    for input_keyword_presents, expected_output in (
        (None, []),
        (keyword_presents, keyword_presents),
    ):
        metadata = AutoModerationRuleTriggerMetadataKeyword(keywords = input_keyword_presents)
        vampytest.assert_eq([*metadata.iter_keywords()], expected_output)


def test__AutoModerationRuleTriggerMetadataKeyword__iter_regex_patterns():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.iter_regex_patterns`` works as intended.
    """
    old_regex_patterns = ['apple', 'peach']
    
    for input_keyword_presents, expected_output in (
        (None, []),
        (old_regex_patterns, old_regex_patterns),
    ):
        metadata = AutoModerationRuleTriggerMetadataKeyword(regex_patterns = input_keyword_presents)
        vampytest.assert_eq([*metadata.iter_regex_patterns()], expected_output)
