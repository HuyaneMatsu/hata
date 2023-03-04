import vampytest

from ..preinstanced import OnboardingPromptType


def test__OnboardingPromptType__name():
    """
    Tests whether ``OnboardingPromptType`` instance names are all strings.
    """
    for instance in OnboardingPromptType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__OnboardingPromptType__value():
    """
    Tests whether ``OnboardingPromptType`` instance values are all the expected value type.
    """
    for instance in OnboardingPromptType.INSTANCES.values():
        vampytest.assert_instance(instance.value, OnboardingPromptType.VALUE_TYPE)
