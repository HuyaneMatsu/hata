import vampytest

from ...channel import Channel

from .. import TimeoutActionMetadata


def test__TimeoutActionMetadata__constructor_0():
    """
    Tests whether ``TimeoutActionMetadata``'s constructor returns as expected.
    """
    metadata = TimeoutActionMetadata(0)
    
    vampytest.assert_instance(metadata, TimeoutActionMetadata)


def test__TimeoutActionMetadata__constructor_1():
    """
    Tests whether ``TimeoutActionMetadata``'s constructor works as expected.
    Passing parameter as `None`
    """
    metadata = TimeoutActionMetadata(None)
    
    vampytest.assert_eq(metadata.duration, 0)


def test__TimeoutActionMetadata__constructor_2():
    """
    Tests whether ``TimeoutActionMetadata``'s constructor works as expected.
    Passing parameter as `int`
    """
    metadata = TimeoutActionMetadata(69)
    
    vampytest.assert_eq(metadata.duration, 69)


def test__TimeoutActionMetadata__constructor_3():
    """
    Tests whether ``TimeoutActionMetadata``'s constructor works as expected.
    Passing parameter as ``float``
    """
    metadata = TimeoutActionMetadata(69.0)
    
    vampytest.assert_eq(metadata.duration, 69)
