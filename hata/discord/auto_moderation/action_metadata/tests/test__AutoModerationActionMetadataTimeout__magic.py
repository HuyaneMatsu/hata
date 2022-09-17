import vampytest

from .. import AutoModerationActionMetadataTimeout


def test__AutoModerationActionMetadataTimeout__eq__0():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationActionMetadataTimeout(0),
        AutoModerationActionMetadataTimeout(0),
    )

    vampytest.assert_not_eq(
        AutoModerationActionMetadataTimeout(0),
        AutoModerationActionMetadataTimeout(1),
    )


def test__AutoModerationActionMetadataTimeout__eq__1():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationActionMetadataTimeout(0),
        0,
    )


def test__AutoModerationActionMetadataTimeout__hash():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `__hash__` method works as intended
    """
    metadata = AutoModerationActionMetadataTimeout(0)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadataTimeout__repr():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `__repr__` method works as intended
    """
    metadata = AutoModerationActionMetadataTimeout(0)
    
    vampytest.assert_instance(repr(metadata), str)
