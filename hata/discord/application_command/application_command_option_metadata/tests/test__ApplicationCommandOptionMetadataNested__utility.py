import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..nested import ApplicationCommandOptionMetadataNested

from .test__ApplicationCommandOptionMetadataNested__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataNested__copy():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.copy`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    option_metadata = ApplicationCommandOptionMetadataNested({
        'options': options,
    })
    copy = option_metadata.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataNested__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.copy_with`` works as intended.
    
    Case: no parameters.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    option_metadata = ApplicationCommandOptionMetadataNested({
        'options': options,
    })
    copy = option_metadata.copy_with({})
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataNested__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.copy_with`` works as intended.
    
    Case: All field given
    """
    old_options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    new_options = [
        ApplicationCommandOption('aya', 'ayaya', ApplicationCommandOptionType.float),
        ApplicationCommandOption('momiji', 'awoo', ApplicationCommandOptionType.user),
    ]
    
    option_metadata = ApplicationCommandOptionMetadataNested({
        'options': old_options,
    })
    
    copy = option_metadata.copy_with({
        'options': new_options,
    })
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.options, tuple(new_options))
