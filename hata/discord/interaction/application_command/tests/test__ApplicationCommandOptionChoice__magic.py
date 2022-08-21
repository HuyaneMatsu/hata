import vampytest

from ....localizations import Locale

from .. import ApplicationCommandOptionChoice


def test__ApplicationCommandOptionChoice__len_0():
    """
    Tests whether ``ApplicationCommandOptionChoice.__len__`` only counts the longest name's length and not all's together.
    
    Case: The longest is a localization.
    """
    name_1 = 'hi'
    name_2 = 'hoi'
    name_3 = 'halo'
    
    application_command = ApplicationCommandOptionChoice(
        name_1,
        12.6,
        name_localizations = {
            Locale.thai: name_2,
            Locale.czech: name_3,
        },
    )
    
    expected_length = max(
        len(name) for name in (name_1, name_2, name_3)
    )
    
    vampytest.assert_eq(len(application_command), expected_length,)


def test__ApplicationCommandOptionChoice__len_1():
    """
    Tests whether ``ApplicationCommandOptionChoice.__len__`` only counts the longest name's length and not all's together.
    
    Case: The longest is the name itself.
    """
    name_1 = 'hi'
    name_2 = 'hoi'
    name_3 = 'halo'
    
    application_command = ApplicationCommandOptionChoice(
        name_3,
        12.6,
        name_localizations = {
            Locale.thai: name_1,
            Locale.czech: name_2,
        },
    )
    
    expected_length = max(
        len(name) for name in (name_1, name_2, name_3)
    )
    
    vampytest.assert_eq(len(application_command), expected_length,)
