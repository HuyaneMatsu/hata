import vampytest
from scarletio import WeakReferer

from ......discord.application import ApplicationIntegrationType
from ......discord.application_command import (
    ApplicationCommand, ApplicationCommandIntegrationContextType, ApplicationCommandOption,
    ApplicationCommandOptionType, ApplicationCommandPermissionOverwrite,
    ApplicationCommandPermissionOverwriteTargetType, ApplicationCommandTargetType
)
from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.interaction import (
    InteractionEvent, InteractionMetadataApplicationCommand, InteractionMetadataApplicationCommandAutocomplete,
    InteractionOption, InteractionResponseType, InteractionType
)
from ......discord.permission import Permission
from ......discord.user import ClientUserBase

from ....response_modifier import ResponseModifier
from ....utils import UNLOADING_BEHAVIOUR_DELETE

from ..slash_command import SlashCommand
from ..slash_command_category import SlashCommandCategory
from ..slash_command_function import SlashCommandFunction
from ..slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


def _assert_fields_set(slash_command):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    slash_command : ``SlashCommand``
        The command to checkout.
    """
    vampytest.assert_instance(slash_command, SlashCommand)
    vampytest.assert_instance(slash_command._auto_completers, list, nullable = True)
    vampytest.assert_instance(slash_command._command, object, nullable = True)
    vampytest.assert_instance(slash_command._exception_handlers, list, nullable = True)
    vampytest.assert_instance(slash_command._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(slash_command._permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(
        slash_command._registered_application_command_ids, dict, nullable = True,
    )
    vampytest.assert_instance(slash_command._schema, ApplicationCommand, nullable = True)
    vampytest.assert_instance(slash_command._unloading_behaviour, int)
    vampytest.assert_instance(slash_command.default, bool)
    vampytest.assert_instance(slash_command.description, str)
    vampytest.assert_instance(slash_command.global_, bool)
    vampytest.assert_instance(slash_command.guild_ids, set, nullable = True)
    vampytest.assert_instance(slash_command.integration_context_types, tuple, nullable = True)
    vampytest.assert_instance(slash_command.integration_types, tuple, nullable = True)
    vampytest.assert_instance(slash_command.name, str)
    vampytest.assert_instance(slash_command.nsfw, bool)
    vampytest.assert_instance(slash_command.required_permissions, Permission)


def test__SlashCommand__new():
    """
    Tests whether ``SlashCommand.__new__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    description = 'rember happy day'
    default = False
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
    show_for_invoking_user_only = True
    
    slash_command = SlashCommand(
        function,
        name,
        default = default,
        delete_on_unload = delete_on_unload,
        description = description,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
        show_for_invoking_user_only = show_for_invoking_user_only,
    )
    _assert_fields_set(slash_command)
    
    vampytest.assert_is_not(slash_command._command, None)
    vampytest.assert_is(slash_command._command._command_function, function)
    vampytest.assert_eq(slash_command._unloading_behaviour, UNLOADING_BEHAVIOUR_DELETE)
    vampytest.assert_eq(slash_command.description, description)
    vampytest.assert_eq(slash_command.default, default)
    vampytest.assert_eq(slash_command.global_, True)
    vampytest.assert_is(slash_command.guild_ids, None)
    vampytest.assert_eq(slash_command.integration_context_types, tuple(integration_context_types))
    vampytest.assert_eq(slash_command.integration_types, tuple(integration_types))
    vampytest.assert_eq(slash_command.name, name)
    vampytest.assert_eq(slash_command.nsfw, nsfw)
    vampytest.assert_eq(slash_command.required_permissions, required_permissions)
    vampytest.assert_eq(
        slash_command._command.response_modifier,
        ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only}),
    )


def test__SlashCommand__new__category():
    """
    Tests whether ``SlashCommand.__new__`` works as intended.
    
    Case: create category.
    """
    function = None
    name = 'yuuka'
    
    slash_command = SlashCommand(
        function,
        name,
    )
    
    vampytest.assert_is(slash_command._command, None)


