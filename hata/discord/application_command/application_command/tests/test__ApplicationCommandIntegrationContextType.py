import vampytest

from ..preinstanced import ApplicationCommandIntegrationContextType


@vampytest.call_from(ApplicationCommandIntegrationContextType.INSTANCES.values())
def test__ApplicationCommandIntegrationContextType__instances(instance):
    """
    Tests whether ``ApplicationCommandIntegrationContextType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationCommandIntegrationContextType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationCommandIntegrationContextType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationCommandIntegrationContextType.VALUE_TYPE)
