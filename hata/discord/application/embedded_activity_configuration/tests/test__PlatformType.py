import vampytest

from ..preinstanced import PlatformType


@vampytest.call_from(PlatformType.INSTANCES.values())
def test__PlatformType__instances(instance):
    """
    Tests whether ``PlatformType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``PlatformType``
        The instance to test.
    """
    vampytest.assert_instance(instance, PlatformType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, PlatformType.VALUE_TYPE)
