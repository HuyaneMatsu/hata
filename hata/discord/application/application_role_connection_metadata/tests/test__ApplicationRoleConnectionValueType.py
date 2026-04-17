from types import FunctionType

import vampytest

from ..preinstanced import ApplicationRoleConnectionValueType


def _assert_fields_set(application_role_connection_value_type):
    """
    Asserts whether every field are set of the given application role connection value type.
    
    Parameters
    ----------
    application_role_connection_value_type : ``ApplicationRoleConnectionValueType``
        The instance to test.
    """
    vampytest.assert_instance(application_role_connection_value_type, ApplicationRoleConnectionValueType)
    vampytest.assert_instance(application_role_connection_value_type.name, str)
    vampytest.assert_instance(application_role_connection_value_type.value, ApplicationRoleConnectionValueType.VALUE_TYPE)
    vampytest.assert_instance(application_role_connection_value_type.serializer, FunctionType)
    vampytest.assert_instance(application_role_connection_value_type.deserializer, FunctionType)


@vampytest.call_from(ApplicationRoleConnectionValueType.INSTANCES.values())
def test__ApplicationRoleConnectionValueType__instances(instance):
    """
    Tests whether ``ApplicationRoleConnectionValueType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationRoleConnectionValueType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ApplicationRoleConnectionValueType__new__min_fields():
    """
    Tests whether ``ApplicationRoleConnectionValueType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 6
    
    try:
        output = ApplicationRoleConnectionValueType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ApplicationRoleConnectionValueType.NAME_DEFAULT)
        vampytest.assert_is(output.serializer, ApplicationRoleConnectionValueType.SERIALIZER_DEFAULT)
        vampytest.assert_is(output.deserializer, ApplicationRoleConnectionValueType.DESERIALIZER_DEFAULT)
        vampytest.assert_is(ApplicationRoleConnectionValueType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ApplicationRoleConnectionValueType.INSTANCES[value]
        except KeyError:
            pass
