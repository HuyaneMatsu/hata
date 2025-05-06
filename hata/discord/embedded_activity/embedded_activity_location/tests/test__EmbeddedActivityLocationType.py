import vampytest

from ..preinstanced import EmbeddedActivityLocationType


def _assert_fields_set(embedded_activity_location_type):
    """
    Asserts whether every field are set of the given embedded activity location type.
    
    Parameters
    ----------
    embedded_activity_location_type : ``EmbeddedActivityLocationType``
        The instance to test.
    """
    vampytest.assert_instance(embedded_activity_location_type, EmbeddedActivityLocationType)
    vampytest.assert_instance(embedded_activity_location_type.name, str)
    vampytest.assert_instance(embedded_activity_location_type.value, EmbeddedActivityLocationType.VALUE_TYPE)


@vampytest.call_from(EmbeddedActivityLocationType.INSTANCES.values())
def test__EmbeddedActivityLocationType__instances(instance):
    """
    Tests whether ``EmbeddedActivityLocationType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``EmbeddedActivityLocationType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__EmbeddedActivityLocationType__new__min_fields():
    """
    Tests whether ``EmbeddedActivityLocationType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    # :clueless:
    value = 'nyanner-nest'
    
    try:
        output = EmbeddedActivityLocationType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, 'nyanner nest')
        vampytest.assert_is(EmbeddedActivityLocationType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del EmbeddedActivityLocationType.INSTANCES[value]
        except KeyError:
            pass
