import vampytest

from .. import KeywordTriggerMetadata


def test__KeywordTriggerMetadata__copy__0():
    """
    Tests whether ``KeywordTriggerMetadata.copy`` method works as expected.
    
    Case: no keywords.
    """
    metadata = KeywordTriggerMetadata(None)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__KeywordTriggerMetadata__copy__1():
    """
    Tests whether ``KeywordTriggerMetadata.copy`` method works as expected.
    
    Case: *n* keyword(s).
    """
    metadata = KeywordTriggerMetadata('owo')
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__KeywordTriggerMetadata__iter_keywords__0():
    """
    Tests whether ``KeywordTriggerMetadata.iter_keywords`` method works as expected.
    
    Case: no keywords.
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_eq([*metadata.iter_keywords()], [])


def test__KeywordTriggerMetadata__iter_keywords__1():
    """
    Tests whether ``KeywordTriggerMetadata.iter_keywords`` method works as expected.
    
    Case: *n* keyword(s).
    """
    metadata = KeywordTriggerMetadata('owo')
    
    vampytest.assert_eq([*metadata.iter_keywords()], ['owo'])
