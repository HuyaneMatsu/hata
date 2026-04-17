import vampytest

from ..preinstanced import MfaLevel


@vampytest.call_from(MfaLevel.INSTANCES.values())
def test__MfaLevel__instances(instance):
    """
    Tests whether ``MfaLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MfaLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, MfaLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MfaLevel.VALUE_TYPE)
