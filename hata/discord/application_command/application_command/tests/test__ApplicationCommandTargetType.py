import vampytest

from ..preinstanced import ApplicationCommandTargetType


@vampytest.call_from(ApplicationCommandTargetType.INSTANCES.values())
def test__ApplicationCommandTargetType__instances(instance):
    """
    Tests whether ``ApplicationCommandTargetType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationCommandTargetType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationCommandTargetType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationCommandTargetType.VALUE_TYPE)
