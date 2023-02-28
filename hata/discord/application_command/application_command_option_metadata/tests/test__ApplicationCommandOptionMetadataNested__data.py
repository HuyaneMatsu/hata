import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..nested import ApplicationCommandOptionMetadataNested

from .test__ApplicationCommandOptionMetadataNested__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataNested__from_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.from_data`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    data = {
        'options': [option.to_data() for option in options],
    }
    
    option_metadata = ApplicationCommandOptionMetadataNested.from_data(data)
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.options, tuple(options))


def test__ApplicationCommandOptionMetadataNested__to_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.to_data`` works as intended.
    
    Case: include defaults
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    option_metadata = ApplicationCommandOptionMetadataNested({
        'options': options,
    })
    
    expected_output = {
        'options': [option.to_data(defaults = True) for option in options],
    }
    
    vampytest.assert_eq(
        option_metadata.to_data(
            defaults = True,
        ),
        expected_output
    )
