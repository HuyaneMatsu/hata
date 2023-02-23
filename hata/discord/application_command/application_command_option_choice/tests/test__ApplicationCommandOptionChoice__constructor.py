from enum import Enum

import vampytest

from ....localization import Locale

from ..application_command_option_choice import ApplicationCommandOptionChoice


class TestEnum(Enum):
    ayaya = 'owo'


def _asert_fields_set(application_command_option_choice):
    """
    Checks whether all attributes of the application command option choice.
    
    Parameters
    ----------
    application_command_option_choice : ``ApplicationCommandOptionChoice``
        The application command choice to check.
    """
    vampytest.assert_instance(application_command_option_choice, ApplicationCommandOptionChoice)
    
    vampytest.assert_instance(application_command_option_choice.name, str)
    vampytest.assert_instance(application_command_option_choice.name_localizations, dict, nullable = True)
    vampytest.assert_instance(application_command_option_choice.value, object)


def test__ApplicationCommandOptionChoice__new__0():
    """
    Tests whether ``ApplicationCommandOptionChoice.__new__`` works as intended.
    
    Case: All parameters given.
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
    _asert_fields_set(application_command_option_choice)
    
    vampytest.assert_eq(application_command_option_choice.name, name)
    vampytest.assert_eq(application_command_option_choice.name_localizations, name_localizations)
    vampytest.assert_eq(application_command_option_choice.value, value)


def test__ApplicationCommandOptionChoice__new__1():
    """
    Tests whether ``ApplicationCommandOptionChoice.__new__`` works as intended.
    
    Case: using enum and defaulting.
    """
    application_command_option_choice = ApplicationCommandOptionChoice(
        TestEnum.ayaya,
    )
    _asert_fields_set(application_command_option_choice)
    
    vampytest.assert_eq(application_command_option_choice.name, 'ayaya')
    vampytest.assert_eq(application_command_option_choice.value, 'owo')
