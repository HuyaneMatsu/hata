import vampytest

from .. import KeywordTriggerMetadata


def test__KeywordTriggerMetadata__copy_0():
    """
    Tests whether ``KeywordTriggerMetadata``'s `copy` method works as expected.
    Case: no keywords.
    """
    metadata = KeywordTriggerMetadata(None)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__KeywordTriggerMetadata__copy_1():
    """
    Tests whether ``KeywordTriggerMetadata``'s `copy` method works as expected.
    Case: *n* keyword(s).
    """
    metadata = KeywordTriggerMetadata('owo')
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__KeywordTriggerMetadata__iter_keywords_0():
    """
    Tests whether ``KeywordTriggerMetadata``'s `iter_keywords` method works as expected.
    Case: no keywords.
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_eq([*metadata.iter_keywords()], [])


def test__KeywordTriggerMetadata__iter_keywords_1():
    """
    Tests whether ``KeywordTriggerMetadata``'s `iter_keywords` method works as expected.
    Case: *n* keyword(s).
    """
    metadata = KeywordTriggerMetadata('owo')
    
    vampytest.assert_eq([*metadata.iter_keywords()], ['owo'])
