import vampytest

from ...role_manager_metadata import RoleManagerMetadataBase

from ..preinstanced import RoleManagerType


@vampytest.call_from(RoleManagerType.INSTANCES.values())
def test__RoleManagerType__instances(instance):
    """
    Tests whether ``RoleManagerType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``RoleManagerType``
        The instance to test.
    """
    vampytest.assert_instance(instance, RoleManagerType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, RoleManagerType.VALUE_TYPE)
    vampytest.assert_subtype(instance.metadata_type, RoleManagerMetadataBase)
