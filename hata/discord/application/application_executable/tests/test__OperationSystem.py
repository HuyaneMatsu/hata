import vampytest

from ..preinstanced import OperationSystem


@vampytest.call_from(OperationSystem.INSTANCES.values())
def test__OperationSystem__instances(instance):
    """
    Tests whether ``OperationSystem`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``OperationSystem``
        The instance to test.
    """
    vampytest.assert_instance(instance, OperationSystem)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, OperationSystem.VALUE_TYPE)
