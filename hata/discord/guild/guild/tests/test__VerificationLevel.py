import vampytest

from ..preinstanced import VerificationLevel


@vampytest.call_from(VerificationLevel.INSTANCES.values())
def test__VerificationLevel__instances(instance):
    """
    Tests whether ``VerificationLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``VerificationLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, VerificationLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, VerificationLevel.VALUE_TYPE)
