import vampytest
from scarletio import WeakReferer

from ......discord.application import ApplicationIntegrationType
from ......discord.application_command import (
    ApplicationCommand, ApplicationCommandIntegrationContextType, ApplicationCommandTargetType
)
from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.interaction import (
    InteractionEvent, InteractionMetadataApplicationCommand, InteractionType, Resolved
)
from ......discord.permission import Permission
from ......discord.user import ClientUserBase, User

from ....response_modifier import ResponseModifier
from ....utils import UNLOADING_BEHAVIOUR_DELETE

from ..context_command import ContextCommand


def _assert_fields_set(context_command):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    context_command : ``ContextCommand``
        The command to checkout.
    """
    vampytest.assert_instance(context_command, ContextCommand)
    vampytest.assert_instance(context_command._exception_handlers, list, nullable = True)
    vampytest.assert_instance(context_command._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(context_command.name, str)
    vampytest.assert_instance(context_command._permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(
        context_command._registered_application_command_ids, dict, nullable = True,
    )
    vampytest.assert_instance(context_command._schema, ApplicationCommand, nullable = True)
    vampytest.assert_instance(context_command._unloading_behaviour, int)
    
    vampytest.assert_instance(context_command.global_, bool)
    vampytest.assert_instance(context_command.guild_ids, set, nullable = True)
    vampytest.assert_instance(context_command.integration_context_types, tuple, nullable = True)
    vampytest.assert_instance(context_command.integration_types, tuple, nullable = True)
    vampytest.assert_instance(context_command.nsfw, bool)
    vampytest.assert_instance(context_command.required_permissions, Permission)
    vampytest.assert_instance(context_command.response_modifier, ResponseModifier, nullable = True)
    vampytest.assert_instance(context_command.target, ApplicationCommandTargetType)


def test__ContextCommand__new():
    """
    Tests whether ``ContextCommand.__new__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
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
    target = ApplicationCommandTargetType.user
    show_for_invoking_user_only = True
    
    context_command = ContextCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        target = target,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    _assert_fields_set(context_command)
    
    vampytest.assert_is(context_command._command_function, function)
    vampytest.assert_eq(context_command._unloading_behaviour, UNLOADING_BEHAVIOUR_DELETE)
    vampytest.assert_eq(context_command.global_, True)
    vampytest.assert_is(context_command.guild_ids, None)
    vampytest.assert_eq(context_command.integration_context_types, tuple(integration_context_types))
    vampytest.assert_eq(context_command.integration_types, tuple(integration_types))
    vampytest.assert_eq(context_command.name, name)
    vampytest.assert_eq(context_command.nsfw, nsfw)
    vampytest.assert_eq(context_command.required_permissions, required_permissions)
    vampytest.assert_eq(
        context_command.response_modifier,
        ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only}),
    )
    vampytest.assert_is(context_command.target, target)


def test__ContextCommand__repr():
    """
    Tests whether ``ContextCommand.__repr__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
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
    target = ApplicationCommandTargetType.user
    show_for_invoking_user_only = True
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    context_command = ContextCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        target = target,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    context_command.error(exception_handler)
    response_modifier = ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only})
    
    output = repr(context_command)
    vampytest.assert_in(type(context_command).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)
    vampytest.assert_in(f'type = global', output)
    vampytest.assert_in(f'unloading_behaviour = delete', output)
    vampytest.assert_in(f'integration_context_types = {tuple(integration_context_types)!r}', output)
    vampytest.assert_in(f'integration_types = {tuple(integration_types)!r}', output)
    vampytest.assert_in(f'nsfw = {nsfw!r}', output)
    vampytest.assert_in(f'required_permissions = {required_permissions!r}', output)
    vampytest.assert_in(f'target = {target.name!s}', output)
    vampytest.assert_in(f'response_modifier = {response_modifier!r}', output)


def test__ContextCommand__hash():
    """
    Tests whether ``ContextCommand.__hash__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
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
    target = ApplicationCommandTargetType.user
    show_for_invoking_user_only = True
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    context_command = ContextCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        target = target,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    context_command.error(exception_handler)
    
    output = hash(context_command)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    async def function_0():
        pass
    
    async def function_1():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    guild = [202410240003, 202410240004]
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
    target = ApplicationCommandTargetType.user
    show_for_invoking_user_only = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function_0,
        'name': name,
        'delete_on_unload': delete_on_unload,
        # 'guild': guild,
        'integration_context_types': integration_context_types,
        'integration_types': integration_types,
        'is_global': is_global,
        'nsfw': nsfw,
        'required_permissions': required_permissions,
        'target': target,
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
            'is_global': False,
        },
        (),
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'is_global': ...,
            'guild': guild,
        },
        (),
        {
            **keyword_parameters,
            'is_global': ...,
            'guild': [202410240005, 202410240006],
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
            'target': ApplicationCommandTargetType.message,
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
def test__ContextCommand__eq(keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1):
    """
    Tests whether ``ContextCommand.__eq__`` works as intended.
    
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
    context_command_0 = ContextCommand(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        context_command_0.error(exception_handler)
    
    context_command_1 = ContextCommand(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        context_command_1.error(exception_handler)
    
    output = context_command_0 == context_command_1
    vampytest.assert_instance(output, bool)
    return output


async def test__ContextCommand__invoke():
    """
    Tests whether ``ContextCommand.invoke`` works as intended.
    
    This function is a coroutine.
    """
    client = None
    interaction_event = None
    function_called = 0
    
    async def function(input_client : Client, input_interaction_event : InteractionEvent, target : ClientUserBase):
        nonlocal client
        nonlocal interaction_event
        nonlocal user
        nonlocal function_called
        
        vampytest.assert_is_not(input_client, None)
        vampytest.assert_is_not(input_interaction_event, None)
        
        vampytest.assert_is(input_client, client)
        vampytest.assert_is(input_interaction_event, interaction_event)
        vampytest.assert_is(target, user)
        
        function_called += 1
    
    
    name = 'yuuka'
    target = ApplicationCommandTargetType.user
    
    context_command = ContextCommand(function, name, target = target)
    
    client_id = 202410240000
    interaction_event_id = 202410240001
    user_id = 202410240002
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    user = User.precreate(user_id)
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.application_command,
        interaction = InteractionMetadataApplicationCommand(
            target_id = user_id,
            resolved = Resolved(users = {user_id: user}),
        ),
    )
    
    try:
        await context_command.invoke(client, interaction_event)
        
        vampytest.assert_eq(function_called, 1)
    finally:
        client._delete()
        client = None


def test__ContextCommand__copy():
    """
    Tests whether ``ContextCommand.copy`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
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
    target = ApplicationCommandTargetType.user
    show_for_invoking_user_only = True
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    context_command = ContextCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        target = target,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    context_command.error(exception_handler)
    copy = context_command.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, context_command)


def test__ContextCommand__get_command_function():
    """
    Tests whether ``ContextCommand.get_command_function`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    target = ApplicationCommandTargetType.user
    
    context_command = ContextCommand(function, name, target = target)
    
    output = context_command.get_command_function()
    vampytest.assert_instance(output, object)
    vampytest.assert_is(output, function)
