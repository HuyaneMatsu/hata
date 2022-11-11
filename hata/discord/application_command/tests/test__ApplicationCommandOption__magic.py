import vampytest

from ...localization import Locale

from .. import ApplicationCommandOption, ApplicationCommandOptionChoice, ApplicationCommandOptionType


def test__ApplicationCommandOption__repr__0():
    """
    Tests whether ``ApplicationCommandOption``'s `__repr__` method works correctly.
    This test tests string sub-fields.
    """
    application_command_option = ApplicationCommandOption(
        'owo',
        'owo',
        ApplicationCommandOptionType.string,
        min_length = 30,
        max_length = 60,
    )
    vampytest.assert_instance(repr(application_command_option), str)


def test__ApplicationCommandOption__eq():
    """
    Tests whether ``ApplicationCommandOption``'s `__eq__` method works correctly.
    This test tests string sub-fields.
    """
    vampytest.assert_eq(
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
    )
    
    vampytest.assert_not_eq(
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=59),
    )

    vampytest.assert_not_eq(
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string),
    )



def test__ApplicationCommandOption__len__0():
    """
    Tests whether ``ApplicationCommandOption.__len__`` only counts the longest description's length and not all's
    together.
    
    Case: The longest is a localization.
    """
    name = 'owo'
    
    description_1 = 'hi'
    description_2 = 'hoi'
    description_3 = 'halo'
    
    application_command_option = ApplicationCommandOption(
        name,
        description_1,
        ApplicationCommandOptionType.string,
        description_localizations = {
            Locale.thai: description_2,
            Locale.czech: description_3,
        }
    )
    
    expected_length = len(name) + max(
        len(description) for description in (description_1, description_2, description_3)
    )
    
    vampytest.assert_eq(len(application_command_option), expected_length,)


def test__ApplicationCommandOption__len__1():
    """
    Tests whether ``ApplicationCommandOption.__len__`` only counts the longest description's length and not all's
    together.
    
    Case: The longest is the description itself.
    """
    name = 'owo'
    
    description_1 = 'hi'
    description_2 = 'hoi'
    description_3 = 'halo'
    
    application_command_option = ApplicationCommandOption(
        name,
        description_3,
        ApplicationCommandOptionType.string,
        description_localizations = {
            Locale.thai: description_1,
            Locale.czech: description_2,
        }
    )
    
    expected_length = len(name) + max(
        len(description) for description in (description_1, description_2, description_3)
    )
    
    vampytest.assert_eq(len(application_command_option), expected_length)


def test__ApplicationCommandOption__len__2():
    """
    Tests whether ``ApplicationCommandOption.__len__`` only counts the longest name's length and not all's together.
    
    Case: The longest is a localization.
    """
    name_1 = 'hi'
    name_2 = 'hoi'
    name_3 = 'halo'
    
    description = 'owo'
    
    application_command_option = ApplicationCommandOption(
        name_1,
        description,
        ApplicationCommandOptionType.string,
        name_localizations = {
            Locale.thai: name_2,
            Locale.czech: name_3,
        },
    )
    
    expected_length = len(description) + max(
        len(name) for name in (name_1, name_2, name_3)
    )
    
    vampytest.assert_eq(len(application_command_option), expected_length)


def test__ApplicationCommandOption__len__3():
    """
    Tests whether ``ApplicationCommandOption.__len__`` only counts the longest name's length and not all's together.
    
    Case: The longest is the name itself.
    """
    name_1 = 'hi'
    name_2 = 'hoi'
    name_3 = 'halo'
    
    description = 'owo'
    
    application_command_option = ApplicationCommandOption(
        name_3,
        description,
        ApplicationCommandOptionType.string,
        name_localizations = {
            Locale.thai: name_1,
            Locale.czech: name_2,
        },
    )
    
    expected_length = len(description) + max(
        len(name) for name in (name_1, name_2, name_3)
    )
    
    vampytest.assert_eq(len(application_command_option), expected_length)


def test__ApplicationCommandOption__hash__0():
    """
    Tests whether ``ApplicationCommandOption.__hash__`` works as intended.
    """
    application_command_option = ApplicationCommandOption(
        'vanilla',
        'chocola',
        ApplicationCommandOptionType.string,
        choices = [
            ApplicationCommandOptionChoice(
                'exploring',
                'is-fun',
                name_localizations = {
                    Locale.thai: 'stay-safe',
                }
            )
        ],
        default = True,
        description_localizations = {
            Locale.thai: 'choco',
        },
        name_localizations = {
            Locale.thai: 'vani',
        },
        required = True
    )
    
    vampytest.assert_instance(hash(application_command_option), int)
