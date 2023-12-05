import vampytest

from ..preinstanced import ApplicationType


@vampytest.call_from(ApplicationType.INSTANCES.values())
def test__ApplicationType__instances(instance):
    """
    Tests whether ``ApplicationType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationType.VALUE_TYPE)
