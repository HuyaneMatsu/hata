import vampytest

from ..preinstanced import Locale


def _assert_fields_set(locale):
    """
    Asserts whether every field are set of the given locale.
    
    Parameters
    ----------
    locale : ``Locale``
        The instance to test.
    """
    vampytest.assert_instance(locale, Locale)
    vampytest.assert_instance(locale.name, str)
    vampytest.assert_instance(locale.value, Locale.VALUE_TYPE)
    vampytest.assert_instance(locale.native_name, str)


@vampytest.call_from(Locale.INSTANCES.values())
def test__Locale__instances(instance):
    """
    Tests whether ``Locale`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``Locale``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__Locale__new__min_fields():
    """
    Tests whether ``Locale.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 'oven'
    
    try:
        output = Locale(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, value)
        vampytest.assert_eq(output.native_name, value)
        vampytest.assert_is(Locale.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del Locale.INSTANCES[value]
        except KeyError:
            pass
