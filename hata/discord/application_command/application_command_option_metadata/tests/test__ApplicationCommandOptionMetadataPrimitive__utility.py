import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..primitive import ApplicationCommandOptionMetadataPrimitive

from .test__ApplicationCommandOptionMetadataPrimitive__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataPrimitive__copy():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.copy`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
    )
    copy = option_metadata.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataPrimitive__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.copy_with`` works as intended.
    
    Case: no parameters.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
    )
    copy = option_metadata.copy_with()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataPrimitive__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.copy_with`` works as intended.
    
    Case: All field given
    """
    old_required = True
    old_autocomplete = True
    old_choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    new_required = False
    new_autocomplete = True
    new_choices = [ApplicationCommandOptionChoice('aya'), ApplicationCommandOptionChoice('ayaya')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = old_required,
        autocomplete = old_autocomplete,
        choices = old_choices,
    )
    
    copy = option_metadata.copy_with(
        required = new_required,
        autocomplete = new_autocomplete,
        choices = new_choices,
    )
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_eq(copy.autocomplete, new_autocomplete)
    vampytest.assert_eq(copy.choices, tuple(new_choices))


def test__ApplicationCommandOptionMetadataPrimitive__copy_with_keyword_parameters__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.copy_with_keyword_parameters`` works as intended.
    
    Case: no parameters.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
    )
    copy = option_metadata.copy_with_keyword_parameters({})
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataPrimitive__copy_with_keyword_parameters__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.copy_with_keyword_parameters`` works as intended.
    
    Case: All field given
    """
    old_required = True
    old_autocomplete = True
    old_choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    new_required = False
    new_autocomplete = True
    new_choices = [ApplicationCommandOptionChoice('aya'), ApplicationCommandOptionChoice('ayaya')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = old_required,
        autocomplete = old_autocomplete,
        choices = old_choices,
    )
    
    copy = option_metadata.copy_with_keyword_parameters({
        'required': new_required,
        'autocomplete': new_autocomplete,
        'choices': new_choices,
    })
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_eq(copy.autocomplete, new_autocomplete)
    vampytest.assert_eq(copy.choices, tuple(new_choices))
