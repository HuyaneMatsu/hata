import vampytest

from ..preinstanced import IntegrationType


def test__IntegrationType__name():
    """
    Tests whether ``IntegrationType`` instance names are all strings.
    """
    for instance in IntegrationType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__IntegrationType__value():
    """
    Tests whether ``IntegrationType`` instance values are all the expected value type.
    """
    for instance in IntegrationType.INSTANCES.values():
        vampytest.assert_instance(instance.value, IntegrationType.VALUE_TYPE)
