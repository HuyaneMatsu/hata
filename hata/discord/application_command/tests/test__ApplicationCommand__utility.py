import vampytest

from ...localization import Locale
from ...permission import Permission

from ..application_command import ApplicationCommand
from ..application_command_option import ApplicationCommandOption
from ..preinstanced import ApplicationCommandOptionType, ApplicationCommandTargetType


def test__ApplicationCommand__copy():
    """
    Tests whether ``ApplicationCommand.copy`` works as intended.
    """
    name = 'owo'
    description = 'description'
    allow_in_dm = True
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    nsfw = True
    options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    required_permissions = Permission().update_by_keys(administrator=True)
    target_type = ApplicationCommandTargetType.chat
    
    application_command = ApplicationCommand(
        name,
        description,
        allow_in_dm = allow_in_dm,
        description_localizations = description_localizations,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    copy = application_command.copy()
    
    vampytest.assert_eq(application_command.name, copy.name)
    vampytest.assert_eq(application_command.description, copy.description)
    vampytest.assert_eq(application_command.allow_in_dm, copy.allow_in_dm)
    vampytest.assert_eq(application_command.description_localizations, copy.description_localizations)
    vampytest.assert_eq(application_command.name_localizations, copy.name_localizations)
    vampytest.assert_eq(application_command.nsfw, copy.nsfw)
    vampytest.assert_eq(application_command.options, copy.options)
    vampytest.assert_eq(application_command.required_permissions, copy.required_permissions)
    vampytest.assert_eq(application_command.target_type, copy.target_type)

    # Also test the extra fields whether they are set.
    vampytest.assert_instance(application_command.id, int)
    vampytest.assert_instance(application_command.application_id, int)
    vampytest.assert_instance(application_command.guild_id, int)
    vampytest.assert_instance(application_command.version, int)
