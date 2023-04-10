import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..sub_command import ApplicationCommandOptionMetadataSubCommand


def test__ApplicationCommandOptionMetadataSubCommand__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.__repr__`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    default = True
    
    option_metadata = ApplicationCommandOptionMetadataSubCommand(
        options = options,
        default = default,
    )
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataSubCommand__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.__hash__`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    default = True
    
    option_metadata = ApplicationCommandOptionMetadataSubCommand(
        options = options,
        default = default,
    )
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataSubCommand__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.__eq__`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    default = True
    
    keyword_parameters = {
        'options': options,
        'default': default,
    }
    
    option_metadata = ApplicationCommandOptionMetadataSubCommand(**keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('options', None),
        ('default', False),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataSubCommand(
            **{**keyword_parameters, field_name: field_value}
        )
        vampytest.assert_ne(option_metadata, test_option_metadata)
