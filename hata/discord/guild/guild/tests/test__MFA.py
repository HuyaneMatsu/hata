import vampytest

from ..preinstanced import MFA


@vampytest.call_from(MFA.INSTANCES.values())
def test__MFA__instances(instance):
    """
    Tests whether ``MFA`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MFA``
        The instance to test.
    """
    vampytest.assert_instance(instance, MFA)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MFA.VALUE_TYPE)
