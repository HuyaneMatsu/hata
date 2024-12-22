import vampytest

from ....application import ApplicationIntegrationType
from ....localization import Locale
from ....permission import Permission

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..application_command import ApplicationCommand
from ..preinstanced import (
    ApplicationCommandHandlerType, ApplicationCommandIntegrationContextType, ApplicationCommandTargetType
)


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
    
    output = len(application_command)
    vampytest.assert_instance(output, int)


def test__ApplicationCommand__len__all_fields():
    """
    Tests whether ``ApplicationCommand.__len__`` works as intended if the maximal amount of fields are given at
    creation.
    """
    name = 'owo'
    description = 'description'
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    handler_type = ApplicationCommandHandlerType.discord_embedded_activity_launcher
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.any_private_channel,
    ]
    integration_types = [ApplicationIntegrationType.user_install]
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
        handler_type = handler_type,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    output = len(application_command)
    vampytest.assert_instance(output, int)



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
    name = 'owo'
    description = 'description'
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    handler_type = ApplicationCommandHandlerType.discord_embedded_activity_launcher
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.any_private_channel,
    ]
    integration_types = [ApplicationIntegrationType.user_install]
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
        handler_type = handler_type,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    output = repr(application_command)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    description = 'description'
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    handler_type = ApplicationCommandHandlerType.discord_embedded_activity_launcher
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.any_private_channel,
    ]
    integration_types = [ApplicationIntegrationType.user_install]
    name = 'hey'
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
    
    keyword_parameters = {
        'description': description,
        'description_localizations': description_localizations,
        'handler_type': handler_type,
        'integration_context_types': integration_context_types,
        'integration_types': integration_types,
        'name': name,
        'name_localizations': name_localizations,
        'nsfw': nsfw,
        'options': options,
        'required_permissions': required_permissions,
        'target_type': target_type,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'mars',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description_localizations': {
                Locale.dutch: 'aya',
                Locale.greek: 'yya',
            },
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'integration_context_types': [
                ApplicationCommandIntegrationContextType.guild,
                ApplicationCommandIntegrationContextType.bot_private_channel,
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'integration_types': [
                ApplicationIntegrationType.guild_install,
                ApplicationIntegrationType.user_install,
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'mister',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name_localizations': {
                Locale.dutch: 'aya',
                Locale.greek: 'yya',
            },
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'nsfw': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'options': [
                ApplicationCommandOption(
                    'hello',
                    'hell',
                    ApplicationCommandOptionType.float,
                ),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'required_permissions': Permission().update_by_keys(kick_users = True),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_type': ApplicationCommandTargetType.message,
        },
        False,
    )
    


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ApplicationCommand__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ApplicationCommand.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    application_command_0 = ApplicationCommand(**keyword_parameters_0)
    application_command_1 = ApplicationCommand(**keyword_parameters_1)
    
    output = application_command_0 == application_command_1
    vampytest.assert_instance(output, bool)
    return output


def test__ApplicationCommand__hash():
    """
    Tests whether ``ApplicationCommand.__hash__`` works as intended.
    """
    name = 'owo'
    description = 'description'
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    handler_type = ApplicationCommandHandlerType.discord_embedded_activity_launcher
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.any_private_channel,
    ]
    integration_types = [ApplicationIntegrationType.user_install]
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
        handler_type = handler_type,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    output = hash(application_command)
    vampytest.assert_instance(output, int)


def test__ApplicationCommand__format():
    """
    Tests whether ``ApplicationCommand.__format__`` works as intended.
    """
    description = 'description'
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    handler_type = ApplicationCommandHandlerType.discord_embedded_activity_launcher
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
        handler_type = handler_type,
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
