import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..numeric import ApplicationCommandOptionMetadataNumeric


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataNumeric``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataNumeric)
    
    vampytest.assert_instance(option_metadata.required, bool)
    vampytest.assert_instance(option_metadata.autocomplete, bool)
    vampytest.assert_instance(option_metadata.choices, tuple, nullable = True)
    vampytest.assert_instance(option_metadata.max_value, object, nullable = True)
    vampytest.assert_instance(option_metadata.min_value, object, nullable = True)


def test__ApplicationCommandOptionMetadataNumeric__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataNumeric.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataNumeric({})
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataNumeric__new__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataNumeric.__new__`` works as intended.
    
    Case: All fields given.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataNumeric({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
    vampytest.assert_eq(option_metadata.max_value, max_value)
    vampytest.assert_eq(option_metadata.min_value, min_value)
