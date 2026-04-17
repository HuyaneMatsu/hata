import vampytest

from ..preinstanced import ApplicationExplicitContentFilterLevel


@vampytest.call_from(ApplicationExplicitContentFilterLevel.INSTANCES.values())
def test__ApplicationExplicitContentFilterLevel__instances(instance):
    """
    Tests whether ``ApplicationExplicitContentFilterLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationExplicitContentFilterLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationExplicitContentFilterLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationExplicitContentFilterLevel.VALUE_TYPE)
