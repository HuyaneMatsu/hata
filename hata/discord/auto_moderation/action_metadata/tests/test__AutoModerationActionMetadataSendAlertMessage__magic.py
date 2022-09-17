import vampytest

from .. import AutoModerationActionMetadataSendAlertMessage


def test__AutoModerationActionMetadataSendAlertMessage__eq__0():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationActionMetadataSendAlertMessage(0),
        AutoModerationActionMetadataSendAlertMessage(0),
    )

    vampytest.assert_not_eq(
        AutoModerationActionMetadataSendAlertMessage(0),
        AutoModerationActionMetadataSendAlertMessage(1),
    )


def test__AutoModerationActionMetadataSendAlertMessage__eq__1():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationActionMetadataSendAlertMessage(0),
        0,
    )


def test__AutoModerationActionMetadataSendAlertMessage__hash():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `__hash__` method works as intended
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(0)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadataSendAlertMessage__repr():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `__repr__` method works as intended
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(0)
    
    vampytest.assert_instance(repr(metadata), str)
