from re import compile as re_compile

import vampytest
from scarletio import WeakReferer

from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.interaction import InteractionEvent

from ....converters import RegexMatcher
from ....parameter_converters.base import ParameterConverterBase
from ....response_modifier import ResponseModifier

from ..form_submit_command import FormSubmitCommand


def _assert_fields_set(form_submit_command):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    form_submit_command : ``FormSubmitCommand``
        The command to checkout.
    """
    vampytest.assert_instance(form_submit_command, FormSubmitCommand)
    vampytest.assert_instance(form_submit_command._command_function, object)
    vampytest.assert_instance(form_submit_command._exception_handlers, list, nullable = True)
    vampytest.assert_instance(form_submit_command._parameter_converters, tuple)
    vampytest.assert_instance(form_submit_command._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(form_submit_command._regex_custom_ids, tuple, nullable = True)
    vampytest.assert_instance(form_submit_command._string_custom_ids, tuple, nullable = True)
    vampytest.assert_instance(form_submit_command.name, str)
    vampytest.assert_instance(form_submit_command.response_modifier, ResponseModifier, nullable = True)
    vampytest.assert_instance(form_submit_command._keyword_parameter_converters, tuple)
    vampytest.assert_instance(form_submit_command._multi_parameter_converter, ParameterConverterBase, nullable = True)


def test__FormSubmitCommand__new():
    """
    Tests whether ``FormSubmitCommand.__new__`` works as intended.
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
    
    form_submit_command = FormSubmitCommand(
        function, name, custom_id = custom_id, show_for_invoking_user_only = show_for_invoking_user_only
    )
    form_submit_command.error(exception_handler)
    _assert_fields_set(form_submit_command)
    
    vampytest.assert_is(form_submit_command._command_function, function)
    vampytest.assert_eq(form_submit_command.name, name)
    vampytest.assert_eq(form_submit_command._exception_handlers, [exception_handler])
    vampytest.assert_eq(form_submit_command._string_custom_ids, (custom_id_string,))
    vampytest.assert_eq(form_submit_command._regex_custom_ids, (RegexMatcher(custom_id_regex),))
    vampytest.assert_eq(
        form_submit_command.response_modifier,
        ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only}),
    )


async def test__FormSubmitCommand__invoke():
    """
    Tests whether ``FormSubmitCommand.invoke`` works as intended.
    
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
    
    
    name = 'yuuka'
    regex_match = None
    custom_id = ['hey_sister']
    
    form_submit_command = FormSubmitCommand(function, name, custom_id = custom_id)
    
    client_id = 202410200004
    interaction_event_id = 202410200005
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    try:
        await form_submit_command.invoke(client, interaction_event, regex_match)
        
        vampytest.assert_eq(func_called, 1)
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
    
    form_submit_command = FormSubmitCommand(
        function, name, custom_id = custom_id, show_for_invoking_user_only = show_for_invoking_user_only
    )
    form_submit_command.error(exception_handler)
    copy = form_submit_command.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, form_submit_command)
