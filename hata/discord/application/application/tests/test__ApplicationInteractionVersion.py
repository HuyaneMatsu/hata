import vampytest

from ..preinstanced import ApplicationInteractionVersion


@vampytest.call_from(ApplicationInteractionVersion.INSTANCES.values())
def test__ApplicationInteractionVersion__instances(instance):
    """
    Tests whether ``ApplicationInteractionVersion`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationInteractionVersion``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationInteractionVersion)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationInteractionVersion.VALUE_TYPE)
