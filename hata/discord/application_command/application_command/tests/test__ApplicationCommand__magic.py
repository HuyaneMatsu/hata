import vampytest

from ....application import ApplicationIntegrationType
from ....localization import Locale
from ....permission import Permission

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..application_command import ApplicationCommand
from ..preinstanced import ApplicationCommandIntegrationContextType, ApplicationCommandTargetType


def test__ApplicationCommand__len__no_description():
    """
    Tests whether ``ApplicationCommand.__len__`` works as intended if the minimal amount of fields are given at
    creation.
    
    We directly set `target_type`, so `description` can default to `None` instead of `str`
    """
    application_command = ApplicationCommand(
        'owo',
        None,
        target_type = ApplicationCommandTargetType.user,
    )
    
    return len(application_command)


def test__ApplicationCommand__len__all_fields():
    """
    Tests whether ``ApplicationCommand.__len__`` works as intended if the maximal amount of fields are given at
    creation.
    """
    application_command = ApplicationCommand(
        'owo',
        'description',
        description_localizations = {
            Locale.thai: 'ayy',
            Locale.czech: 'yay',
        },
        integration_context_types = [
            ApplicationCommandIntegrationContextType.guild,
            ApplicationCommandIntegrationContextType.any_private_channel,
        ],
        integration_types = [ApplicationIntegrationType.user_install],
        name_localizations = {
            Locale.thai: 'nay',
            Locale.czech: 'lay',
        },
        nsfw = True,
        options = [
            ApplicationCommandOption(
                'option',
                'optional',
                ApplicationCommandOptionType.string,

            )
        ],
        required_permissions = Permission().update_by_keys(administrator = True),
        target_type = ApplicationCommandTargetType.chat,
    )
    
    return len(application_command)



def test__ApplicationCommand__len__longest_in_localization():
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


def test__ApplicationCommand__len__longest_description():
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


def test__ApplicationCommand__len__longest_localized_description():
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


def test__ApplicationCommand__len__longest_is_name():
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


def test__ApplicationCommand__repr():
    """
    Tests whether ``ApplicationCommand.__repr__`` works as intended.
    """
    application_command = ApplicationCommand(
        'owo',
        'description',
        description_localizations = {
            Locale.thai: 'ayy',
            Locale.czech: 'yay',
        },
        name_localizations = {
            Locale.thai: 'nay',
            Locale.czech: 'lay',
        },
        integration_context_types = [
            ApplicationCommandIntegrationContextType.guild,
            ApplicationCommandIntegrationContextType.any_private_channel,
        ],
        integration_types = [ApplicationIntegrationType.user_install],
        nsfw = True,
        options = [
            ApplicationCommandOption(
                'option',
                'optional',
                ApplicationCommandOptionType.string,

            )
        ],
        required_permissions = Permission().update_by_keys(administrator = True),
        target_type = ApplicationCommandTargetType.chat,
    )
    
    vampytest.assert_instance(repr(application_command), str)


def test__ApplicationCommand__eq():
    """
    Tests whether ``ApplicationCommand.__eq__`` works as intended.
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
    new_target_type = ApplicationCommandTargetType.message
    
    old_fields = {
        'description': old_description,
        'description_localizations': old_description_localizations,
        'integration_context_types': old_integration_context_types,
        'integration_types': old_integration_types,
        'name': old_name,
        'name_localizations': old_name_localizations,
        'nsfw': old_nsfw,
        'options': old_options,
        'required_permissions': old_required_permissions,
        'target_type': old_target_type,
    }
    
    vampytest.assert_eq(
        ApplicationCommand(**old_fields),
        ApplicationCommand(**old_fields),
    )
    
    for field_name, field_value in (
        ('description', new_description),
        ('description_localizations', new_description_localizations),
        ('integration_context_types', new_integration_context_types),
        ('integration_types', new_integration_types),
        ('name', new_name),
        ('name_localizations', new_name_localizations),
        ('nsfw', new_nsfw),
        ('options', new_options),
        ('required_permissions', new_required_permissions),
        ('target_type', new_target_type),
    ):
        vampytest.assert_eq(
            ApplicationCommand(**old_fields),
            ApplicationCommand(**{**old_fields, field_name: field_value}),
            reverse = True
        )


def test__ApplicationCommand__hash():
    """
    Tests whether ``ApplicationCommand.__hash__`` works as intended.
    """
    application_command = ApplicationCommand(
        'owo',
        'description',
        description_localizations = {
            Locale.thai: 'ayy',
            Locale.czech: 'yay',
        },
        integration_context_types = [
            ApplicationCommandIntegrationContextType.guild,
            ApplicationCommandIntegrationContextType.any_private_channel,
        ],
        integration_types = [ApplicationIntegrationType.user_install],
        name_localizations = {
            Locale.thai: 'nay',
            Locale.czech: 'lay',
        },
        nsfw = True,
        options = [
            ApplicationCommandOption(
                'option',
                'optional',
                ApplicationCommandOptionType.string,

            )
        ],
        required_permissions = Permission().update_by_keys(administrator = True),
        target_type = ApplicationCommandTargetType.chat,
    )
    
    vampytest.assert_instance(hash(application_command), int)


def test__ApplicationCommand__format():
    """
    Tests whether ``ApplicationCommand.__format__`` works as intended.
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
        description = description,
        description_localizations = description_localizations,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        name = name,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    vampytest.assert_instance(format(application_command, ''), str)
