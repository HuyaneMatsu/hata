import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..integer import ApplicationCommandOptionMetadataInteger

from .test__ApplicationCommandOptionMetadataInteger__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataInteger__copy():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.copy`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataInteger({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    copy = option_metadata.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataInteger__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.copy_with`` works as intended.
    
    Case: no parameters.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataInteger({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    copy = option_metadata.copy_with({})
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataInteger__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.copy_with`` works as intended.
    
    Case: All field given
    """
    old_required = True
    old_autocomplete = True
    old_choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    old_max_value = 10
    old_min_value = 20
    
    new_required = False
    new_autocomplete = True
    new_choices = [ApplicationCommandOptionChoice("31", 31), ApplicationCommandOptionChoice("32", 32)]
    new_max_value = 11
    new_min_value = 12
    
    option_metadata = ApplicationCommandOptionMetadataInteger({
        'required': old_required,
        'autocomplete': old_autocomplete,
        'choices': old_choices,
        'max_value': old_max_value,
        'min_value': old_min_value,
    })
    
    copy = option_metadata.copy_with({
        'required': new_required,
        'autocomplete': new_autocomplete,
        'choices': new_choices,
        'max_value': new_max_value,
        'min_value': new_min_value,
    })
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_eq(copy.autocomplete, new_autocomplete)
    vampytest.assert_eq(copy.choices, tuple(new_choices))
    vampytest.assert_eq(copy.max_value, new_max_value)
    vampytest.assert_eq(copy.min_value, new_min_value)
