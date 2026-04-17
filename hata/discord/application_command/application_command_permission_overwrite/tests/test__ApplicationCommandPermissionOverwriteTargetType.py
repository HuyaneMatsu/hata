import vampytest

from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


@vampytest.call_from(ApplicationCommandPermissionOverwriteTargetType.INSTANCES.values())
def test__ApplicationCommandPermissionOverwriteTargetType__instances(instance):
    """
    Tests whether ``ApplicationCommandPermissionOverwriteTargetType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationCommandPermissionOverwriteTargetType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationCommandPermissionOverwriteTargetType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationCommandPermissionOverwriteTargetType.VALUE_TYPE)
