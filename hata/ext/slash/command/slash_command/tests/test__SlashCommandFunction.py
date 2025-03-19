import vampytest
from scarletio import WeakReferer

from ......discord.application_command import ApplicationCommandOption, ApplicationCommandOptionType
from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.interaction import (
    InteractionEvent, InteractionMetadataApplicationCommandAutocomplete, InteractionOption, InteractionResponseType,
    InteractionType
)

from ....converters import (
    ANNOTATION_TYPE_SELF_CLIENT, ANNOTATION_TYPE_SELF_INTERACTION_EVENT, ANNOTATION_TYPE_STR,
    ParameterConverterInternal, ParameterConverterSlashCommand, converter_self_client, converter_self_interaction_event,
    converter_str
)
from ....response_modifier import ResponseModifier
from ....utils import SYNC_ID_GLOBAL

from ..slash_command import SlashCommand
from ..slash_command_function import SlashCommandFunction
from ..slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


def _assert_fields_set(slash_command_function):
    """
    Asserts whether every fields are set of the given slash command function.
    
    Parameters
    ----------
    slash_command_function : ``SlashCommandFunction``
        The auto completer to check.
    """
    vampytest.assert_instance(slash_command_function, SlashCommandFunction)
    vampytest.assert_instance(slash_command_function._auto_completers, list, nullable = True)
    vampytest.assert_instance(slash_command_function._command_function, object)
    vampytest.assert_instance(slash_command_function._exception_handlers, list, nullable = True)
    vampytest.assert_instance(slash_command_function._parameter_converters, tuple)
    vampytest.assert_instance(slash_command_function._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(slash_command_function._self_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(slash_command_function.default, bool)
    vampytest.assert_instance(slash_command_function.description, str)
    vampytest.assert_instance(slash_command_function.name, str)
    vampytest.assert_instance(slash_command_function.response_modifier, ResponseModifier, nullable = True)


def test__SlashCommandFunction__new():
    """
    Tests whether ``SlashCommandFunction.__new__`` works as intended.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    _assert_fields_set(slash_command_function)
    
    vampytest.assert_is(slash_command_function._command_function, function)
    vampytest.assert_eq(slash_command_function._parameter_converters, parameter_converters)
    vampytest.assert_eq(slash_command_function.name, name)
    vampytest.assert_eq(slash_command_function.description, description)
    vampytest.assert_eq(slash_command_function.response_modifier, response_modifier)
    vampytest.assert_eq(slash_command_function.default, default)


def test__SlashCommandFunction__repr():
    """
    Tests whether ``SlashCommandFunction.__repr__`` works as intended.
    """
    async def function(pudding : str):
        return None
    
    parameter_converters = (
        ParameterConverterSlashCommand(
            'pudding',
            ANNOTATION_TYPE_STR,
            converter_str,
            'value',
            'value',
            False,
            True,
            None,
            None,
            None,
            None,
            None,
            None,
            0,
            0,
        ),
    )
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    async def auto_complete_function():
        pass
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    slash_command_function.error(exception_handler)
    auto_completer = slash_command_function.autocomplete('pudding', function = auto_complete_function)
    
    output = repr(slash_command_function)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(slash_command_function).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'description = {description!r}', output)
    vampytest.assert_in(f'default = {default!r}', output)
    vampytest.assert_in(f'response_modifier = {response_modifier!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)
    vampytest.assert_in(f'auto_completers = {[auto_completer]!r}', output)
    vampytest.assert_in(f'command_function = {function!r}', output)


def test__SlashCommandFunction__hash():
    """
    Tests whether ``SlashCommandFunction.__hash__`` works as intended.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    slash_command_function.error(exception_handler)
    
    output = hash(slash_command_function)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    async def function_0():
        return None
    
    async def function_1():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function_0,
        'parameter_converters': parameter_converters,
        'name': name,
        'description': description,
        'response_modifier': response_modifier,
        'default': default,
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
            'response_modifier': ResponseModifier({'show_for_invoking_user_only': False}),
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
def test__SlashCommandFunction__eq(
    keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1
):
    """
    Tests whether ``SlashCommandFunction.__eq__`` works as intended.
    
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
    slash_command_function_0 = SlashCommandFunction(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        slash_command_function_0.error(exception_handler)
    
    slash_command_function_1 = SlashCommandFunction(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        slash_command_function_1.error(exception_handler)
    
    output = slash_command_function_0 == slash_command_function_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__format():
    yield '', str
    yield 'm', SlashCommandFunction.mention.fget


@vampytest.call_from(_iter_options__format())
def test__SlashCommandFunction__format(code, equal_getter):
    """
    Tests whether ``SlashCommandFunction.__format__`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Format code.
    
    equal_getter : `FunctionType`
        A function to create something equal.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = format(slash_command_function, code)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, equal_getter(slash_command_function))


async def test__SlashCommandFunction__invoke():
    """
    Tests whether ``SlashCommandFunction.invoke`` works as intended.
    
    This function is a coroutine.
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
    
    parameter_converters = (
        ParameterConverterInternal(
            'input_client', ANNOTATION_TYPE_SELF_CLIENT, converter_self_client
        ),
        ParameterConverterInternal(
            'input_interaction_event', ANNOTATION_TYPE_SELF_INTERACTION_EVENT, converter_self_interaction_event
        )
    )
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    client_id = 202410250000
    interaction_event_id = 202410250001
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
        await slash_command_function.invoke(client, interaction_event, options)
        
        vampytest.assert_eq(func_called, 1)
    finally:
        client._delete()
        client = None


def test__SlashCommandFunction__get_command_function():
    """
    Tests whether ``SlashCommandFunction.get_command_function`` works as intended.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = slash_command_function.get_command_function()
    vampytest.assert_instance(output, object)
    vampytest.assert_is(output, function)


def test__SlashCommandFunction__error():
    """
    Tests whether ``SlashCommandFunction.error`` works as intended.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    slash_command_function.error(exception_handler)
    
    vampytest.assert_eq(slash_command_function._exception_handlers, [exception_handler])


def test__SlashCommandFunction__as_option():
    """
    Tests whether ``SlashCommandFunction.as_option`` works as intended.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = slash_command_function.as_option()
    vampytest.assert_instance(output, ApplicationCommandOption)
    vampytest.assert_eq(
        output,
        ApplicationCommandOption(
            name,
            description,
            ApplicationCommandOptionType.sub_command,
            options = None,
            default = default,
        )
    )


def test__SlashCommandFunction__mention__no_parent():
    """
    Tests whether ``SlashCommandFunction.mention`` works as intended.
    
    Case: no parent.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = slash_command_function.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'')


def test__SlashCommandFunction__mention__no_sync():
    """
    Tests whether ``SlashCommandFunction.mention`` works as intended.
    
    Case: no sync.
    """
    async def function():
        return None
    
    parent_name = 'kazami'
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    parent = SlashCommand(None, parent_name, is_global = True)
    slash_command_function._parent_reference = parent.get_self_reference()
    
    output = slash_command_function.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'/{parent_name!s} {name!s}')


def test__SlashCommandFunction__mention__sync_global():
    """
    Tests whether ``SlashCommandFunction.mention`` works as intended.
    
    Case: synced global.
    """
    async def function():
        return None
    
    parent_name = 'kazami'
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    application_command_id = 202410250002
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    parent = SlashCommand(None, parent_name, is_global = True)
    parent._register_guild_and_application_command_id(SYNC_ID_GLOBAL, application_command_id)
    slash_command_function._parent_reference = parent.get_self_reference()
    
    output = slash_command_function.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'</{parent_name!s} {name!s}:{application_command_id!s}>')


def test__SlashCommandFunction__mention_at__no_parent():
    """
    Tests whether ``SlashCommandFunction.mention_at`` works as intended.
    
    Case: no parent.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    guild_id = 202410250002
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = slash_command_function.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'')


def test__SlashCommandFunction__mention_at__no_sync():
    """
    Tests whether ``SlashCommandFunction.mention_at`` works as intended.
    
    Case: no sync.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    parent_name = 'kazami'
    guild_id = 202410250003
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    parent = SlashCommand(None, parent_name, guild = guild_id)
    slash_command_function._parent_reference = parent.get_self_reference()
    
    output = slash_command_function.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'/{parent_name!s} {name!s}')


def test__SlashCommandFunction__mention_at__sync_guild():
    """
    Tests whether ``SlashCommandFunction.mention_at`` works as intended.
    
    Case: synced guild.
    """
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = ResponseModifier({'show_for_invoking_user_only': True})
    default = True
    parent_name = 'kazami'
    guild_id = 202410250004
    application_command_id = 202410250005
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    parent = SlashCommand(None, parent_name, guild = guild_id)
    parent._register_guild_and_application_command_id(guild_id, application_command_id)
    slash_command_function._parent_reference = parent.get_self_reference()
    
    output = slash_command_function.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'</{parent_name!s} {name!s}:{application_command_id!s}>')


def test__SlashCommandFunction__autocomplete():
    """
    Tests whether ``SlashCommandFunction.autocomplete`` works as intended.
    """
    async def function(value : str):
        return None
    
    async def auto_complete_function(value):
        return None
    
    parameter_converter = ParameterConverterSlashCommand(
        'value',
        ANNOTATION_TYPE_STR,
        converter_str,
        'value',
        'value',
        False,
        True,
        None,
        None,
        None,
        None,
        None,
        None,
        0,
        0,
    )
    
    parameter_converters = (parameter_converter,)
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = None
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = slash_command_function.autocomplete('value', function = auto_complete_function)
    vampytest.assert_instance(output, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(output._command_function, auto_complete_function)
    vampytest.assert_eq(output.name_pairs, frozenset((('value', 'value'),)))
    vampytest.assert_eq(output._parent_reference, slash_command_function.get_self_reference())
    vampytest.assert_eq(slash_command_function._auto_completers, [output])
    vampytest.assert_is(parameter_converter.auto_completer, output)


def test__SlashCommandFunction__try_resolve_auto_completer__no_match():
    """
    Tests whether ``SlashCommandFunction._try_resolve_auto_completer`` works as intended.
    
    Case: no match.
    """
    async def function():
        return None
    
    async def auto_complete_function(value):
        return None
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        auto_complete_function, ['value'], 2, None,
    )
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = None
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = slash_command_function._try_resolve_auto_completer(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    vampytest.assert_eq(slash_command_function._auto_completers, None)


def test__SlashCommandFunction__try_resolve_auto_completer__with_match():
    """
    Tests whether ``SlashCommandFunction._try_resolve_auto_completer`` works as intended.
    
    Case: with match.
    """
    async def function(hey : str, mister : str, sister : str):
        return None
    
    async def auto_complete_function(value):
        return None
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        auto_complete_function, ['sister', 'mister'], 2, None,
    )
    
    parameter_converter_0, parameter_converter_1, parameter_converter_2 = (
        ParameterConverterSlashCommand(
            parameter_name,
            ANNOTATION_TYPE_STR,
            converter_str,
            parameter_name,
            parameter_name,
            False,
            True,
            None,
            None,
            None,
            None,
            None,
            None,
            0,
            0,
        )
        for parameter_name in
        ('hey', 'sister', 'mister')
    )
    
    parameter_converters = (
        parameter_converter_0,
        parameter_converter_1,
        parameter_converter_2,
    )
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = None
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    output = slash_command_function._try_resolve_auto_completer(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    
    vampytest.assert_eq(slash_command_function._auto_completers, None)
    vampytest.assert_is(parameter_converter_1.auto_completer, slash_command_parameter_auto_completer)
    vampytest.assert_is(parameter_converter_2.auto_completer, slash_command_parameter_auto_completer)


async def test__SlashCommandFunction__invoke_auto_completion():
    """
    Tests whether ``SlashCommandFunction.invoke_auto_completion`` works as intended.
    
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
    
    parameter_converter = ParameterConverterSlashCommand(
        'value',
        ANNOTATION_TYPE_STR,
        converter_str,
        'value',
        'value',
        False,
        True,
        None,
        None,
        None,
        None,
        None,
        None,
        0,
        0,
    )
    
    parameter_converters = (parameter_converter,)
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = None
    default = True
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
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
    
    client_id = 202410260020
    interaction_event_id = 202410260021
    interaction_event_token = 'hello hell'
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    api.interaction_response_message_create = mock_interaction_response_message_create
    
    auto_complete_option = InteractionMetadataApplicationCommandAutocomplete(
        options = [
            InteractionOption(
                focused = True,
                name = 'value',
                value = value,
                option_type = ApplicationCommandOptionType.string,
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
