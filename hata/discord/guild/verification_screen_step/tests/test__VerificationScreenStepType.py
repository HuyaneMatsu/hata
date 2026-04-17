import vampytest

from ..preinstanced import VerificationScreenStepType


@vampytest.call_from(VerificationScreenStepType.INSTANCES.values())
def test__VerificationScreenStepType__instances(instance):
    """
    Tests whether ``VerificationScreenStepType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``VerificationScreenStepType``
        The instance to test.
    """
    vampytest.assert_instance(instance, VerificationScreenStepType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, VerificationScreenStepType.VALUE_TYPE)
