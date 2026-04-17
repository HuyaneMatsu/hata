import vampytest

from ..application_command_option_choice import ApplicationCommandOptionChoice

from ....localization import Locale

from .test__ApplicationCommandOptionChoice__constructor import _asert_fields_set


def test__ApplicationCommandOptionChoice__copy():
    """
    Tests whether ``ApplicationCommandOptionChoice.copy`` works as intended.
    """
    name = 'satori'
    name_localizations = {
        Locale.german: 'koishi',
    }
    value = 456
    
    application_command_option_choice = ApplicationCommandOptionChoice(
        name = name,
        name_localizations = name_localizations,
        value = value,
    )
    copy = application_command_option_choice.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_option_choice, copy)
    
    vampytest.assert_eq(application_command_option_choice, copy)


def test__ApplicationCommandOptionChoice__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionChoice.copy_with`` works as intended.
    
    Case: no parameters.
    """ 
    name = 'satori'
    name_localizations = {
        Locale.german: 'koishi',
    }
    value = 456
    
    application_command_option_choice = ApplicationCommandOptionChoice(
        name = name,
        name_localizations = name_localizations,
        value = value,
    )
    copy = application_command_option_choice.copy_with()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_option_choice, copy)
    
    vampytest.assert_eq(application_command_option_choice, copy)


def test__ApplicationCommandOptionChoice__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionChoice.copy_with`` works as intended.
    
    Case: All field given
    """
    old_name = 'satori'
    old_name_localizations = {
        Locale.german: 'koishi',
    }
    old_value = 456
    
    new_name = 'komeiji'
    new_name_localizations = {
        Locale.danish: 'hartmann',
    }
    new_value = 56.8
    
    application_command_option_choice = ApplicationCommandOptionChoice(
        name = old_name,
        name_localizations = old_name_localizations,
        value = old_value,
    )
    
    copy = application_command_option_choice.copy_with(
        name = new_name,
        name_localizations = new_name_localizations,
        value = new_value,
    )
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_option_choice, copy)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.name_localizations, new_name_localizations)
    vampytest.assert_eq(copy.value, new_value)


def test__ApplicationCommandOptionChoice__with_translation():
    """
    Tests whether ``ApplicationCommandOptionChoice.with_translation`` works as intended.
    
    Case: no parameters.
    """ 
    name = 'satori'
    name_localizations = {
        Locale.german: 'koishi',
    }
    value = 456
    
    translation_table = {
        Locale.danish: {
            'satori': 'komeiji',
        }
    }
    
    application_command_option_choice = ApplicationCommandOptionChoice(
        name = name,
        name_localizations = name_localizations,
        value = value,
    )
    
    copy = application_command_option_choice.with_translation(translation_table)
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_option_choice, copy)
    
    vampytest.assert_eq(copy.name, name)
    vampytest.assert_eq(copy.value, value)
    vampytest.assert_eq(
        copy.name_localizations,
        {
            Locale.german: 'koishi',
            Locale.danish: 'komeiji',
        }
    )
