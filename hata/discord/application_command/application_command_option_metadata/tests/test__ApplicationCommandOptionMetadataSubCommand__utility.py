import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..sub_command import ApplicationCommandOptionMetadataSubCommand

from .test__ApplicationCommandOptionMetadataSubCommand__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataSubCommand__copy():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.copy`` works as intended.
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
    copy = option_metadata.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataSubCommand__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.copy_with`` works as intended.
    
    Case: no parameters.
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
    copy = option_metadata.copy_with({})
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataSubCommand__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataSubCommand.copy_with`` works as intended.
    
    Case: All field given
    """
    old_options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    old_default = True
    
    new_options = [
        ApplicationCommandOption('aya', 'ayaya', ApplicationCommandOptionType.float),
        ApplicationCommandOption('momiji', 'awoo', ApplicationCommandOptionType.user),
    ]
    new_default = False
    
    option_metadata = ApplicationCommandOptionMetadataSubCommand({
        'options': old_options,
        'default': old_default,
    })
    
    copy = option_metadata.copy_with({
        'options': new_options,
        'default': new_default,
    })
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.default, new_default)
