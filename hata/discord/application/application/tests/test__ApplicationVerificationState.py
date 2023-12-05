import vampytest

from ..preinstanced import ApplicationVerificationState


@vampytest.call_from(ApplicationVerificationState.INSTANCES.values())
def test__ApplicationVerificationState__instances(instance):
    """
    Tests whether ``ApplicationVerificationState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationVerificationState``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationVerificationState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationVerificationState.VALUE_TYPE)
