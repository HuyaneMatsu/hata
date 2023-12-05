import vampytest

from ..preinstanced import Status


@vampytest.call_from(Status.INSTANCES.values())
def test__Status__instances(instance):
    """
    Tests whether ``Status`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``Status``
        The instance to test.
    """
    vampytest.assert_instance(instance, Status)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, Status.VALUE_TYPE)
    vampytest.assert_instance(instance.position, int)


@vampytest.call_from(Status.INSTANCES.values())
def test__Status__repr(instance):
    """
    Tests whether ``Status.__repr__`` works as intended.
    
    Parameters
    ----------
    instance : ``Status``
        The instance to test.
    """
    vampytest.assert_instance(repr(instance), str)


def test__Status__sort():
    """
    Tests whether ``Status`` sorting works as intended.
    """
    vampytest.assert_eq(
        sorted(['idle', Status.online, 'your custom status', Status.dnd]),
        [Status.online, 'idle', Status.dnd, 'your custom status'],
    )
