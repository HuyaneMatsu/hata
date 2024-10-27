import vampytest
from scarletio import WeakReferer

from ......discord.application_command import ApplicationCommandOption, ApplicationCommandOptionType
from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.interaction import (
    InteractionEvent, InteractionMetadataApplicationCommand, InteractionMetadataApplicationCommandAutocomplete,
    InteractionOption, InteractionResponseType, InteractionType
)

from ....converters import (
    ANNOTATION_TYPE_SELF_CLIENT, ANNOTATION_TYPE_SELF_INTERACTION_EVENT, InternalParameterConverter,
    converter_self_client, converter_self_interaction_event
)
from ....utils import SYNC_ID_GLOBAL

from ..slash_command import SlashCommand
from ..slash_command_category import SlashCommandCategory
from ..slash_command_function import SlashCommandFunction
from ..slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


def _assert_fields_set(slash_command_category):
    """
    Asserts whether every fields are set of the given slash command function.
    
    Parameters
    ----------
    slash_command_category : ``SlashCommandCategory``
        The auto completer to check.
    """
    vampytest.assert_instance(slash_command_category, SlashCommandCategory)
    vampytest.assert_instance(slash_command_category._auto_completers, list, nullable = True)
    vampytest.assert_instance(slash_command_category._exception_handlers, list, nullable = True)
    vampytest.assert_instance(slash_command_category._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(slash_command_category._self_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(slash_command_category._sub_commands, dict, nullable = True)
    vampytest.assert_instance(slash_command_category.default, bool)
    vampytest.assert_instance(slash_command_category.description, str)
    vampytest.assert_instance(slash_command_category.name, str)


def test__SlashCommandCategory__new():
    """
    Tests whether ``SlashCommandCategory.__new__`` works as intended.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    _assert_fields_set(slash_command_category)
    
    vampytest.assert_eq(slash_command_category.name, name)
    vampytest.assert_eq(slash_command_category.description, description)
    vampytest.assert_eq(slash_command_category.default, default)
    vampytest.assert_eq(slash_command_category._deepness, deepness)


def test__SlashCommandCategory__repr():
    """
    Tests whether ``SlashCommandCategory.__repr__`` works as intended.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    slash_command_category.error(exception_handler)
    
    output = repr(slash_command_category)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(slash_command_category).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'description = {description!r}', output)
    vampytest.assert_in(f'default = {default!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)


def test__SlashCommandCategory__hash():
    """
    Tests whether ``SlashCommandCategory.__hash__`` works as intended.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    slash_command_category.error(exception_handler)
    
    output = hash(slash_command_category)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'name': name,
        'description': description,
        'default': default,
        'deepness': deepness,
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
            'default': False,
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
def test__SlashCommandCategory__eq(
    keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1
):
    """
    Tests whether ``SlashCommandCategory.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_0 : `tuple<CoroutineCategoryType>`
        Exception handlers to register to the instance.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_1 : `tuple<CoroutineCategoryType>`
        Exception handlers to register to the instance.
    
    Returns
    -------
    output : `bool`
    """
    slash_command_category_0 = SlashCommandCategory(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        slash_command_category_0.error(exception_handler)
    
    slash_command_category_1 = SlashCommandCategory(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        slash_command_category_1.error(exception_handler)
    
    output = slash_command_category_0 == slash_command_category_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__format():
    yield '', str
    yield 'm', SlashCommandCategory.mention.fget


@vampytest.call_from(_iter_options__format())
def test__SlashCommandCategory__format(code, equal_getter):
    """
    Tests whether ``SlashCommandCategory.__format__`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Format code.
    
    equal_getter : `CategoryType`
        A function to create something equal.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    output = format(slash_command_category, code)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, equal_getter(slash_command_category))


async def test__SlashCommandCategory__invoke__no_sub_command():
    """
    Tests whether ``SlashCommandCategory.invoke`` works as intended.
    
    This function is a coroutine.
    
    Case: no sub-command.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    client_id = 202410260000
    interaction_event_id = 202410260001
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    options = None
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    try:
        await slash_command_category.invoke(client, interaction_event, options)
    finally:
        client._delete()
        client = None


async def test__SlashCommandCategory__invoke__with_sub_command():
    """
    Tests whether ``SlashCommandCategory.invoke`` works as intended.
    
    This function is a coroutine.
    
    Case: with sub command.
    """
    client = None
    interaction_event = None
    func_called = 0
    
    async def function(input_client : Client, input_interaction_event : InteractionEvent):
        nonlocal client
        nonlocal interaction_event
        nonlocal func_called
        
        vampytest.assert_is_not(input_client, None)
        vampytest.assert_is_not(input_interaction_event, None)
        
        vampytest.assert_is(input_client, client)
        vampytest.assert_is(input_interaction_event, interaction_event)
        
        func_called += 1
    
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    parameter_converters = (
        InternalParameterConverter(
            'input_client', ANNOTATION_TYPE_SELF_CLIENT, converter_self_client
        ),
        InternalParameterConverter(
            'input_interaction_event', ANNOTATION_TYPE_SELF_INTERACTION_EVENT, converter_self_interaction_event
        )
    )
    response_modifier = None
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    slash_command_category._sub_commands = {slash_command_function.name: slash_command_function}
    
    client_id = 202410260002
    interaction_event_id = 202410260003
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    options = [
        InteractionOption(
            name = slash_command_function.name,
            option_type = ApplicationCommandOptionType.sub_command,
            options = None,
        )
    ]
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.application_command,
        interaction = InteractionMetadataApplicationCommand(
            name = slash_command_category.name,
            options = options,
        )
    )
    
    try:
        await slash_command_category.invoke(client, interaction_event, options)
        
        vampytest.assert_eq(func_called, 1)
    finally:
        client._delete()
        client = None


def test__SlashCommandCategory__create_event():
    """
    Tests whether ``SlashCommandCategory.create_event`` works as intended.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 1
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    command_name = 'wriggle'
    
    output = slash_command_category.create_event(None, command_name)
    
    # since output function is `None`, we expected it to return `SlashCommandCategory`.
    vampytest.assert_instance(output, SlashCommandCategory)
    vampytest.assert_eq(output.name, command_name)
    vampytest.assert_eq(output._parent_reference, slash_command_category.get_self_reference())
    vampytest.assert_eq(output._deepness, deepness + 1)
    
    vampytest.assert_eq(
        slash_command_category._sub_commands,
        {
            command_name: output,
        },
    )


def test__SlashCommandCategory__error():
    """
    Tests whether ``SlashCommandCategory.error`` works as intended.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    slash_command_category.error(exception_handler)
    
    vampytest.assert_eq(slash_command_category._exception_handlers, [exception_handler])


def test__SlashCommandCategory__as_option():
    """
    Tests whether ``SlashCommandCategory.as_option`` works as intended.
    """
    async def function():
        return None
    
    name = 'yuuka'
    description = 'rember happy day'
    default = False
    deepness = 2
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    slash_command_category.create_event(function, 'sekibanki')
    slash_command_category.create_event(function, 'kagerou')
    
    output = slash_command_category.as_option()
    vampytest.assert_instance(output, ApplicationCommandOption)
    vampytest.assert_eq(
        output,
        ApplicationCommandOption(
            name,
            description,
            ApplicationCommandOptionType.sub_command_group,
            default = default,
            options = [
                ApplicationCommandOption(
                    name = 'kagerou',
                    description = 'kagerou',
                    option_type = ApplicationCommandOptionType.sub_command,         
                ),
                ApplicationCommandOption(
                    name = 'sekibanki',
                    description = 'sekibanki',
                    option_type = ApplicationCommandOptionType.sub_command,         
                ),
            ],
        )
    )


def test__SlashCommandCategory__mention__no_parent():
    """
    Tests whether ``SlashCommandCategory.mention`` works as intended.
    
    Case: no parent.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    output = slash_command_category.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'')


def test__SlashCommandCategory__mention__no_sync():
    """
    Tests whether ``SlashCommandCategory.mention`` works as intended.
    
    Case: no sync.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    parent_name = 'kazami'
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    parent = SlashCommand(None, parent_name, is_global = True)
    slash_command_category._parent_reference = parent.get_self_reference()
    
    output = slash_command_category.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'/{parent_name!s} {name!s}')


def test__SlashCommandCategory__mention__sync_global():
    """
    Tests whether ``SlashCommandCategory.mention`` works as intended.
    
    Case: synced global.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    parent_name = 'kazami'
    application_command_id = 202410260004
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    parent = SlashCommand(None, parent_name, is_global = True)
    parent._register_guild_and_application_command_id(SYNC_ID_GLOBAL, application_command_id)
    slash_command_category._parent_reference = parent.get_self_reference()
    
    output = slash_command_category.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'</{parent_name!s} {name!s}:{application_command_id!s}>')


def test__SlashCommandCategory__mention_at__no_parent():
    """
    Tests whether ``SlashCommandCategory.mention_at`` works as intended.
    
    Case: no parent.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    guild_id = 202410260005
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    output = slash_command_category.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'')


def test__SlashCommandCategory__mention_at__no_sync():
    """
    Tests whether ``SlashCommandCategory.mention_at`` works as intended.
    
    Case: no sync.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    parent_name = 'kazami'
    guild_id = 202410260006
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    parent = SlashCommand(None, parent_name, guild = guild_id)
    slash_command_category._parent_reference = parent.get_self_reference()
    
    output = slash_command_category.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'/{parent_name!s} {name!s}')


def test__SlashCommandCategory__mention_at__sync_guild():
    """
    Tests whether ``SlashCommandCategory.mention_at`` works as intended.
    
    Case: synced guild.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    parent_name = 'kazami'
    guild_id = 202410260007
    application_command_id = 202410260008
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    parent = SlashCommand(None, parent_name, guild = guild_id)
    parent._register_guild_and_application_command_id(guild_id, application_command_id)
    slash_command_category._parent_reference = parent.get_self_reference()
    
    output = slash_command_category.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'</{parent_name!s} {name!s}:{application_command_id!s}>')


def test__SlashCommandCategory__is_nestable__category():
    """
    Tests whether ``SlashCommandCategory._is_nestable`` works as intended.
    
    Case: category.
    """
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 2
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    output = slash_command_category._is_nestable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__SlashCommandCategory__autocomplete():
    """
    Tests whether ``SlashCommandCategory.autocomplete`` works as intended.
    """
    async def function(value : str):
        return None
    
    async def auto_complete_function(value):
        return None
    
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 1
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    slash_command_function_0 = slash_command_category.create_event(function, 'kagerou')
    slash_command_function_1 = slash_command_category.create_event(function, 'wakasagihime')
    
    output = slash_command_category.autocomplete('value', function = auto_complete_function)
    vampytest.assert_instance(output, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(output._command_function, auto_complete_function)
    vampytest.assert_eq(output.name_pairs, frozenset((('value', 'value'),)))
    vampytest.assert_eq(output._parent_reference, slash_command_category.get_self_reference())
    vampytest.assert_eq(slash_command_category._auto_completers, [output])
    vampytest.assert_is(slash_command_function_0._parameter_converters[0].auto_completer, output)
    vampytest.assert_is(slash_command_function_1._parameter_converters[0].auto_completer, output)


def test__SlashCommandCategory__try_resolve_auto_completer__no_match():
    """
    Tests whether ``SlashCommandCategory._try_resolve_auto_completer`` works as intended.
    
    Case: no match.
    """
    async def auto_complete_function(value):
        return None
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        auto_complete_function, ['value'], 2, None,
    )
    
    name = 'yuuka'
    description = 'rember happy day'
    default = True
    deepness = 1
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    
    output = slash_command_category._try_resolve_auto_completer(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    vampytest.assert_eq(slash_command_category._auto_completers, None)


def test__SlashCommandCategory__try_resolve_auto_completer__with_match():
    """
    Tests whether ``SlashCommandCategory._try_resolve_auto_completer`` works as intended.
    
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
    description = 'rember happy day'
    default = True
    deepness = 1
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    slash_command_function_0 = slash_command_category.create_event(function_0, 'kagerou')
    slash_command_function_1 = slash_command_category.create_event(function_1, 'wakasagihime')
    
    output = slash_command_category._try_resolve_auto_completer(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    
    vampytest.assert_eq(slash_command_category._auto_completers, None)
    vampytest.assert_is(
        slash_command_function_0._parameter_converters[1].auto_completer, slash_command_parameter_auto_completer
    )
    vampytest.assert_is(
        slash_command_function_1._parameter_converters[1].auto_completer, slash_command_parameter_auto_completer
    )


async def test__SlashCommandCategory__invoke_auto_completion():
    """
    Tests whether ``SlashCommandCategory.invoke_auto_completion`` works as intended.
    
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
    description = 'rember happy day'
    default = True
    deepness = 1
    
    slash_command_category = SlashCommandCategory(
        name, description, default, deepness
    )
    slash_command_function = slash_command_category.create_event(function, 'kappa')
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
    
    client_id = 202410260030
    interaction_event_id = 202410260031
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
