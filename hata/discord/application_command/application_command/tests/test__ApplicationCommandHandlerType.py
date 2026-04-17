import vampytest

from ..preinstanced import ApplicationCommandHandlerType


@vampytest.call_from(ApplicationCommandHandlerType.INSTANCES.values())
def test__ApplicationCommandHandlerType__instances(instance):
    """
    Tests whether ``ApplicationCommandHandlerType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationCommandHandlerType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationCommandHandlerType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationCommandHandlerType.VALUE_TYPE)
