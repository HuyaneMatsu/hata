import vampytest

from .. import KeywordTriggerMetadata


def test__KeywordTriggerMetadata__eq_0():
    """
    Tests whether ``KeywordTriggerMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        KeywordTriggerMetadata(None),
        KeywordTriggerMetadata(None),
    )


def test__KeywordTriggerMetadata__eq_1():
    """
    Tests whether ``KeywordTriggerMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        KeywordTriggerMetadata(None),
        0,
    )


def test__KeywordTriggerMetadata__not_eq_0():
    """
    Tests whether ``KeywordTriggerMetadata``'s `__eq__` method works as expected when passing
    objects with different values.
    """
    vampytest.assert_not_eq(
        KeywordTriggerMetadata(None),
        KeywordTriggerMetadata('owo'),
    )


def test__KeywordTriggerMetadata__hash():
    """
    Tests whether ``KeywordTriggerMetadata``'s `__hash__` method works as intended
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_instance(hash(metadata), int)


def test__KeywordTriggerMetadata__repr():
    """
    Tests whether ``KeywordTriggerMetadata``'s `__repr__` method works as intended
    """
    metadata = KeywordTriggerMetadata(None)
    
    vampytest.assert_instance(repr(metadata), str)
