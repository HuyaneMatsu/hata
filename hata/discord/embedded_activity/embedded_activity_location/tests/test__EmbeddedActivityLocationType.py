import vampytest

from ..preinstanced import EmbeddedActivityLocationType


@vampytest.call_from(EmbeddedActivityLocationType.INSTANCES.values())
def test__EmbeddedActivityLocationType__instances(instance):
    """
    Tests whether ``EmbeddedActivityLocationType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``EmbeddedActivityLocationType``
        The instance to test.
    """
    vampytest.assert_instance(instance, EmbeddedActivityLocationType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, EmbeddedActivityLocationType.VALUE_TYPE)
