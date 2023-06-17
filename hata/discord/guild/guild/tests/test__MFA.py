import vampytest

from ..preinstanced import MFA


def test__MFA__name():
    """
    Tests whether ``MFA`` instance names are all strings.
    """
    for instance in MFA.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__MFA__value():
    """
    Tests whether ``MFA`` instance values are all the expected value type.
    """
    for instance in MFA.INSTANCES.values():
        vampytest.assert_instance(instance.value, MFA.VALUE_TYPE)
