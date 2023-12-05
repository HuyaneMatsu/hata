import vampytest

from ..preinstanced import InteractionResponseType


@vampytest.call_from(InteractionResponseType.INSTANCES.values())
def test__InteractionResponseType__instances(instance):
    """
    Tests whether ``InteractionResponseType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``InteractionResponseType``
        The instance to test.
    """
    vampytest.assert_instance(instance, InteractionResponseType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, InteractionResponseType.VALUE_TYPE)
