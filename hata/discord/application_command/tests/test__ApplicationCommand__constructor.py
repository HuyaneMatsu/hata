import vampytest

from ...localization import Locale
from ...permission import Permission

from ..application_command import ApplicationCommand
from ..application_command_option import ApplicationCommandOption
from ..preinstanced import ApplicationCommandOptionType, ApplicationCommandTargetType


def test__ApplicationCommand__new__0():
    """
    Tests whether ``ApplicationCommand.__new__`` works as intended if the maximal amount of fields are given.
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
    required_permissions = Permission().update_by_keys(administrator = True)
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
    
    vampytest.assert_eq(application_command.name, name)
    vampytest.assert_eq(application_command.description, description)
    vampytest.assert_eq(application_command.allow_in_dm, allow_in_dm)
    vampytest.assert_eq(application_command.description_localizations, description_localizations)
    vampytest.assert_eq(application_command.name_localizations, name_localizations)
    vampytest.assert_eq(application_command.nsfw, nsfw)
    vampytest.assert_eq(application_command.options, options)
    vampytest.assert_eq(application_command.required_permissions, required_permissions)
    vampytest.assert_is(application_command.target_type, target_type)
    
    # Also test the extra fields whether they are set.
    vampytest.assert_instance(application_command.id, int)
    vampytest.assert_instance(application_command.application_id, int)
    vampytest.assert_instance(application_command.guild_id, int)
    vampytest.assert_instance(application_command.version, int)


def test__ApplicationCommand__new__1():
    """
    Tests whether ``ApplicationCommand.__new__`` works as intended if the minimal amount of fields are given.
    """
    name = 'owo'
    
    application_command = ApplicationCommand(
        name,
    )
    
    vampytest.assert_eq(application_command.name, name)
    vampytest.assert_instance(application_command.description, str, nullable=True)
    vampytest.assert_instance(application_command.allow_in_dm, bool)
    vampytest.assert_instance(application_command.description_localizations, dict, nullable=True)
    vampytest.assert_instance(application_command.name_localizations, dict, nullable=True)
    vampytest.assert_instance(application_command.nsfw, bool)
    vampytest.assert_instance(application_command.options, list, nullable=True)
    vampytest.assert_instance(application_command.required_permissions, Permission)
    vampytest.assert_instance(application_command.target_type, ApplicationCommandTargetType)
    
    # Also test the extra fields whether they are set.
    vampytest.assert_instance(application_command.id, int)
    vampytest.assert_instance(application_command.application_id, int)
    vampytest.assert_instance(application_command.guild_id, int)
    vampytest.assert_instance(application_command.version, int)


def test__ApplicationCommand__create_empty():
    """
    Tests whether ``ApplicationCommand._create_empty`` works as intended.
    """
    application_command_id = 202209030000
    application_id = 202209030001
    
    application_command = ApplicationCommand._create_empty(application_command_id, application_id)
    
    vampytest.assert_instance(application_command.name, str)
    vampytest.assert_instance(application_command.description, str, nullable=True)
    vampytest.assert_instance(application_command.allow_in_dm, bool)
    vampytest.assert_instance(application_command.description_localizations, dict, nullable=True)
    vampytest.assert_instance(application_command.name_localizations, dict, nullable=True)
    vampytest.assert_instance(application_command.nsfw, bool)
    vampytest.assert_instance(application_command.options, list, nullable=True)
    vampytest.assert_instance(application_command.required_permissions, Permission)
    vampytest.assert_instance(application_command.target_type, ApplicationCommandTargetType)
    
    vampytest.assert_eq(application_command.id, application_command_id)
    vampytest.assert_eq(application_command.application_id, application_id)
    vampytest.assert_instance(application_command.guild_id, int)
    vampytest.assert_instance(application_command.version, int)