def test__SlashCommand__repr():
    """
    Tests whether ``SlashCommand.__repr__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    delete_on_unload = True
    guild_id = 2024120434
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
    permission_overwrite = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 20241204305),
        True,
    )
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command = SlashCommand(
        function,
        name,
        default = default,
        delete_on_unload = delete_on_unload,
        description = description,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    slash_command.error(exception_handler)
    slash_command.add_permission_overwrite(guild_id, permission_overwrite)
    
    output = repr(slash_command)
    vampytest.assert_in(type(slash_command).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)
    vampytest.assert_in(f'type = global', output)
    vampytest.assert_in(f'unloading_behaviour = delete', output)
    vampytest.assert_in(f'integration_context_types = {tuple(integration_context_types)!r}', output)
    vampytest.assert_in(f'integration_types = {tuple(integration_types)!r}', output)
    vampytest.assert_in(f'nsfw = {nsfw!r}', output)
    vampytest.assert_in(f'required_permissions = {required_permissions!r}', output)
    vampytest.assert_in(f'default = {default!r}', output)
    vampytest.assert_in(f'description = {description!r}', output)
    vampytest.assert_in(f'command = {slash_command._command!r}', output)
    vampytest.assert_in(f'permission_overwrites = { {guild_id: [permission_overwrite]}!r}', output)


def test__SlashCommand__hash():
    """
    Tests whether ``SlashCommand.__hash__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    description = 'rember happy day'
    default = True
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
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command = SlashCommand(
        function,
        name,
        default = default,
        delete_on_unload = delete_on_unload,
        description = description,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    slash_command.error(exception_handler)
    
    output = hash(slash_command)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    async def function_0():
        pass
    
    async def function_1():
        pass
    
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    delete_on_unload = True
    guild = [202410260010, 202410260011]
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
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function_0,
        'name': name,
        'default': default,
        'delete_on_unload': delete_on_unload,
        'description': description,
        # 'guild': guild,
        'integration_context_types': integration_context_types,
        'integration_types': integration_types,
        'is_global': is_global,
        'nsfw': nsfw,
        'required_permissions': required_permissions,
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
            'default': False,
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
            'description': 'everything returns to null',
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
            'guild': [202410260013, 202410260014],
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
        keyword_parameters,
        (exception_handler,),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__SlashCommand__eq(keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1):
    """
    Tests whether ``SlashCommand.__eq__`` works as intended.
    
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
    slash_command_0 = SlashCommand(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        slash_command_0.error(exception_handler)
    
    slash_command_1 = SlashCommand(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        slash_command_1.error(exception_handler)
    
    output = slash_command_0 == slash_command_1
    vampytest.assert_instance(output, bool)
    return output


async def test__SlashCommand__invoke():
    """
    Tests whether ``SlashCommand.invoke`` works as intended.
    
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
    
    slash_command = SlashCommand(function, name)
    
    client_id = 202410260015
    interaction_event_id = 202410260016
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
        interaction = InteractionMetadataApplicationCommand(),
    )
    
    try:
        await slash_command.invoke(client, interaction_event)
        
        vampytest.assert_eq(function_called, 1)
    finally:
        client._delete()
        client = None



async def test__SlashCommand__invoke__subcommand():
    """
    Tests whether ``SlashCommand.invoke`` works as intended.
    
    This function is a coroutine.
    
    Case: sub-command.
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
    sub_command_name = 'wriggle'
    
    slash_command = SlashCommand(None, name)
    slash_command.interactions(function, sub_command_name)
    
    client_id = 202410260017
    interaction_event_id = 202410260018
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
        interaction = InteractionMetadataApplicationCommand(
            name = 'name',
            options = [
                InteractionOption(
                    name = sub_command_name,
                    option_type = ApplicationCommandOptionType.sub_command,
                    options = None,
                ),
            ],
        ),
    )
    
    try:
        await slash_command.invoke(client, interaction_event)
        
        vampytest.assert_eq(function_called, 1)
    finally:
        client._delete()
        client = None


def test__SlashCommand__copy():
    """
    Tests whether ``SlashCommand.copy`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    description = 'rember happy day'
    default = False
    delete_on_unload = True
    # guild = nONE
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
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command = SlashCommand(
        function,
        name,
        default = default,
        delete_on_unload = delete_on_unload,
        description = description,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    slash_command.error(exception_handler)
    copy = slash_command.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, slash_command)


def test__SlashCommand__target():
    """
    Tests whether ``SlashCommand.target`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command.target
    vampytest.assert_instance(output, ApplicationCommandTargetType)
    vampytest.assert_is(output, ApplicationCommandTargetType.chat)


