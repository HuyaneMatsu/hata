import vampytest

from ..preinstanced import ApplicationCommandOptionType

from ...application_command_option_metadata import ApplicationCommandOptionMetadataBase


def _assert_fields_set(application_command_option_type):
    """
    Asserts whether every field are set of the given application command option type.
    
    Parameters
    ----------
    application_command_option_type : ``ApplicationCommandOptionType``
        The instance to test.
    """
    vampytest.assert_instance(application_command_option_type, ApplicationCommandOptionType)
    vampytest.assert_instance(application_command_option_type.name, str)
    vampytest.assert_instance(application_command_option_type.value, ApplicationCommandOptionType.VALUE_TYPE)
    vampytest.assert_subtype(application_command_option_type.metadata_type, ApplicationCommandOptionMetadataBase)


@vampytest.call_from(ApplicationCommandOptionType.INSTANCES.values())
def test__ApplicationCommandOptionType__instances(instance):
    """
    Tests whether ``ApplicationCommandOptionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationCommandOptionType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ApplicationCommandOptionType__new__min_fields():
    """
    Tests whether ``ApplicationCommandOptionType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = ApplicationCommandOptionType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ApplicationCommandOptionType.NAME_DEFAULT)
        vampytest.assert_is(output.metadata_type, ApplicationCommandOptionMetadataBase)
        vampytest.assert_is(ApplicationCommandOptionType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ApplicationCommandOptionType.INSTANCES[value]
        except KeyError:
            pass
