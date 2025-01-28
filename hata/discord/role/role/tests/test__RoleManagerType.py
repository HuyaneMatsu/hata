import vampytest

from ...role_manager_metadata import RoleManagerMetadataBase

from ..preinstanced import RoleManagerType

def _assert_fields_set(role_manager_type):
    """
    Asserts whether every field are set of the given role manager type.
    
    Parameters
    ----------
    role_manager_type : ``RoleManagerType``
        The instance to test.
    """
    vampytest.assert_instance(role_manager_type, RoleManagerType)
    vampytest.assert_instance(role_manager_type.name, str)
    vampytest.assert_instance(role_manager_type.value, RoleManagerType.VALUE_TYPE)
    vampytest.assert_subtype(role_manager_type.metadata_type, RoleManagerMetadataBase)


@vampytest.call_from(RoleManagerType.INSTANCES.values())
def test__RoleManagerType__instances(instance):
    """
    Tests whether ``RoleManagerType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``RoleManagerType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__RoleManagerType__new__min_fields():
    """
    Tests whether ``RoleManagerType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 30
    
    try:
        output = RoleManagerType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, RoleManagerType.NAME_DEFAULT)
        vampytest.assert_is(output.metadata_type, RoleManagerMetadataBase)
        vampytest.assert_is(RoleManagerType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del RoleManagerType.INSTANCES[value]
        except KeyError:
            pass


def _iter_options__bool():
    yield RoleManagerType.none, False
    yield RoleManagerType.unset, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__RoleManagerType__bool(instance):
    """
    Tests whether ``RoleManagerType.__bool__`` instances work as intended.
    
    Parameters
    ----------
    instance : ``RoleManagerType``
        The instance to test.
    
    Returns
    -------
    output : `bool`
    """
    output = bool(instance)
    vampytest.assert_instance(output, bool)
    return output
