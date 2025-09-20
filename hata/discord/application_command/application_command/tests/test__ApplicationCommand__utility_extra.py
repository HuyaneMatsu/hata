from datetime import datetime as DateTime

import vampytest

from ....application import ApplicationIntegrationType
from ....guild import Guild
from ....utils import id_to_datetime

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..application_command import ApplicationCommand
from ..preinstanced import ApplicationCommandIntegrationContextType, ApplicationCommandTargetType


def test__ApplicationCommand__mention_sub_command():
    """
    Tests whether ``ApplicationCommand.mention_sub_command`` works as intended.
    """
    name = 'kimi'
    sub_command_names = ['no', 'kiseki']
    
    application_command = ApplicationCommand(name)
    
    output = application_command.mention_sub_command(*sub_command_names)
    
    vampytest.assert_instance(output, str)
    
    for sub_command_name in sub_command_names:
        vampytest.assert_in(sub_command_name, output)


def test__ApplicationCommand__mention_with():
    """
    Tests whether ``ApplicationCommand.mention_sub_command`` works as intended.
    """
    name = 'kimi'
    with_ = 'no kiseki'
    
    application_command = ApplicationCommand(name)
    
    output = application_command.mention_with(with_)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(with_, output)


def test__ApplicationCommand__mention():
    """
    Tests whether ``ApplicationCommand.mention`` works as intended.
    """
    name = 'kimi'
    
    application_command = ApplicationCommand(name)
    
    output = application_command.mention
    
    vampytest.assert_instance(output, str)


def test__ApplicationCommand__display_name():
    """
    Tests whether ``ApplicationCommand.display_name`` works as intended.
    """
    name = 'kimi'
    
    application_command = ApplicationCommand(name)
    
    output = application_command.display_name
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(name.casefold(), output.casefold())


def _iter_options__edited_at():
    
    version = 202302260014
    
    yield 202403280003, 0, None
    yield 202403280004, version, id_to_datetime(version)


@vampytest._(vampytest.call_from(_iter_options__edited_at()).returning_last())
def test__ApplicationCommand__edited_at(application_command_id, version):
    """
    Tests whether ``ApplicationCommand.edited_at`` works as intended.
    
    Parameters
    ----------
    application_command_id : `int`
        Identifier to create the application command with.
    version : `int`
        Version to create the application command with.
    
    Returns
    -------
    output : `None | DateTime`
    """
    application_command = ApplicationCommand.precreate(application_command_id, name = 'kimi', version = version)
        
    output = application_command.edited_at
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output


def _iter_options__partial():
    yield 0, True
    yield 202302260015, False


@vampytest._(vampytest.call_from(_iter_options__partial()).returning_last())
def test__ApplicationCommand__partial(application_command_id):
    """
    Tests whether ``ApplicationCommand.partial`` works as intended.
    
    Parameters
    ----------
    application_command_id : `int`
        The application command's identifier.
    
    Returns
    -------
    output : `bool`
    """
    application_command = ApplicationCommand('kimi')
    application_command.id = application_command_id
    
    output = application_command.partial
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__is_context_command():
    yield ApplicationCommandTargetType.message, True
    yield ApplicationCommandTargetType.chat, False


@vampytest._(vampytest.call_from(_iter_options__is_context_command()).returning_last())
def test__ApplicationCommand__is_context_command(target_type):
    """
    Tests whether ``ApplicationCommand.is_context_command`` works as intended.
    
    Parameters
    ----------
    target_type : ``ApplicationCommandTargetType``
        Target type to create the application with.
    
    Returns
    -------
    output : `bool`
    """
    application_command = ApplicationCommand('kimi', target_type = target_type)
    output = application_command.is_context_command()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__is_slash_command():
    yield ApplicationCommandTargetType.message, False
    yield ApplicationCommandTargetType.chat, True


