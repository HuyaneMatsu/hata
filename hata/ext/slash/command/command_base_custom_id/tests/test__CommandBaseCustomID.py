from re import compile as re_compile

import vampytest
from scarletio import WeakReferer

from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.events.handling_helpers import check_name
from ......discord.interaction import InteractionEvent

from ....converters import RegexMatcher, get_component_command_parameter_converters
from ....response_modifier import ResponseModifier

from ..helpers import _validate_custom_ids, split_and_check_satisfaction

from ..command_base_custom_id import CommandBaseCustomId


def _assert_fields_set(command_base_custom_id):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    command_base_custom_id : ``CommandBaseCustomId``
        The command to checkout.
    """
    vampytest.assert_instance(command_base_custom_id, CommandBaseCustomId)
    vampytest.assert_instance(command_base_custom_id._command_function, object)
    vampytest.assert_instance(command_base_custom_id._exception_handlers, list, nullable = True)
    vampytest.assert_instance(command_base_custom_id._keyword_parameter_converters, tuple)
    vampytest.assert_instance(command_base_custom_id._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(command_base_custom_id._positional_parameter_converters, tuple)
    vampytest.assert_instance(command_base_custom_id._regex_custom_ids, tuple, nullable = True)
    vampytest.assert_instance(command_base_custom_id._string_custom_ids, tuple, nullable = True)
    vampytest.assert_instance(command_base_custom_id.name, str)
    vampytest.assert_instance(command_base_custom_id.response_modifier, ResponseModifier, nullable = True)


class InstantiableCommandBaseCustomId(CommandBaseCustomId):
    __slots__ = ()
    
    def __new__(cls, function, name = None, *, custom_id = ..., **keyword_parameters):
        name = check_name(function, name)
        assert custom_id is not ...
        custom_id = _validate_custom_ids(custom_id)
        (
            command,
            positional_parameter_converters,
            keyword_parameter_converters,
        ) = get_component_command_parameter_converters(function)
        string_custom_ids, regex_custom_ids = split_and_check_satisfaction(custom_id, positional_parameter_converters)
        response_modifier = ResponseModifier(keyword_parameters)
        
        self = object.__new__(cls)
        self._command_function = function
        self._exception_handlers = None
        self._keyword_parameter_converters = keyword_parameter_converters
        self._parent_reference = None
        self._positional_parameter_converters = positional_parameter_converters
        self._regex_custom_ids = regex_custom_ids
        self._string_custom_ids = string_custom_ids
        self.name = name
        self.response_modifier = response_modifier
        return self


def test__CommandBaseCustomId__new():
    """
    Tests whether ``CommandBaseCustomId.__new__`` works as intended.
    """
    async def function():
        pass
    
    custom_id = re_compile('([a-z]+)_([a-z]+)')
    name = 'yuuka'
    
    with vampytest.assert_raises(NotImplementedError):
        CommandBaseCustomId(function, name, custom_id = custom_id)


def test__CommandBaseCustomId__repr():
    """
    Tests whether ``CommandBaseCustomId.__repr__`` works as intended.
    """
    async def function():
        pass
    
    custom_id_string = 'hey_mister'
    custom_id_regex = re_compile('([a-z]+)_([a-z]+)')
    custom_id = [
        custom_id_string,
        custom_id_regex,
    ]
    name = 'yuuka'
    show_for_invoking_user_only = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base_custom_id = InstantiableCommandBaseCustomId(
        function, name, custom_id = custom_id, show_for_invoking_user_only = True
    )
    command_base_custom_id.error(exception_handler)
    response_modifier = ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only})
    
    output = repr(command_base_custom_id)
    vampytest.assert_in(type(command_base_custom_id).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)
    vampytest.assert_in(f'string_custom_ids = {[custom_id_string]!r}', output)
    vampytest.assert_in(f'regex_custom_ids = {[RegexMatcher(custom_id_regex)]!r}', output)
    vampytest.assert_in(f'response_modifier = {response_modifier!r}', output)
    vampytest.assert_in(f'command_function = {function!r}', output)


def test__CommandBaseCustomId__hash():
    """
    Tests whether ``CommandBaseCustomId.__hash__`` works as intended.
    """
    async def function():
        pass
    
    custom_id_string = 'hey_mister'
    custom_id_regex = re_compile('([a-z]+)_([a-z]+)')
    custom_id = [
        custom_id_string,
        custom_id_regex,
    ]
    name = 'yuuka'
    show_for_invoking_user_only = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base_custom_id = InstantiableCommandBaseCustomId(
        function, name, custom_id = custom_id, show_for_invoking_user_only = show_for_invoking_user_only
    )
    command_base_custom_id.error(exception_handler)
    
    output = hash(command_base_custom_id)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    async def function_0():
        pass
    
    async def function_1():
        return 1
    
    custom_id_string = 'hey_mister'
    custom_id_regex = re_compile('([a-z]+)_([a-z]+)')
    custom_id = [
        custom_id_string,
        custom_id_regex,
    ]
    name = 'yuuka'
    show_for_invoking_user_only = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function_0,
        'name': name,
        'custom_id': custom_id,
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
            'custom_id': ['hey_sister'],
        },
        (),
        False,
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
            'show_for_invoking_user_only': not show_for_invoking_user_only,
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
def test__CommandBaseCustomId__eq(keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1):
    """
    Tests whether ``CommandBaseCustomId.__eq__`` works as intended.
    
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
    command_base_custom_id_0 = InstantiableCommandBaseCustomId(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        command_base_custom_id_0.error(exception_handler)
    
    command_base_custom_id_1 = InstantiableCommandBaseCustomId(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        command_base_custom_id_1.error(exception_handler)
    
    output = command_base_custom_id_0 == command_base_custom_id_1
    vampytest.assert_instance(output, bool)
    return output


async def test__CommandBaseCustomId__invoke():
    """
    Tests whether ``CommandBaseCustomId.invoke`` works as intended.
    
    This function is a coroutine.
    """
    async def function():
        pass
    
    name = 'yuuka'
    regex_match = None
    custom_id = ['hey_sister']
    
    command_base_custom_id = InstantiableCommandBaseCustomId(function, name, custom_id = custom_id)
    
    client_id = 202410200000
    interaction_event_id = 202410200001
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    try:
        await command_base_custom_id.invoke(client, interaction_event, regex_match)
        
    finally:
        client._delete()
        client = None


def test__CommandBaseCustomId__copy():
    """
    Tests whether ``CommandBaseCustomId.copy`` works as intended.
    """
    async def function():
        pass
    
    custom_id_string = 'hey_mister'
    custom_id_regex = re_compile('([a-z]+)_([a-z]+)')
    custom_id = [
        custom_id_string,
        custom_id_regex,
    ]
    name = 'yuuka'
    show_for_invoking_user_only = True
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base_custom_id = InstantiableCommandBaseCustomId(
        function, name, custom_id = custom_id, show_for_invoking_user_only = show_for_invoking_user_only
    )
    command_base_custom_id.error(exception_handler)
    copy = command_base_custom_id.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, command_base_custom_id)


def test__CommandBaseCustomId__get_command_function():
    """
    Tests whether ``CommandBaseCustomId.get_command_function`` works as intended.
    """
    async def function():
        pass
    
    custom_id = ['hey_mister']
    name = 'yuuka'
    
    command_base_custom_id = InstantiableCommandBaseCustomId(function, name, custom_id = custom_id)
    
    output = command_base_custom_id.get_command_function()
    vampytest.assert_is(output, function)
