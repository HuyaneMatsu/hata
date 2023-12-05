import vampytest

from ..preinstanced import FriendRequestFlag


@vampytest.call_from(FriendRequestFlag.INSTANCES.values())
def test__FriendRequestFlag__instances(instance):
    """
    Tests whether ``FriendRequestFlag`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``FriendRequestFlag``
        The instance to test.
    """
    vampytest.assert_instance(instance, FriendRequestFlag)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, FriendRequestFlag.VALUE_TYPE)


@vampytest.call_from(FriendRequestFlag.INSTANCES.values())
def test__FriendRequestFlag__encode(instance):
    """
    Tests whether ``FriendRequestFlag.encode`` works as intended.
    
    Parameters
    ----------
    instance : ``FriendRequestFlag``
        The instance to test.
    """
    vampytest.assert_instance(instance.encode(), dict)


@vampytest.call_from(FriendRequestFlag.INSTANCES.values())
def test__FriendRequestFlag__get(instance):
    """
    Tests whether ``FriendRequestFlag.get`` works as intended.
    
    Parameters
    ----------
    instance : ``FriendRequestFlag``
        The instance to test.
    """
    vampytest.assert_is(FriendRequestFlag.get(instance.encode()), instance)
