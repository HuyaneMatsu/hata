import vampytest

from .. import KeywordTriggerMetadata


def test__KeywordTriggerMetadata__to_data__0():
    """
    Tests whether ``KeywordTriggerMetadata``'s `to_data` method works as expected.
    Defining no keyword(s).
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'keyword_filter': [],
        },
    )


def test__KeywordTriggerMetadata__to_data__1():
    """
    Tests whether ``KeywordTriggerMetadata``'s `to_data` method works as expected.
    Defining keyword(s).
    """
    metadata = KeywordTriggerMetadata('owo')
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'keyword_filter': ['owo'],
        },
    )


def test__KeywordTriggerMetadata__from_data__0():
    """
    Tests whether ``KeywordTriggerMetadata``'s `from_data` method works as expected.
    Case: `None`.
    """
    metadata = KeywordTriggerMetadata.from_data({
        'keyword_filter': None,
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordTriggerMetadata(None),
    )


def test__KeywordTriggerMetadata__from_data__1():
    """
    Tests whether ``KeywordTriggerMetadata``'s `from_data` method works as expected.
    Case: *missing*.
    """
    metadata = KeywordTriggerMetadata.from_data({})
    
    vampytest.assert_eq(
        metadata,
        KeywordTriggerMetadata(None),
    )


def test__KeywordTriggerMetadata__from_data__2():
    """
    Tests whether ``KeywordTriggerMetadata``'s `from_data` method works as expected.
    Case: `[]`.
    """
    metadata = KeywordTriggerMetadata.from_data({
        'keyword_filter': [],
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordTriggerMetadata(None),
    )


def test__KeywordTriggerMetadata__from_data__3():
    """
    Tests whether ``KeywordTriggerMetadata``'s `from_data` method works as expected.
    Case: `['owo']`.
    """
    metadata = KeywordTriggerMetadata.from_data({
        'keyword_filter': ['owo'],
    })
    
    vampytest.assert_eq(
        metadata,
        KeywordTriggerMetadata('owo'),
    )
