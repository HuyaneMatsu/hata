import vampytest

from ..preinstanced import FriendRequestFlag


def test__FriendRequestFlag__name():
    """
    Tests whether ``FriendRequestFlag`` instance names are all strings.
    """
    for instance in FriendRequestFlag.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__FriendRequestFlag__value():
    """
    Tests whether ``FriendRequestFlag`` instance values are all the expected value type.
    """
    for instance in FriendRequestFlag.INSTANCES.values():
        vampytest.assert_instance(instance.value, FriendRequestFlag.VALUE_TYPE)


def test__FriendRequestFlag__encode():
    """
    Tests whether ``FriendRequestFlag.encode`` works as intended.
    """
    for instance in FriendRequestFlag.INSTANCES.values():
        vampytest.assert_instance(instance.encode(), dict)


def test__FriendRequestFlag__get():
    """
    Tests whether ``FriendRequestFlag.get`` works as intended.
    """
    for instance in FriendRequestFlag.INSTANCES.values():
        vampytest.assert_is(FriendRequestFlag.get(instance.encode()), instance)
