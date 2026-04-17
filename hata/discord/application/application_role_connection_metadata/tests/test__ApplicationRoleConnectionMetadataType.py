import vampytest

from ..preinstanced import ApplicationRoleConnectionMetadataType, ApplicationRoleConnectionValueType

def _assert_fields_set(application_role_connection_metadata_type):
    """
    Asserts whether every field are set of the given application role connection metadata type.
    
    Parameters
    ----------
    application_role_connection_metadata_type : ``ApplicationRoleConnectionMetadataType``
        The instance to test.
    """
    vampytest.assert_instance(application_role_connection_metadata_type, ApplicationRoleConnectionMetadataType)
    vampytest.assert_instance(application_role_connection_metadata_type.name, str)
    vampytest.assert_instance(
        application_role_connection_metadata_type.value, ApplicationRoleConnectionMetadataType.VALUE_TYPE
    )
    vampytest.assert_instance(application_role_connection_metadata_type.value_type, ApplicationRoleConnectionValueType)


@vampytest.call_from(ApplicationRoleConnectionMetadataType.INSTANCES.values())
def test__ApplicationRoleConnectionMetadataType__instances(instance):
    """
    Tests whether ``ApplicationRoleConnectionMetadataType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationRoleConnectionMetadataType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ApplicationRoleConnectionMetadataType__new__min_fields():
    """
    Tests whether ``ApplicationRoleConnectionMetadataType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = ApplicationRoleConnectionMetadataType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ApplicationRoleConnectionMetadataType.NAME_DEFAULT)
        vampytest.assert_is(output.value_type, ApplicationRoleConnectionValueType.none)
        vampytest.assert_is(ApplicationRoleConnectionMetadataType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ApplicationRoleConnectionMetadataType.INSTANCES[value]
        except KeyError:
            pass
