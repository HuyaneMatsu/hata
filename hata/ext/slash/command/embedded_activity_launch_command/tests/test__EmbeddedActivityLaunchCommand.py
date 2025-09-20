import vampytest
from scarletio import WeakReferer

from ......discord.application import ApplicationIntegrationType
from ......discord.application_command import (
    ApplicationCommand, ApplicationCommandIntegrationContextType, ApplicationCommandPermissionOverwrite,
    ApplicationCommandPermissionOverwriteTargetType, ApplicationCommandTargetType
)
from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.interaction import (
    InteractionEvent, InteractionMetadataApplicationCommand, InteractionType
)
from ......discord.permission import Permission

from ....response_modifier import ResponseModifier
from ....utils import UNLOADING_BEHAVIOUR_DELETE

from ..embedded_activity_launch_command import ApplicationCommandHandlerType, EmbeddedActivityLaunchCommand


def _assert_fields_set(embedded_activity_launch_command):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    embedded_activity_launch_command : ``EmbeddedActivityLaunchCommand``
        The command to checkout.
    """
    vampytest.assert_instance(embedded_activity_launch_command, EmbeddedActivityLaunchCommand)
    vampytest.assert_instance(embedded_activity_launch_command._exception_handlers, list, nullable = True)
    vampytest.assert_instance(embedded_activity_launch_command._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(embedded_activity_launch_command.name, str)
    vampytest.assert_instance(embedded_activity_launch_command._permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(
        embedded_activity_launch_command._registered_application_command_ids, dict, nullable = True,
    )
    vampytest.assert_instance(embedded_activity_launch_command._schema, ApplicationCommand, nullable = True)
    vampytest.assert_instance(embedded_activity_launch_command._unloading_behaviour, int)
    
    vampytest.assert_instance(embedded_activity_launch_command._command_function, object)
    vampytest.assert_instance(embedded_activity_launch_command.global_, bool)
    vampytest.assert_instance(embedded_activity_launch_command.guild_ids, set, nullable = True)
    vampytest.assert_instance(embedded_activity_launch_command.integration_context_types, tuple, nullable = True)
    vampytest.assert_instance(embedded_activity_launch_command.integration_types, tuple, nullable = True)
    vampytest.assert_instance(embedded_activity_launch_command.nsfw, bool)
    vampytest.assert_instance(embedded_activity_launch_command.required_permissions, Permission)
    vampytest.assert_instance(embedded_activity_launch_command.response_modifier, ResponseModifier, nullable = True)


def test__EmbeddedActivityLaunchCommand__new():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.__new__`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    show_for_invoking_user_only = True
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    _assert_fields_set(embedded_activity_launch_command)
    
    vampytest.assert_is(embedded_activity_launch_command._command_function, function)
    vampytest.assert_eq(embedded_activity_launch_command._unloading_behaviour, UNLOADING_BEHAVIOUR_DELETE)
    vampytest.assert_eq(embedded_activity_launch_command.global_, True)
    vampytest.assert_is(embedded_activity_launch_command.guild_ids, None)
    vampytest.assert_eq(embedded_activity_launch_command.integration_context_types, tuple(integration_context_types))
    vampytest.assert_eq(embedded_activity_launch_command.integration_types, tuple(integration_types))
    vampytest.assert_eq(embedded_activity_launch_command.name, name)
    vampytest.assert_eq(embedded_activity_launch_command.nsfw, nsfw)
    vampytest.assert_eq(embedded_activity_launch_command.required_permissions, required_permissions)
    vampytest.assert_eq(
        embedded_activity_launch_command.response_modifier,
        ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only}),
    )


def _iter_options__new__only_global_check():
    yield {}, False
    yield {'is_global': False}, True
    yield {'is_global': True}, False
    yield {'guild': [202412210050]}, True


@vampytest._(vampytest.call_from(_iter_options__new__only_global_check()).returning_last())
def test__new__only_global_check(keyword_parameters):
    """
    Tests whether ``EmbeddedActivityLaunchCommand.__new__`` works as intended.
    
    Case: only global commands are allowed.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to call ``EmbeddedActivityLaunchCommand`` with.
    
    Returns
    -------
    raised : `bool`
    """
    function = None
    name = 'yuuka'
    
    try:
        embedded_activity_launch_command = EmbeddedActivityLaunchCommand(
            function,
            name,
            **keyword_parameters,
        )
    except TypeError:
        return True
    
    vampytest.assert_eq(embedded_activity_launch_command.global_, True)
    return False


def test__EmbeddedActivityLaunchCommand__repr():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.__repr__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    guild_id = 2024120432
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    show_for_invoking_user_only = True
    permission_overwrite = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 20241204303),
        True,
    )
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    embedded_activity_launch_command.error(exception_handler)
    embedded_activity_launch_command.add_permission_overwrite(guild_id, permission_overwrite)
    response_modifier = ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only})
    
    output = repr(embedded_activity_launch_command)
    vampytest.assert_in(type(embedded_activity_launch_command).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)
    vampytest.assert_in(f'type = global', output)
    vampytest.assert_in(f'unloading_behaviour = delete', output)
    vampytest.assert_in(f'integration_context_types = {tuple(integration_context_types)!r}', output)
    vampytest.assert_in(f'integration_types = {tuple(integration_types)!r}', output)
    vampytest.assert_in(f'nsfw = {nsfw!r}', output)
    vampytest.assert_in(f'required_permissions = {required_permissions!r}', output)
    vampytest.assert_in(f'response_modifier = {response_modifier!r}', output)
    vampytest.assert_in(f'command_function = {function!r}', output)
    vampytest.assert_in(f'permission_overwrites = { {guild_id: [permission_overwrite]}!r}', output)


def test__EmbeddedActivityLaunchCommand__hash():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.__hash__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    show_for_invoking_user_only = True
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    embedded_activity_launch_command.error(exception_handler)
    
    output = hash(embedded_activity_launch_command)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    async def function_0():
        pass
    
    async def function_1():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    nsfw = True
    required_permissions = Permission(8)
    show_for_invoking_user_only = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function_0,
        'name': name,
        'delete_on_unload': delete_on_unload,
        'integration_context_types': integration_context_types,
        'integration_types': integration_types,
        'nsfw': nsfw,
        'required_permissions': required_permissions,
        'show_for_invoking_user_only': show_for_invoking_user_only,
    }
    
    yield (
        keyword_parameters,
        (),
        keyword_parameters,
        (),
        True,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'function': function_1,
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'name': 'kazami',
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'delete_on_unload': False,
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'integration_context_types': [ApplicationCommandIntegrationContextType.guild],
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'integration_types': [ApplicationIntegrationType.guild_install],
        },
        (),
        False,
    )
    
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'nsfw': False,
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'required_permissions': Permission(6),
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'show_for_invoking_user_only': False,
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        keyword_parameters,
        (exception_handler,),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbeddedActivityLaunchCommand__eq(keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1):
    """
    Tests whether ``EmbeddedActivityLaunchCommand.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_0 : `tuple<CoroutineFunctionType>`
        Exception handlers to register to the instance.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_1 : `tuple<CoroutineFunctionType>`
        Exception handlers to register to the instance.
    
    Returns
    -------
    output : `bool`
    """
    embedded_activity_launch_command_0 = EmbeddedActivityLaunchCommand(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        embedded_activity_launch_command_0.error(exception_handler)
    
    embedded_activity_launch_command_1 = EmbeddedActivityLaunchCommand(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        embedded_activity_launch_command_1.error(exception_handler)
    
    output = embedded_activity_launch_command_0 == embedded_activity_launch_command_1
    vampytest.assert_instance(output, bool)
    return output


async def test__EmbeddedActivityLaunchCommand__invoke():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.invoke`` works as intended.
    
    This function is a coroutine.
    """
    client = None
    interaction_event = None
    function_called = 0
    
    async def function(input_client : Client, input_interaction_event : InteractionEvent):
        nonlocal client
        nonlocal interaction_event
        nonlocal function_called
        
        vampytest.assert_is_not(input_client, None)
        vampytest.assert_is_not(input_interaction_event, None)
        
        vampytest.assert_is(input_client, client)
        vampytest.assert_is(input_interaction_event, interaction_event)
        
        function_called += 1
    
    
    name = 'yuuka'
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(function, name)
    
    client_id = 202509100016
    interaction_event_id = 202410240001
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.application_command,
    )
    
    try:
        await embedded_activity_launch_command.invoke(client, interaction_event)
        
        vampytest.assert_eq(function_called, 1)
    finally:
        client._delete()
        client = None


