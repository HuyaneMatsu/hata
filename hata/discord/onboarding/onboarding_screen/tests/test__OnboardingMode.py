import vampytest

from ..preinstanced import OnboardingMode


def test__OnboardingMode__name():
    """
    Tests whether ``OnboardingMode`` instance names are all strings.
    """
    for instance in OnboardingMode.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__OnboardingMode__value():
    """
    Tests whether ``OnboardingMode`` instance values are all the expected value type.
    """
    for instance in OnboardingMode.INSTANCES.values():
        vampytest.assert_instance(instance.value, OnboardingMode.VALUE_TYPE)
