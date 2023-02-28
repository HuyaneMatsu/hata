import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..sub_command import ApplicationCommandOptionMetadataSubCommand

from .test__ApplicationCommandOptionMetadataSubCommand__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataSubCommand__from_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.from_data`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    default = True
    
    data = {
        'options': [option.to_data() for option in options],
        'default': default,
    }
    
    option_metadata = ApplicationCommandOptionMetadataSubCommand.from_data(data)
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.options, tuple(options))
    vampytest.assert_eq(option_metadata.default, default)


def test__ApplicationCommandOptionMetadataSubCommand__to_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.to_data`` works as intended.
    
    Case: include defaults
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    default = True
    
    option_metadata = ApplicationCommandOptionMetadataSubCommand({
        'options': options,
        'default': default,
    })
    
    expected_output = {
        'options': [option.to_data(defaults = True) for option in options],
        'default': default,
    }
    
    vampytest.assert_eq(
        option_metadata.to_data(
            defaults = True,
        ),
        expected_output
    )
