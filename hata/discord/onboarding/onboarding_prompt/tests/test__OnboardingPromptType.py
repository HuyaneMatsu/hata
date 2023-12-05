import vampytest

from ..preinstanced import OnboardingPromptType


@vampytest.call_from(OnboardingPromptType.INSTANCES.values())
def test__OnboardingPromptType__instances(instance):
    """
    Tests whether ``OnboardingPromptType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``OnboardingPromptType``
        The instance to test.
    """
    vampytest.assert_instance(instance, OnboardingPromptType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, OnboardingPromptType.VALUE_TYPE)
