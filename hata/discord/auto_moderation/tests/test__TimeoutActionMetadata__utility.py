import vampytest

from .. import TimeoutActionMetadata


def test__TimeoutActionMetadata__copy():
    """
    Tests whether ``TimeoutActionMetadata``'s `copy` method works as expected.
    """
    metadata = TimeoutActionMetadata(0)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
