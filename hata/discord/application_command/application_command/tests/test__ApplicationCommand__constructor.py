import vampytest

from ....application import ApplicationIntegrationType
from ....localization import Locale
from ....permission import Permission

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..application_command import ApplicationCommand
from ..preinstanced import (
    ApplicationCommandHandlerType, ApplicationCommandIntegrationContextType, ApplicationCommandTargetType
)


def _assert_fields_set(application_command):
    """
    Asserts whether every fields are set of the given application command.
    
    Parameters
    ----------
    application_command : ``ApplicationCommand``
        The application command to check.
    """
    vampytest.assert_instance(application_command, ApplicationCommand)
    vampytest.assert_instance(application_command.application_id, int)
    vampytest.assert_instance(application_command.description, str, nullable = True)
    vampytest.assert_instance(application_command.description_localizations, dict, nullable = True)
    vampytest.assert_instance(application_command.guild_id, int)
    vampytest.assert_instance(application_command.handler_type, ApplicationCommandHandlerType)
    vampytest.assert_instance(application_command.id, int)
    vampytest.assert_instance(application_command.integration_context_types, tuple, nullable = True)
    vampytest.assert_instance(application_command.integration_types, tuple, nullable = True)
    vampytest.assert_instance(application_command.name, str)
    vampytest.assert_instance(application_command.name_localizations, dict, nullable = True)
    vampytest.assert_instance(application_command.nsfw, bool)
    vampytest.assert_instance(application_command.options, tuple, nullable = True)
    vampytest.assert_instance(application_command.required_permissions, Permission)
    vampytest.assert_instance(application_command.target_type, ApplicationCommandTargetType)
    vampytest.assert_instance(application_command.version, int)
    


def test__ApplicationCommand__new__no_fields():
    """
    Tests whether ``ApplicationCommand.__new__`` works as intended if the minimal amount of fields are given.
    """
    name = 'owo'
    
    application_command = ApplicationCommand(
        name,
    )
    _assert_fields_set(application_command)
    
    vampytest.assert_eq(application_command.name, name)
    vampytest.assert_eq(application_command.integration_types, None)


def test__ApplicationCommand__new__all_fields():
    """
    Tests whether ``ApplicationCommand.__new__`` works as intended if the maximal amount of fields are given.
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
    _assert_fields_set(application_command)
    
    vampytest.assert_eq(application_command.name, name)
    vampytest.assert_eq(application_command.description, description)
    vampytest.assert_eq(application_command.description_localizations, description_localizations)
    vampytest.assert_is(application_command.handler_type, handler_type)
    vampytest.assert_eq(application_command.integration_context_types, tuple(integration_context_types))
    vampytest.assert_eq(application_command.integration_types, tuple(integration_types))
    vampytest.assert_eq(application_command.name_localizations, name_localizations)
    vampytest.assert_eq(application_command.nsfw, nsfw)
    vampytest.assert_eq(application_command.options, tuple(options))
    vampytest.assert_eq(application_command.required_permissions, required_permissions)
    vampytest.assert_is(application_command.target_type, target_type)



def test__ApplicationCommand__precreate__no_fields():
    """
    Tests whether ``ApplicationCommand.precreate`` works as intended.
    
    Case: No extra fields given.
    """
    application_command_id = 202310300000
    
    application_command = ApplicationCommand.precreate(
        application_command_id,
    )
    _assert_fields_set(application_command)
    
    vampytest.assert_eq(application_command.id, application_command_id)
    vampytest.assert_eq(application_command.integration_types, None)


def test__ApplicationCommand__precreate__caching():
    """
    Tests whether ``ApplicationCommand.precreate`` works as intended.
    
    Case: Caching.
    """
    application_command_id = 202310300001
    
    application_command = ApplicationCommand.precreate(
        application_command_id,
    )
    
    test_application_command = ApplicationCommand.precreate(
        application_command_id,
    )
    
    vampytest.assert_is(application_command, test_application_command)


def test__ApplicationCommand__precreate__all_fields():
    """
    Tests whether ``ApplicationCommand.precreate`` works as intended.
    
    Case: All fields given.
    """
    application_command_id = 202310300002
    application_id = 202310300003
    guild_id = 202310300004
    version = 202310300005
    
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
    
    application_command = ApplicationCommand.precreate(
        application_command_id,
        application_id = application_id,
        guild_id = guild_id,
        version = version,
        name = name,
        description = description,
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
    
    _assert_fields_set(application_command)
    
    vampytest.assert_eq(application_command.id, application_command_id)
    vampytest.assert_eq(application_command.application_id, application_id)
    vampytest.assert_eq(application_command.guild_id, guild_id)
    vampytest.assert_eq(application_command.version, version)
    
    vampytest.assert_eq(application_command.name, name)
    vampytest.assert_eq(application_command.description, description)
    vampytest.assert_eq(application_command.description_localizations, description_localizations)
    vampytest.assert_eq(application_command.integration_context_types, tuple(integration_context_types))
    vampytest.assert_eq(application_command.integration_types, tuple(integration_types))
    vampytest.assert_eq(application_command.name_localizations, name_localizations)
    vampytest.assert_eq(application_command.nsfw, nsfw)
    vampytest.assert_eq(application_command.options, tuple(options))
    vampytest.assert_eq(application_command.required_permissions, required_permissions)
    vampytest.assert_is(application_command.target_type, target_type)



def test__ApplicationCommand__create_empty():
    """
    Tests whether ``ApplicationCommand._create_empty`` works as intended.
    """
    application_command_id = 202209030000
    application_id = 202209030001
    
    application_command = ApplicationCommand._create_empty(application_command_id, application_id)
    _assert_fields_set(application_command)
    
    vampytest.assert_eq(application_command.id, application_command_id)
    vampytest.assert_eq(application_command.application_id, application_id)
    vampytest.assert_eq(application_command.integration_types, None)
