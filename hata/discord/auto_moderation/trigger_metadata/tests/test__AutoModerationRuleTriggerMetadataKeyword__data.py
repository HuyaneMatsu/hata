import vampytest

from ..keyword import AutoModerationRuleTriggerMetadataKeyword

from .test__AutoModerationRuleTriggerMetadataKeyword__constructor import _assert_is_every_attribute_set


def test__AutoModerationRuleTriggerMetadataKeyword__to_data():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.to_data`` works as intended.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(
        keywords,
        regex_patterns,
        excluded_keywords = excluded_keywords,
    )
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        {
            'allow_list': excluded_keywords,
            'keyword_filter': keywords,
            'regex_patterns': regex_patterns,
        },
    )


def test__AutoModerationRuleTriggerMetadataKeyword__from_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.from_data`` works as intended.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    data = {
        'allow_list': excluded_keywords,
        'keyword_filter': keywords,
        'regex_patterns': regex_patterns,
    }
    
    metadata = AutoModerationRuleTriggerMetadataKeyword.from_data(data)
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.excluded_keywords, tuple(excluded_keywords))
    vampytest.assert_eq(metadata.keywords, tuple(keywords))
    vampytest.assert_eq(metadata.regex_patterns, tuple(regex_patterns))
