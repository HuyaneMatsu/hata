import vampytest

from ..preinstanced import OperationSystem


def test__OperationSystem__name():
    """
    Tests whether ``OperationSystem`` instance names are all strings.
    """
    for instance in OperationSystem.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__OperationSystem__value():
    """
    Tests whether ``OperationSystem`` instance values are all the expected value type.
    """
    for instance in OperationSystem.INSTANCES.values():
        vampytest.assert_instance(instance.value, OperationSystem.VALUE_TYPE)