def test__EmbeddedActivityLaunchCommand__copy():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.copy`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    show_for_invoking_user_only = True
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    embedded_activity_launch_command.error(exception_handler)
    copy = embedded_activity_launch_command.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, embedded_activity_launch_command)


def test__EmbeddedActivityLaunchCommand__target_type():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.target_type`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(function, name)
    
    output = embedded_activity_launch_command.target_type
    vampytest.assert_instance(output, ApplicationCommandTargetType)
    vampytest.assert_is(output, ApplicationCommandTargetType.embedded_activity_launch)


def test__EmbeddedActivityLaunchCommand__handler_type__with_function():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.handler_type`` works as intended.
    
    Case: with function.
    """
    async def function():
        pass
    
    name = 'yuuka'
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(function, name)
    
    output = embedded_activity_launch_command.handler_type
    vampytest.assert_instance(output, ApplicationCommandHandlerType)
    vampytest.assert_is(output, ApplicationCommandHandlerType.application)


def test__EmbeddedActivityLaunchCommand__handler_type__without_function():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.handler_type`` works as intended.
    
    Case: out function.
    """
    function = None
    
    name = 'yuuka'
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(function, name)
    
    output = embedded_activity_launch_command.handler_type
    vampytest.assert_instance(output, ApplicationCommandHandlerType)
    vampytest.assert_is(output, ApplicationCommandHandlerType.discord_embedded_activity_launcher)


def test__EmbeddedActivityLaunchCommand__get_command_function():
    """
    Tests whether ``EmbeddedActivityLaunchCommand.get_command_function`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    
    embedded_activity_launch_command = EmbeddedActivityLaunchCommand(function, name)
    
    output = embedded_activity_launch_command.get_command_function()
    vampytest.assert_instance(output, object)
    vampytest.assert_is(output, function)