def test__SlashCommand__get_command_function():
    """
    Tests whether ``SlashCommand.get_command_function`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command.get_command_function()
    vampytest.assert_instance(output, object)
    vampytest.assert_is(output, function)


# invoke_auto_completion -> ignore for now


def test__SlashCommand__as_sub_command__function():
    """
    Tests whether ``SlashCommand.as_sub_command`` works as intended.
    
    Case: function.
    """
    async def function():
        pass
    
    name = 'yuuka'
    deepness = 1
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command.as_sub_command(deepness)
    vampytest.assert_instance(output, SlashCommandFunction)
    vampytest.assert_is(output._command_function, function)
    vampytest.assert_eq(output.name, name)


def test__SlashCommand__as_sub_command__category():
    """
    Tests whether ``SlashCommand.as_sub_command`` works as intended.
    
    Case: category.
    """
    function = None
    name = 'yuuka'
    deepness = 1
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command.as_sub_command(deepness)
    vampytest.assert_instance(output, SlashCommandCategory)
    vampytest.assert_is(output._deepness, deepness)
    vampytest.assert_eq(output.name, name)


def test__SlashCommand__is_nestable__function():
    """
    Tests whether ``SlashCommand._is_nestable`` works as intended.
    
    Case: function.
    """
    async def function():
        pass
    
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command._is_nestable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__SlashCommand__is_nestable__category():
    """
    Tests whether ``SlashCommand._is_nestable`` works as intended.
    
    Case: category.
    """
    function = None
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command._is_nestable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__SlashCommand__create_event():
    """
    Tests whether ``SlashCommand.create_event`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    
    command_name = 'wriggle'
    
    output = slash_command.create_event(None, command_name)
    
    # since output function is `None`, we expected it to return `SlashCommandCategory`.
    vampytest.assert_instance(output, SlashCommandCategory)
    vampytest.assert_eq(output.name, command_name)
    vampytest.assert_eq(output._parent_reference, slash_command.get_self_reference())
    vampytest.assert_eq(output._deepness, 2)
    
    vampytest.assert_eq(
        slash_command._sub_commands,
        {
            command_name: output,
        },
    )


def test__SlashCommand__get_real_command_count__empty():
    """
    Tests whether ``SlashCommand.get_real_command_count`` works as intended.
    
    Case: Empty category.
    """
    function = None
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command.get_real_command_count()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)


def test__SlashCommand__get_real_command_count__command():
    """
    Tests whether ``SlashCommand.get_real_command_count`` works as intended.
    
    Case: Command..
    """
    async def function():
        return None
    
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    
    output = slash_command.get_real_command_count()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__SlashCommand__get_real_command_count__category():
    """
    Tests whether ``SlashCommand.get_real_command_count`` works as intended.
    
    Case: Category.
    """
    async def function():
        return None
    
    function = None
    name = 'yuuka'
    
    slash_command = SlashCommand(function, name)
    slash_command.create_event(None, 'wriggle').create_event(function, 'sekibanki')
    slash_command.create_event(None, 'chiruno').create_event(function, 'kagerou')
    
    output = slash_command.get_real_command_count()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)


def test__SlashCommand__get_schema__function():
    """
    Tests whether ``SlashCommand.get_schema`` works as intended.
    
    Case: function.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.    
    async def function(user : ClientUserBase):
        return None
    
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
    
    
    slash_command = SlashCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    
    output = slash_command.get_schema()
    vampytest.assert_instance(output, ApplicationCommand)
    vampytest.assert_eq(slash_command._schema, output)
    vampytest.assert_eq(
        output,
        ApplicationCommand(
            name,
            name,
            integration_context_types = integration_context_types,
            integration_types = integration_types,
            options = [
                ApplicationCommandOption(
                    name = 'user',
                    description = 'user',
                    option_type = ApplicationCommandOptionType.user,
                    required = True,
                ),
            ],
            nsfw = nsfw,
            required_permissions = required_permissions,
            target_type = ApplicationCommandTargetType.chat,
        )
    )


def test__SlashCommand__get_schema__category():
    """
    Tests whether ``SlashCommand.get_schema`` works as intended.
    
    Case: category.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.    
    async def function():
        return None
    
    name = 'yuuka'
    is_global = True
    
    slash_command = SlashCommand(
        None,
        name,
        is_global = is_global,
    )
    slash_command.create_event(None, 'wriggle').create_event(function, 'sekibanki')
    slash_command.create_event(None, 'chiruno').create_event(function, 'kagerou')
    
    output = slash_command.get_schema()
    vampytest.assert_instance(output, ApplicationCommand)
    vampytest.assert_eq(slash_command._schema, output)
    vampytest.assert_eq(
        output,
        ApplicationCommand(
            name,
            name,
            options = [
                ApplicationCommandOption(
                    name = 'chiruno',
                    description = 'chiruno',
                    option_type = ApplicationCommandOptionType.sub_command_group,
                    options = [
                        ApplicationCommandOption(
                            name = 'kagerou',
                            description = 'kagerou',
                            option_type = ApplicationCommandOptionType.sub_command,         
                        ),
                    ],
                ),
                ApplicationCommandOption(
                    name = 'wriggle',
                    description = 'wriggle',
                    option_type = ApplicationCommandOptionType.sub_command_group,
                    options = [
                        ApplicationCommandOption(
                            name = 'sekibanki',
                            description = 'sekibanki',
                            option_type = ApplicationCommandOptionType.sub_command,         
                        ),
                    ],
                ),
            ],
            target_type = ApplicationCommandTargetType.chat,
            integration_types = [ApplicationIntegrationType.guild_install],
        )
    )


def test__SlashCommand__autocomplete__command():
    """
    Tests whether ``SlashCommand.autocomplete`` works as intended.
    
    Case: command.
    """
    async def function(value : str):
        return None
    
    async def auto_complete_function(value):
        return None
    
    name = 'yuuka'
    
    slash_command = SlashCommand(
        function,
        name,
    )
    output = slash_command.autocomplete('value', function = auto_complete_function)
    vampytest.assert_instance(output, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(output._command_function, auto_complete_function)
    vampytest.assert_eq(output.name_pairs, frozenset((('value', 'value'),)))
    vampytest.assert_eq(output._parent_reference, slash_command._command.get_self_reference())
    vampytest.assert_eq(slash_command._command._auto_completers, [output])
    vampytest.assert_is(slash_command._command._parameter_converters[0].auto_completer, output)


def test__SlashCommand__autocomplete__category():
    """
    Tests whether ``SlashCommand.autocomplete`` works as intended.
    
    Case: category.
    """
    async def function(value : str):
        return None
    
    async def auto_complete_function(value):
        return None
    
    name = 'yuuka'
    
    slash_command = SlashCommand(
        None,
        name,
    )
    slash_command_function_0 = slash_command.create_event(function, 'kagerou')
    slash_command_function_1 = slash_command.create_event(function, 'wakasagihime')
    
    output = slash_command.autocomplete('value', function = auto_complete_function)
    vampytest.assert_instance(output, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(output._command_function, auto_complete_function)
    vampytest.assert_eq(output.name_pairs, frozenset((('value', 'value'),)))
    vampytest.assert_eq(output._parent_reference, slash_command.get_self_reference())
    vampytest.assert_eq(slash_command._auto_completers, [output])
    vampytest.assert_is(slash_command_function_0._parameter_converters[0].auto_completer, output)
    vampytest.assert_is(slash_command_function_1._parameter_converters[0].auto_completer, output)


def test__SlashCommand__try_resolve_auto_completer__no_match():
    """
    Tests whether ``SlashCommand._try_resolve_auto_completer`` works as intended.
    
    Case: no match.
    """
    async def auto_complete_function(value):
        return None
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        auto_complete_function, ['value'], 2, None,
    )
    
    name = 'yuuka'
    
    slash_command = SlashCommand(
        None,
        name,
    )
    
    output = slash_command._try_resolve_auto_completer(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    vampytest.assert_eq(slash_command._auto_completers, None)


def test__SlashCommand__try_resolve_auto_completer__with_match():
    """
    Tests whether ``SlashCommand._try_resolve_auto_completer`` works as intended.
    
    Case: with match.
    """
    async def function_0(hey : str, mister : str):
        return None
    
    async def function_1(hey : str, sister : str):
        return None
    
    async def auto_complete_function(value):
        return None
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        auto_complete_function, ['sister', 'mister'], 2, None,
    )
    
    name = 'yuuka'
    
    slash_command = SlashCommand(
        None,
        name,
    )
    
    # single nest
    slash_command_function_0 = slash_command.create_event(function_0, 'kagerou')
    # double nest
    slash_command_category = slash_command.create_event(None, 'yuyuko')
    slash_command_function_1 = slash_command_category.create_event(function_1, 'wakasagihime')
    
    output = slash_command._try_resolve_auto_completer(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    
    vampytest.assert_eq(slash_command._auto_completers, None)
    vampytest.assert_is(
        slash_command_function_0._parameter_converters[1].auto_completer, slash_command_parameter_auto_completer
    )
    vampytest.assert_is(
        slash_command_function_1._parameter_converters[1].auto_completer, slash_command_parameter_auto_completer
    )


async def test__SlashCommand__invoke_auto_completion():
    """
    Tests whether ``SlashCommand.invoke_auto_completion`` works as intended.
    
    This function is a coroutine.
    """
    client = None
    interaction_event = None
    func_called = 0
    request_made = 0
    value = 'hey sister'
    
    async def function(value : str):
        return
    
    
    async def auto_complete_function(input_client : Client, input_interaction_event : InteractionEvent, input_value):
        nonlocal client
        nonlocal interaction_event
        nonlocal value
        nonlocal func_called
        
        vampytest.assert_is_not(input_client, None)
        vampytest.assert_is_not(input_interaction_event, None)
        
        vampytest.assert_is(input_client, client)
        vampytest.assert_is(input_interaction_event, interaction_event)
        vampytest.assert_eq(input_value, value)
        
        func_called += 1
        return None
    
    
    name = 'yuuka'
    
    slash_command = SlashCommand(
        None,
        name,
    )
    slash_command_function = slash_command.create_event(function, 'kappa')
    slash_command_function.autocomplete('value', function = auto_complete_function)
    
    async def mock_interaction_response_message_create(
        input_interaction_id,
        input_interaction_token,
        input_data,
        query_string_parameters,
    ):
        nonlocal interaction_event_id
        nonlocal request_made
        nonlocal interaction_event_token
        
        vampytest.assert_eq(interaction_event_id, input_interaction_id)
        vampytest.assert_eq(interaction_event_token, input_interaction_token)
        vampytest.assert_eq(
            input_data,
            {
                'type': InteractionResponseType.application_command_autocomplete_result.value,
                'data': {
                    'choices': [],
                },
            },
        )
        request_made += 1
        return None
    
    client_id = 202410260040
    interaction_event_id = 202410260041
    interaction_event_token = 'hello hell'
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    api.interaction_response_message_create = mock_interaction_response_message_create
    
    auto_complete_option = InteractionMetadataApplicationCommandAutocomplete(
        options = [
            InteractionOption(
                option_type = ApplicationCommandOptionType.sub_command,
                name = 'kappa',
                options = [
                    InteractionOption(
                        focused = True,
                        name = 'value',
                        value = value,
                        option_type = ApplicationCommandOptionType.string,
                    ),
                ],
            ),
        ],
    )
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction = auto_complete_option,
        interaction_type = InteractionType.application_command_autocomplete,
        token = interaction_event_token,
    )
    
    try:
        await slash_command_function.invoke_auto_completion(client, interaction_event, auto_complete_option)
        
        vampytest.assert_eq(func_called, 1)
        vampytest.assert_eq(request_made, 1)
    finally:
        client._delete()
        client = None
