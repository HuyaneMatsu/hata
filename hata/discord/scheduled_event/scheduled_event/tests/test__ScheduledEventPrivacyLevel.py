import vampytest

from ..preinstanced import PrivacyLevel


@vampytest.call_from(PrivacyLevel.INSTANCES.values())
def test__PrivacyLevel__instances(instance):
    """
    Tests whether ``PrivacyLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``PrivacyLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, PrivacyLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, PrivacyLevel.VALUE_TYPE)
