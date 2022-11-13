import vampytest

from ..preinstanced import Status


def test__Status__name():
    """
    Tests whether ``Status`` instance names are all strings.
    """
    for instance in Status.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__Status__value():
    """
    Tests whether ``Status`` instance values are all the expected value type.
    """
    for instance in Status.INSTANCES.values():
        vampytest.assert_instance(instance.value, Status.VALUE_TYPE)


def test__Status__position():
    """
    Tests whether ``Status`` instance positions are all strings.
    """
    for instance in Status.INSTANCES.values():
        vampytest.assert_instance(instance.position, int)


def test__Status__repr():
    """
    Tests whether ``Status.__repr__`` works as intended..
    """
    for instance in Status.INSTANCES.values():
        vampytest.assert_instance(repr(Status.online), str)


def test__Status__sort():
    """
    Tests whether ``Status`` sorting works as intended..
    """
    vampytest.assert_eq(
        sorted(['idle', Status.online, 'your custom status', Status.dnd]),
        [Status.online, 'idle', Status.dnd, 'your custom status'],
    )
