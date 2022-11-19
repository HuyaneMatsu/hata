import vampytest

from ..keyword import AutoModerationRuleTriggerMetadataKeyword


def test__AutoModerationRuleTriggerMetadataKeyword__eq():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__eq__`` works as intended.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    keyword_parameters = {
        'excluded_keywords': excluded_keywords,
        'keywords': keywords,
        'regex_patterns': regex_patterns,
    }
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    
    for field_name, field_value in (
        ('excluded_keywords', None),
        ('keywords', None),
        ('regex_patterns', None),
    ):
        test_metadata = AutoModerationRuleTriggerMetadataKeyword(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
        

def test__AutoModerationRuleTriggerMetadataKeyword__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__hash__`` works as intended.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(
        keywords,
        regex_patterns,
        excluded_keywords = excluded_keywords,
    )
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataKeyword__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__repr__`` works as intended.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(
        keywords,
        regex_patterns,
        excluded_keywords = excluded_keywords,
    )
    
    vampytest.assert_instance(repr(metadata), str)
