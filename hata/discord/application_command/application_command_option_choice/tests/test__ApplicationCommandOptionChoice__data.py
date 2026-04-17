import vampytest

from ....localization import Locale

from ..application_command_option_choice import ApplicationCommandOptionChoice

from .test__ApplicationCommandOptionChoice__constructor import _asert_fields_set


def test__ApplicationCommandOptionChoice__from_data():
    """
    Tests whether ``ApplicationCommandOptionChoice.from_data`` works as intended.
    """
    name = 'satori'
    name_localizations = {
        Locale.german: 'koishi',
    }
    value = 456
    
    data = {
        'name': name,
        'name_localizations': {key.value: value for key, value in name_localizations.items()},
        'value': value,
    }
    
    application_command_option_choice = ApplicationCommandOptionChoice.from_data(data)
    _asert_fields_set(application_command_option_choice)
    
    vampytest.assert_eq(application_command_option_choice.name, name)
    vampytest.assert_eq(application_command_option_choice.name_localizations, name_localizations)
    vampytest.assert_eq(application_command_option_choice.value, value)


def test__ApplicationCommandOptionChoice__to_data():
    """
    Tests whether ``ApplicationCommandOptionChoice.to_data`` works as intended.
    
    Case: include defaults
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
  
    vampytest.assert_eq(
        application_command_option_choice.to_data(
            defaults = True,
        ),
        {
            'name': name,
            'name_localizations': {key.value: value for key, value in name_localizations.items()},
            'value': value,
        },
    )
