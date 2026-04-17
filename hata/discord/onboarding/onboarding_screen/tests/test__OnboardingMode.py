import vampytest

from ..preinstanced import OnboardingMode


@vampytest.call_from(OnboardingMode.INSTANCES.values())
def test__OnboardingMode__instances(instance):
    """
    Tests whether ``OnboardingMode`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``OnboardingMode``
        The instance to test.
    """
    vampytest.assert_instance(instance, OnboardingMode)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, OnboardingMode.VALUE_TYPE)
