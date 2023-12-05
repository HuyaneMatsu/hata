from types import FunctionType

import vampytest

from ..preinstanced import ApplicationRoleConnectionValueType


@vampytest.call_from(ApplicationRoleConnectionValueType.INSTANCES.values())
def test__ApplicationRoleConnectionValueType__instances(instance):
    """
    Tests whether ``ApplicationRoleConnectionValueType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationRoleConnectionValueType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationRoleConnectionValueType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationRoleConnectionValueType.VALUE_TYPE)
    vampytest.assert_instance(instance.serializer, FunctionType)
    vampytest.assert_instance(instance.deserializer, FunctionType)
