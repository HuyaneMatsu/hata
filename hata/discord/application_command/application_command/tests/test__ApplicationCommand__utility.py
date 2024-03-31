import vampytest

from ....application import ApplicationIntegrationType
from ....localization import Locale
from ....permission import Permission

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..application_command import ApplicationCommand
from ..preinstanced import ApplicationCommandIntegrationContextType, ApplicationCommandTargetType

from .test__ApplicationCommand__constructor import _assert_fields_set


def test__ApplicationCommand__copy():
    """
    Tests whether ``ApplicationCommand.copy`` works as intended.
    """
    description = 'description'
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.any_private_channel,
    ]
    integration_types = [ApplicationIntegrationType.user_install]
    name = 'owo'
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
        description_localizations = description_localizations,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    copy = application_command.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(application_command, copy)
    vampytest.assert_eq(application_command, copy)


def test__ApplicationCommand__copy_with__no_fields():
    """
    Tests whether ``ApplicationCommand.copy_with`` works as intended.
    
    Case: No fields given.
    """
    description = 'description'
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.any_private_channel,
    ]
    integration_types = [ApplicationIntegrationType.user_install]
    name = 'owo'
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
        description_localizations = description_localizations,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    copy = application_command.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(application_command, copy)
    vampytest.assert_eq(application_command, copy)


def test__ApplicationCommand__copy_with__all_fields():
    """
    Tests whether ``ApplicationCommand.copy_with`` works as intended.
    
    Case: No fields given.
    """

    old_description = 'description'
    old_description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    old_integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.any_private_channel,
    ]
    old_integration_types = [ApplicationIntegrationType.user_install]
    old_name = 'hey'
    old_name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    old_nsfw = True
    old_options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    old_required_permissions = Permission().update_by_keys(administrator = True)
    old_target_type = ApplicationCommandTargetType.chat
    
    new_description = 'mars'
    new_description_localizations = {
        Locale.dutch: 'aya',
        Locale.greek: 'yya',
    }
    new_integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    new_integration_types = [ApplicationIntegrationType.guild_install, ApplicationIntegrationType.user_install]
    new_name = 'mister'
    new_name_localizations = {
        Locale.dutch: 'aya',
        Locale.greek: 'yya',
    }
    new_nsfw = False
    new_options = [
        ApplicationCommandOption(
            'hello',
            'hell',
            ApplicationCommandOptionType.float,

        )
    ]
    new_required_permissions = Permission().update_by_keys(kick_users = True)
    new_target_type = ApplicationCommandTargetType.chat # we wont edit this or else we would drop a few other fields.
    
    application_command = ApplicationCommand(
        old_name,
        old_description,
        description_localizations = old_description_localizations,
        integration_context_types = old_integration_context_types,
        integration_types = old_integration_types,
        name_localizations = old_name_localizations,
        nsfw = old_nsfw,
        options = old_options,
        required_permissions = old_required_permissions,
        target_type = old_target_type,
    )
    
    copy = application_command.copy_with(
        description = new_description,
        description_localizations = new_description_localizations,
        integration_context_types = new_integration_context_types,
        integration_types = new_integration_types,
        name = new_name,
        name_localizations = new_name_localizations,
        nsfw = new_nsfw,
        options = new_options,
        required_permissions = new_required_permissions,
        target_type = new_target_type,
    )
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.description_localizations, new_description_localizations)
    vampytest.assert_eq(copy.integration_context_types, tuple(new_integration_context_types))
    vampytest.assert_eq(copy.integration_types, tuple(new_integration_types))
    vampytest.assert_eq(copy.name_localizations, new_name_localizations)
    vampytest.assert_eq(copy.nsfw, new_nsfw)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.required_permissions, new_required_permissions)
    vampytest.assert_is(copy.target_type, new_target_type)


def test__ApplicationCommand__with_translation():
    """
    Tests whether ``ApplicationCommand.with_translation` works as intended.
    """
    option = ApplicationCommand(
        'yukari',
        'ran',
        options = [ApplicationCommandOption('aya', 'aya', ApplicationCommandOptionType.string)],
    )
    
    translation_table = {
        Locale.german: {
            'yukari': 'satori',
            'ran': 'orin',
            'chen': 'okuu',
            'aya': 'momiji',
        }
    }
    
    expected_output = ApplicationCommand(
        'yukari',
        'ran',
        name_localizations = {
            Locale.german: 'satori',
        },
        description_localizations = {
            Locale.german: 'orin',
        },
        options = [
            ApplicationCommandOption(
                'aya',
                'aya',
                ApplicationCommandOptionType.string,
                name_localizations = {
                    Locale.german: 'momiji',
                },
                description_localizations = {
                    Locale.german: 'momiji',
                },
            ),
        ],
    )
    
    output = option.with_translation(translation_table)
    vampytest.assert_eq(output, expected_output)
