import vampytest

from .. import SendAlertMessageActionMetadata


def test__SendAlertMessageActionMetadata__eq_0():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        SendAlertMessageActionMetadata(0),
        SendAlertMessageActionMetadata(0),
    )

    vampytest.assert_not_eq(
        SendAlertMessageActionMetadata(0),
        SendAlertMessageActionMetadata(1),
    )


def test__SendAlertMessageActionMetadata__eq_1():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        SendAlertMessageActionMetadata(0),
        0,
    )


def test__SendAlertMessageActionMetadata__hash():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s `__hash__` method works as intended
    """
    metadata = SendAlertMessageActionMetadata(0)
    
    vampytest.assert_instance(hash(metadata), int)


def test__SendAlertMessageActionMetadata__repr():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s `__repr__` method works as intended
    """
    metadata = SendAlertMessageActionMetadata(0)
    
    vampytest.assert_instance(repr(metadata), str)
