import vampytest

from .. import TimeoutActionMetadata


def test__TimeoutActionMetadata__eq_0():
    """
    Tests whether ``TimeoutActionMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        TimeoutActionMetadata(0),
        TimeoutActionMetadata(0),
    )

    vampytest.assert_not_eq(
        TimeoutActionMetadata(0),
        TimeoutActionMetadata(1),
    )


def test__TimeoutActionMetadata__eq_1():
    """
    Tests whether ``TimeoutActionMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        TimeoutActionMetadata(0),
        0,
    )


def test__TimeoutActionMetadata__hash():
    """
    Tests whether ``TimeoutActionMetadata``'s `__hash__` method works as intended
    """
    metadata = TimeoutActionMetadata(0)
    
    vampytest.assert_instance(hash(metadata), int)


def test__TimeoutActionMetadata__repr():
    """
    Tests whether ``TimeoutActionMetadata``'s `__repr__` method works as intended
    """
    metadata = TimeoutActionMetadata(0)
    
    vampytest.assert_instance(repr(metadata), str)
