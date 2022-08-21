import vampytest

from ....localizations import Locale

from .. import ApplicationCommand, ApplicationCommandTargetType


def test__ApplicationCommand__len_0():
    """
    Tests whether ``ApplicationCommand.__len__`` will not raise `TypeError` if `.description` is `None`.
    """
    application_command = ApplicationCommand('owo', None)
    
    return len(application_command)


def test__ApplicationCommand__len_1():
    """
    Tests whether ``ApplicationCommand.__len__`` only counts the longest description's length and not all's together.
    
    Case: The longest is a localization.
    """
    name = 'owo'
    
    description_1 = 'hi'
    description_2 = 'hoi'
    description_3 = 'halo'
    
    application_command = ApplicationCommand(
        name,
        description_1,
        description_localizations = {
            Locale.thai: description_2,
            Locale.czech: description_3,
        }
    )
    
    expected_length = len(name) + max(
        len(description) for description in (description_1, description_2, description_3)
    )
    
    vampytest.assert_eq(len(application_command), expected_length,)


def test__ApplicationCommand__len_2():
    """
    Tests whether ``ApplicationCommand.__len__`` only counts the longest description's length and not all's together.
    
    Case: The longest is the description itself.
    """
    name = 'owo'
    
    description_1 = 'hi'
    description_2 = 'hoi'
    description_3 = 'halo'
    
    application_command = ApplicationCommand(
        name,
        description_3,
        description_localizations = {
            Locale.thai: description_1,
            Locale.czech: description_2,
        }
    )
    
    expected_length = len(name) + max(
        len(description) for description in (description_1, description_2, description_3)
    )
    
    vampytest.assert_eq(len(application_command), expected_length,)


def test__ApplicationCommand__len_3():
    """
    Tests whether ``ApplicationCommand.__len__`` only counts the longest name's length and not all's together.
    
    Case: The longest is a localization.
    """
    name_1 = 'hi'
    name_2 = 'hoi'
    name_3 = 'halo'
    
    application_command = ApplicationCommand(
        name_1,
        None,
        name_localizations = {
            Locale.thai: name_2,
            Locale.czech: name_3,
        },
        target_type = ApplicationCommandTargetType.user,
    )
    
    expected_length = max(
        len(name) for name in (name_1, name_2, name_3)
    )
    
    vampytest.assert_eq(len(application_command), expected_length,)


def test__ApplicationCommand__len_4():
    """
    Tests whether ``ApplicationCommand.__len__`` only counts the longest name's length and not all's together.
    
    Case: The longest is the name itself.
    """
    name_1 = 'hi'
    name_2 = 'hoi'
    name_3 = 'halo'
    
    application_command = ApplicationCommand(
        name_3,
        None,
        name_localizations = {
            Locale.thai: name_1,
            Locale.czech: name_2,
        },
        target_type = ApplicationCommandTargetType.user,
    )
    
    expected_length = max(
        len(name) for name in (name_1, name_2, name_3)
    )
    
    vampytest.assert_eq(len(application_command), expected_length,)
