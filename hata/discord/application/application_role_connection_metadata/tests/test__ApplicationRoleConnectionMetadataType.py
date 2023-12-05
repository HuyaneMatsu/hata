import vampytest

from ..preinstanced import ApplicationRoleConnectionMetadataType, ApplicationRoleConnectionValueType


@vampytest.call_from(ApplicationRoleConnectionMetadataType.INSTANCES.values())
def test__ApplicationRoleConnectionMetadataType__instances(instance):
    """
    Tests whether ``ApplicationRoleConnectionMetadataType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationRoleConnectionMetadataType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationRoleConnectionMetadataType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationRoleConnectionMetadataType.VALUE_TYPE)
    vampytest.assert_instance(instance.value_type, ApplicationRoleConnectionValueType)
