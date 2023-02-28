import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..sub_command import ApplicationCommandOptionMetadataSubCommand


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataSubCommand``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataSubCommand)
    
    vampytest.assert_instance(option_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(option_metadata.default, bool)


def test__ApplicationCommandOptionMetadataSubCommand__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataSubCommand({})
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataSubCommand__new__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.__new__`` works as intended.
    
    Case: All fields given.
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
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.options, tuple(options))
