import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..string import ApplicationCommandOptionMetadataString

from .test__ApplicationCommandOptionMetadataString__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataString__from_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.from_data`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_length = 10
    min_length = 20
    
    data = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': [choice.to_data() for choice in choices],
        'max_length': max_length,
        'min_length': min_length,
    }
    
    option_metadata = ApplicationCommandOptionMetadataString.from_data(data)
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
    vampytest.assert_eq(option_metadata.max_length, max_length)
    vampytest.assert_eq(option_metadata.min_length, min_length)


def test__ApplicationCommandOptionMetadataString__to_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.to_data`` works as intended.
    
    Case: include defaults
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_length = 10
    min_length = 20
    
    option_metadata = ApplicationCommandOptionMetadataString({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_length': max_length,
        'min_length': min_length,
    })
    
    expected_output = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': [choice.to_data(defaults = True) for choice in choices],
        'max_length': max_length,
        'min_length': min_length,
    }
    
    vampytest.assert_eq(
        option_metadata.to_data(
            defaults = True,
        ),
        expected_output
    )
