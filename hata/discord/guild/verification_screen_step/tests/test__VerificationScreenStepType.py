import vampytest

from ..preinstanced import VerificationScreenStepType


def test__VerificationScreenStepType__name():
    """
    Tests whether ``VerificationScreenStepType`` instance names are all strings.
    """
    for instance in VerificationScreenStepType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__VerificationScreenStepType__value():
    """
    Tests whether ``VerificationScreenStepType`` instance values are all the expected value type.
    """
    for instance in VerificationScreenStepType.INSTANCES.values():
        vampytest.assert_instance(instance.value, VerificationScreenStepType.VALUE_TYPE)
