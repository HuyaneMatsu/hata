import vampytest

from ..preinstanced import ExplicitContentFilterLevel


@vampytest.call_from(ExplicitContentFilterLevel.INSTANCES.values())
def test__ExplicitContentFilterLevel__instances(instance):
    """
    Tests whether ``ExplicitContentFilterLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ExplicitContentFilterLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, ExplicitContentFilterLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ExplicitContentFilterLevel.VALUE_TYPE)
