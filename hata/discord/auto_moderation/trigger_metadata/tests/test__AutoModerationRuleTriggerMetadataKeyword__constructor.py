import vampytest

from ..keyword import AutoModerationRuleTriggerMetadataKeyword


def _assert_is_every_attribute_set(metadata):
    """
    Asserts whether all attributes are set of the given rule trigger metadata.
    
    Parameters
    ----------
    metadata : ``AutoModerationRuleTriggerMetadataKeyword``
        The metadata object to check.
    """
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataKeyword)
    vampytest.assert_instance(metadata.excluded_keywords, tuple, nullable = True)
    vampytest.assert_instance(metadata.keywords, tuple, nullable = True)
    vampytest.assert_instance(metadata.regex_patterns, tuple, nullable = True)


def test__AutoModerationRuleTriggerMetadataKeyword__new__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` works as intended.
    
    Case: No fields.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword()
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataKeyword)


def test__AutoModerationRuleTriggerMetadataKeyword__new__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` works as intended.
    
    Case: All fields.
    """
    excluded_keywords = ['find', 'way',  'your']
    keywords = ['Howling', 'Moon']
    regex_patterns = ['apple', 'peach']
    
    metadata = AutoModerationRuleTriggerMetadataKeyword(
        keywords,
        regex_patterns,
        excluded_keywords = excluded_keywords
    )
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.keywords, tuple(keywords))
    vampytest.assert_eq(metadata.regex_patterns, tuple(regex_patterns))
