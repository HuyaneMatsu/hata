import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..primitive import ApplicationCommandOptionMetadataPrimitive

from .test__ApplicationCommandOptionMetadataPrimitive__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataPrimitive__from_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.from_data`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    data = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': [choice.to_data() for choice in choices],
    }
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive.from_data(data)
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))


def test__ApplicationCommandOptionMetadataPrimitive__to_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.to_data`` works as intended.
    
    Case: include defaults
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
    )
    
    expected_output = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': [choice.to_data(defaults = True) for choice in choices],
    }
    
    vampytest.assert_eq(
        option_metadata.to_data(
            defaults = True,
        ),
        expected_output
    )
