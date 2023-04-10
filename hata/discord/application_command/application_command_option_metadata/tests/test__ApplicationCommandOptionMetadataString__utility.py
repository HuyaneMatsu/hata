import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..string import ApplicationCommandOptionMetadataString

from .test__ApplicationCommandOptionMetadataString__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataString__copy():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.copy`` works as intended.
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
    copy = option_metadata.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataString__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.copy_with`` works as intended.
    
    Case: no parameters.
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
    copy = option_metadata.copy_with()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataString__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.copy_with`` works as intended.
    
    Case: All field given
    """
    old_required = True
    old_autocomplete = True
    old_choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    old_max_length = 10
    old_min_length = 20
    
    new_required = False
    new_autocomplete = True
    new_choices = [ApplicationCommandOptionChoice('aya'), ApplicationCommandOptionChoice('ayaya')]
    new_max_length = 11
    new_min_length = 12
    
    option_metadata = ApplicationCommandOptionMetadataString(
        required = old_required,
        autocomplete = old_autocomplete,
        choices = old_choices,
        max_length = old_max_length,
        min_length = old_min_length,
    )
    
    copy = option_metadata.copy_with(
        required = new_required,
        autocomplete = new_autocomplete,
        choices = new_choices,
        max_length = new_max_length,
        min_length = new_min_length,
    )
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_eq(copy.autocomplete, new_autocomplete)
    vampytest.assert_eq(copy.choices, tuple(new_choices))
    vampytest.assert_eq(copy.max_length, new_max_length)
    vampytest.assert_eq(copy.min_length, new_min_length)


def test__ApplicationCommandOptionMetadataString__copy_with_keyword_parameters__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.copy_with_keyword_parameters`` works as intended.
    
    Case: no parameters.
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
    copy = option_metadata.copy_with_keyword_parameters({})
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataString__copy_with_keyword_parameters__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.copy_with_keyword_parameters`` works as intended.
    
    Case: All field given
    """
    old_required = True
    old_autocomplete = True
    old_choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    old_max_length = 10
    old_min_length = 20
    
    new_required = False
    new_autocomplete = True
    new_choices = [ApplicationCommandOptionChoice('aya'), ApplicationCommandOptionChoice('ayaya')]
    new_max_length = 11
    new_min_length = 12
    
    option_metadata = ApplicationCommandOptionMetadataString(
        required = old_required,
        autocomplete = old_autocomplete,
        choices = old_choices,
        max_length = old_max_length,
        min_length = old_min_length,
    )
    
    copy = option_metadata.copy_with_keyword_parameters({
        'required': new_required,
        'autocomplete': new_autocomplete,
        'choices': new_choices,
        'max_length': new_max_length,
        'min_length': new_min_length,
    })
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_eq(copy.autocomplete, new_autocomplete)
    vampytest.assert_eq(copy.choices, tuple(new_choices))
    vampytest.assert_eq(copy.max_length, new_max_length)
    vampytest.assert_eq(copy.min_length, new_min_length)
