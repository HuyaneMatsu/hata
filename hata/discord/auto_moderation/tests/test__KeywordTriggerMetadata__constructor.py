import vampytest

from .. import KeywordTriggerMetadata


def test__KeywordTriggerMetadata__constructor_0():
    """
    Tests whether ``KeywordTriggerMetadata``'s constructor returns as expected.
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_instance(metadata, KeywordTriggerMetadata)


def test__KeywordTriggerMetadata__constructor_1():
    """
    Tests whether ``KeywordTriggerMetadata``'s constructor sets `.keywords` as expected.
    Case: `None`.
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_is(metadata.keywords, None)


def test__KeywordTriggerMetadata__constructor_2():
    """
    Tests whether ``KeywordTriggerMetadata``'s constructor sets `.keywords` as expected.
    Case: `[]`.
    """
    metadata = KeywordTriggerMetadata([])
    
    vampytest.assert_is(metadata.keywords, None)


def test__KeywordTriggerMetadata__constructor_3():
    """
    Tests whether ``KeywordTriggerMetadata``'s constructor sets `.keywords` as expected.
    Case: `'owo'`.
    """
    metadata = KeywordTriggerMetadata('owo')
    
    vampytest.assert_eq(metadata.keywords, ('owo', ))


def test__KeywordTriggerMetadata__constructor_4():
    """
    Tests whether ``KeywordTriggerMetadata``'s constructor sets `.keywords` as expected.
    Case: `['owo']`.
    """
    metadata = KeywordTriggerMetadata(['owo'])
    
    vampytest.assert_eq(metadata.keywords, ('owo', ))


def test__KeywordTriggerMetadata__constructor_5():
    """
    Tests whether ``KeywordTriggerMetadata``'s raises as expected on bad parameter.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordTriggerMetadata(12.6)


def test__KeywordTriggerMetadata__constructor_6():
    """
    Tests whether ``KeywordTriggerMetadata``'s raises as expected on bad parameter.
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        KeywordTriggerMetadata([12.6])
