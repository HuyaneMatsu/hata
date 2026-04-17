import vampytest

from ..preinstanced import VerificationFieldPlatform


@vampytest.call_from(VerificationFieldPlatform.INSTANCES.values())
def test__VerificationFieldPlatform__instances(instance):
    """
    Tests whether ``VerificationFieldPlatform`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``VerificationFieldPlatform``
        The instance to test.
    """
    vampytest.assert_instance(instance, VerificationFieldPlatform)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, VerificationFieldPlatform.VALUE_TYPE)
