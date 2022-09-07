import vampytest

from .. import KeywordTriggerMetadata


def test__KeywordTriggerMetadata__new__0():
    """
    Tests whether ``KeywordTriggerMetadata.__new__`` returns as expected.
    
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_instance(metadata, KeywordTriggerMetadata)


def test__KeywordTriggerMetadata__new__1():
    """
    Tests whether ``KeywordTriggerMetadata.__new__`` sets `.keywords` as expected.
    
    Case: `None`.
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_is(metadata.keywords, None)


def test__KeywordTriggerMetadata__new__2():
    """
    Tests whether ``KeywordTriggerMetadata.__new__`` sets `.keywords` as expected.
    
    Case: `[]`.
    """
    metadata = KeywordTriggerMetadata([])
    
    vampytest.assert_is(metadata.keywords, None)


def test__KeywordTriggerMetadata__new__3():
    """
    Tests whether ``KeywordTriggerMetadata.__new__`` sets `.keywords` as expected.
    
    Case: `'owo'`.
    """
    metadata = KeywordTriggerMetadata('owo')
    
    vampytest.assert_eq(metadata.keywords, ('owo', ))


def test__KeywordTriggerMetadata__new__4():
    """
    Tests whether ``KeywordTriggerMetadata.__new__`` sets `.keywords` as expected.
    Case: `['owo']`.
    """
    metadata = KeywordTriggerMetadata(['owo'])
    
    vampytest.assert_eq(metadata.keywords, ('owo', ))


def test__KeywordTriggerMetadata__new__5():
    """
    Tests whether ``KeywordTriggerMetadata.__new__`` raises as expected on bad parameter.
    
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordTriggerMetadata(12.6)


def test__KeywordTriggerMetadata__new__6():
    """
    Tests whether ``KeywordTriggerMetadata.__new__`` raises as expected on bad parameter.
    
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordTriggerMetadata([12.6])
