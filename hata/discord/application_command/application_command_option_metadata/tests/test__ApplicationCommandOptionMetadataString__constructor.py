import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..string import ApplicationCommandOptionMetadataString


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataString``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataString)
    
    vampytest.assert_instance(option_metadata.required, bool)
    vampytest.assert_instance(option_metadata.autocomplete, bool)
    vampytest.assert_instance(option_metadata.choices, tuple, nullable = True)
    vampytest.assert_instance(option_metadata.max_length, int)
    vampytest.assert_instance(option_metadata.min_length, int)


def test__ApplicationCommandOptionMetadataString__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataString()
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataString__new__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.__new__`` works as intended.
    
    Case: All fields given.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_length = 10
    min_length = 20
    
    option_metadata = ApplicationCommandOptionMetadataString(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
        max_length = max_length,
        min_length = min_length,
    )
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
    vampytest.assert_eq(option_metadata.max_length, max_length)
    vampytest.assert_eq(option_metadata.min_length, min_length)


def test__ApplicationCommandOptionMetadataString__from_keyword_parameters__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataString.from_keyword_parameters({})
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataString__from_keyword_parameters__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_length = 10
    min_length = 20
    
    option_metadata = ApplicationCommandOptionMetadataString.from_keyword_parameters({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_length': max_length,
        'min_length': min_length,
    })
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
    vampytest.assert_eq(option_metadata.max_length, max_length)
    vampytest.assert_eq(option_metadata.min_length, min_length)
