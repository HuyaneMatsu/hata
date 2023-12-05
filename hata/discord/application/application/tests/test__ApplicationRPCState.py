import vampytest

from ..preinstanced import ApplicationRPCState


@vampytest.call_from(ApplicationRPCState.INSTANCES.values())
def test__ApplicationRPCState__instances(instance):
    """
    Tests whether ``ApplicationRPCState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationRPCState``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationRPCState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationRPCState.VALUE_TYPE)
