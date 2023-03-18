import vampytest

from ..preinstanced import PrivacyLevel


def test__PrivacyLevel__name():
    """
    Tests whether ``PrivacyLevel`` instance names are all strings.
    """
    for instance in PrivacyLevel.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__PrivacyLevel__value():
    """
    Tests whether ``PrivacyLevel`` instance values are all the expected value type.
    """
    for instance in PrivacyLevel.INSTANCES.values():
        vampytest.assert_instance(instance.value, PrivacyLevel.VALUE_TYPE)
