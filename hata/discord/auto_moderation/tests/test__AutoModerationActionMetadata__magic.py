import vampytest

from .. import AutoModerationActionMetadata


def test__AutoModerationActionMetadata__eq_0():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationActionMetadata(),
        AutoModerationActionMetadata(),
    )


def test__AutoModerationActionMetadata__eq_1():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationActionMetadata(),
        0,
    )


def test__AutoModerationActionMetadata__hash():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__hash__` method works as intended
    """
    metadata = AutoModerationActionMetadata()
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadata__repr():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__repr__` method works as intended
    """
    metadata = AutoModerationActionMetadata()
    
    vampytest.assert_instance(repr(metadata), str)