@vampytest._(vampytest.call_from(_iter_options__is_slash_command()).returning_last())
def test__ApplicationCommand__is_slash_command(target_type):
    """
    Tests whether ``ApplicationCommand.is_slash_command`` works as intended.
    
    Parameters
    ----------
    target_type : ``ApplicationCommandTargetType``
        Target type to create the application with.
    
    Returns
    -------
    output : `bool`
    """
    application_command = ApplicationCommand('kimi', target_type = target_type)
    output = application_command.is_slash_command()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__guild():
    guild_id_0 = 202302260016
    guild_id_1 = 202302260017
    
    yield 202403280000, 0, None
    yield 202403280001, guild_id_0, None
    yield 202403280002, guild_id_1, Guild.precreate(guild_id_1)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__ApplicationCommand__guild(application_command_id, guild_id):
    """
    Tests whether ``ApplicationCommand.guild`` works as intended.
    
    Parameters
    ----------
    application_command_id : `int`
        Application command identifier to test with.
    guild_id : `int`
        Guild identifier to create the application command with.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    application_command = ApplicationCommand.precreate(application_command_id, name = 'kimi', guild_id = guild_id)
    return application_command.guild


def _iter_options__iter_options():
    option_0 = ApplicationCommandOption('okuu', 'orin', ApplicationCommandOptionType.string)
    option_1 = ApplicationCommandOption('orin', 'okuu', ApplicationCommandOptionType.integer)
    
    yield None, []
    yield [option_0], [option_0]
    yield [option_0, option_1], [option_0, option_1]


@vampytest._(vampytest.call_from(_iter_options__iter_options()).returning_last())
def test__ApplicationCommand__iter_options(options):
    """
    Tests whether ``ApplicationCommand.iter_options`` works as intended.
    
    Parameters
    ----------
    options : `None | list<ApplicationCommandOption>`
        Options to create the application command with.
    
    Returns
    -------
    output : `list<ApplicationCommandOption>`
    """
    application_command = ApplicationCommand('kimi', options = options)
    return [*application_command.iter_options()]


def _iter_options__has_integration_type():
    integration_type_0 = ApplicationIntegrationType.guild_install
    integration_type_1 = ApplicationIntegrationType.user_install
    
    yield None, integration_type_0, False
    yield [integration_type_0], integration_type_0, True
    yield [integration_type_0], integration_type_1, False
    yield [integration_type_0, integration_type_1], integration_type_1, True
    
    yield [integration_type_0.value], integration_type_0, True
    yield [integration_type_0.value], integration_type_1, False


@vampytest._(vampytest.call_from(_iter_options__has_integration_type()).returning_last())
def test__ApplicationCommand__has_integration_type(integration_types, integration_type):
    """
    Tests whether ``ApplicationCommand.has_integration_type`` works as intended.
    
    Parameters
    ----------
    integration_types : ``None | list<ApplicationIntegrationType>``
        Application integration types to create the application command with.
    integration_type : ``int | ApplicationIntegrationType``
        Integration type to check for.
    
    Returns
    -------
    output : `bool`
    """
    application = ApplicationCommand('Yuuhei', integration_types = integration_types)
    return application.has_integration_type(integration_type)


def _iter_options__iter_integration_types():
    integration_type_0 = ApplicationIntegrationType.guild_install
    integration_type_1 = ApplicationIntegrationType.user_install
    
    yield None, []
    yield [integration_type_0], [integration_type_0]
    yield [integration_type_0, integration_type_1], [integration_type_0, integration_type_1]


@vampytest._(vampytest.call_from(_iter_options__iter_integration_types()).returning_last())
def test__ApplicationCommand__iter_integration_types(integration_types):
    """
    Tests whether ``ApplicationCommand.iter_integration_types`` works as intended.
    
    Parameters
    ----------
    integration_types : ``None | list<ApplicationIntegrationType>``
        Application integration types to create the application command with.
    
    Returns
    -------
    output : `list<ApplicationIntegrationType>`
    """
    application = ApplicationCommand('Yuuhei', integration_types = integration_types)
    return [*application.iter_integration_types()]


def _iter_options__has_integration_context_type():
    integration_context_type_0 = ApplicationCommandIntegrationContextType.guild
    integration_context_type_1 = ApplicationCommandIntegrationContextType.bot_private_channel
    
    yield None, integration_context_type_0, False
    yield [integration_context_type_0], integration_context_type_0, True
    yield [integration_context_type_0], integration_context_type_1, False
    yield [integration_context_type_0, integration_context_type_1], integration_context_type_1, True
    
    yield [integration_context_type_0.value], integration_context_type_0, True
    yield [integration_context_type_0.value], integration_context_type_1, False


@vampytest._(vampytest.call_from(_iter_options__has_integration_context_type()).returning_last())
def test__ApplicationCommand__has_integration_context_type(integration_context_types, integration_context_type):
    """
    Tests whether ``ApplicationCommand.has_integration_context_type`` works as intended.
    
    Parameters
    ----------
    integration_context_types : `None | list<ApplicationCommandIntegrationContextType>`
        Application integration context types to create the application command with.
    integration_context_type : `int | ApplicationCommandIntegrationContextType`
        Integration type to check for.
    
    Returns
    -------
    output : `bool`
    """
    application = ApplicationCommand('Yuuhei', integration_context_types = integration_context_types)
    return application.has_integration_context_type(integration_context_type)


def _iter_options__iter_integration_context_types():
    integration_context_type_0 = ApplicationCommandIntegrationContextType.guild
    integration_context_type_1 = ApplicationCommandIntegrationContextType.bot_private_channel
    
    yield None, []
    yield [integration_context_type_0], [integration_context_type_0]
    yield [integration_context_type_0, integration_context_type_1], [integration_context_type_0, integration_context_type_1]


@vampytest._(vampytest.call_from(_iter_options__iter_integration_context_types()).returning_last())
def test__ApplicationCommand__iter_integration_context_types(integration_context_types):
    """
    Tests whether ``ApplicationCommand.iter_integration_context_types`` works as intended.
    
    Parameters
    ----------
    integration_context_types : `None | list<ApplicationCommandIntegrationContextType>`
        Application integration context types to create the application command with.
    
    Returns
    -------
    output : `list<ApplicationCommandIntegrationContextType>`
    """
    application = ApplicationCommand('Yuuhei', integration_context_types = integration_context_types)
    return [*application.iter_integration_context_types()]
