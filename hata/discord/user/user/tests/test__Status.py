import vampytest

from ..preinstanced import Status


def _assert_fields_set(status):
    """
    Asserts whether every field are set of the given status.
    
    Parameters
    ----------
    status : ``Status``
        The instance to test.
    """
    vampytest.assert_instance(status, Status)
    vampytest.assert_instance(status.name, str)
    vampytest.assert_instance(status.value, Status.VALUE_TYPE)
    vampytest.assert_instance(status.position, int)


@vampytest.call_from(Status.INSTANCES.values())
def test__Status__instances(instance):
    """
    Tests whether ``Status`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``Status``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__Status__new__min_fields():
    """
    Tests whether ``Status.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 'potato'
    
    try:
        output = Status(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, value)
        vampytest.assert_eq(output.position, 4)
        vampytest.assert_is(Status.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del Status.INSTANCES[value]
        except KeyError:
            pass


def test__Status__sort():
    """
    Tests whether ``Status`` sorting works as intended.
    """
    vampytest.assert_eq(
        sorted(['idle', Status.online, 'your custom status', Status.dnd]),
        [Status.online, 'idle', Status.dnd, 'your custom status'],
    )
