import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..integer import ApplicationCommandOptionMetadataInteger

from .test__ApplicationCommandOptionMetadataInteger__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataInteger__from_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.from_data`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('19', 19), ApplicationCommandOptionChoice('18', 18)]
    max_value = 10
    min_value = 20
    
    data = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': [choice.to_data() for choice in choices],
        'max_value': max_value,
        'min_value': min_value,
    }
    
    option_metadata = ApplicationCommandOptionMetadataInteger.from_data(data)
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
    vampytest.assert_eq(option_metadata.max_value, max_value)
    vampytest.assert_eq(option_metadata.min_value, min_value)


def test__ApplicationCommandOptionMetadataInteger__to_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.to_data`` works as intended.
    
    Case: include defaults
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('19', 19), ApplicationCommandOptionChoice('18', 18)]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataInteger(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
        max_value = max_value,
        min_value = min_value,
    )
    
    expected_output = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': [choice.to_data(defaults = True) for choice in choices],
        'max_value': max_value,
        'min_value': min_value,
    }
    
    vampytest.assert_eq(
        option_metadata.to_data(
            defaults = True,
        ),
        expected_output
    )
