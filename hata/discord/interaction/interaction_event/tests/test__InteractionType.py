import vampytest

from ...interaction_metadata import InteractionMetadataBase

from ..preinstanced import InteractionType


def _assert_fields_set(interaction_type):
    """
    Asserts whether every field are set of the given interaction type.
    
    Parameters
    ----------
    interaction_type : ``InteractionType``
        The instance to test.
    """
    vampytest.assert_instance(interaction_type, InteractionType)
    vampytest.assert_instance(interaction_type.name, str)
    vampytest.assert_instance(interaction_type.value, InteractionType.VALUE_TYPE)
    vampytest.assert_subtype(interaction_type.metadata_type, InteractionMetadataBase)


@vampytest.call_from(InteractionType.INSTANCES.values())
def test__InteractionType__instances(instance):
    """
    Tests whether ``InteractionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``InteractionType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__InteractionType__new__min_fields():
    """
    Tests whether ``InteractionType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = InteractionType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, InteractionType.NAME_DEFAULT)
        vampytest.assert_is(output.metadata_type, InteractionMetadataBase)
        vampytest.assert_is(InteractionType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del InteractionType.INSTANCES[value]
        except KeyError:
            pass
