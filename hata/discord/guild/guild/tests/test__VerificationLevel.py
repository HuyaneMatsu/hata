import vampytest

from ..preinstanced import VerificationLevel


def test__VerificationLevel__name():
    """
    Tests whether ``VerificationLevel`` instance names are all strings.
    """
    for instance in VerificationLevel.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__VerificationLevel__value():
    """
    Tests whether ``VerificationLevel`` instance values are all the expected value type.
    """
    for instance in VerificationLevel.INSTANCES.values():
        vampytest.assert_instance(instance.value, VerificationLevel.VALUE_TYPE)
