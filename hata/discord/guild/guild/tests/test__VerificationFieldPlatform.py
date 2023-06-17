import vampytest

from ..preinstanced import VerificationFieldPlatform


def test__VerificationFieldPlatform__name():
    """
    Tests whether ``VerificationFieldPlatform`` instance names are all strings.
    """
    for instance in VerificationFieldPlatform.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__VerificationFieldPlatform__value():
    """
    Tests whether ``VerificationFieldPlatform`` instance values are all the expected value type.
    """
    for instance in VerificationFieldPlatform.INSTANCES.values():
        vampytest.assert_instance(instance.value, VerificationFieldPlatform.VALUE_TYPE)
