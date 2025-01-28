from types import FunctionType

import vampytest

from ..preinstanced import HangType


def _assert_fields_set(hang_type):
    """
    Asserts whether every field are set of the given hang type.
    
    Parameters
    ----------
    hang_type : ``HangType``
        The instance to test.
    """
    vampytest.assert_instance(hang_type, HangType)
    vampytest.assert_instance(hang_type.name, str)
    vampytest.assert_instance(hang_type.value, HangType.VALUE_TYPE)
    vampytest.assert_instance(hang_type.name_getter, FunctionType)


@vampytest.call_from(HangType.INSTANCES.values())
def test__HangType__instances(instance):
    """
    Tests whether ``HangType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``HangType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__HangType__new__min_fields():
    """
    Tests whether ``HangType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 'Crash-Loop-Backoff'
    
    try:
        output = HangType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, 'crash loop backoff')
        vampytest.assert_is(output.name_getter, HangType.NAME_GETTER_DEFAULT)
        vampytest.assert_is(HangType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del HangType.INSTANCES[value]
        except KeyError:
            pass
