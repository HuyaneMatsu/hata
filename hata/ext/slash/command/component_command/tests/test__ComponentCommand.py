from re import compile as re_compile

import vampytest
from scarletio import WeakReferer

from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.events.handling_helpers import check_name
from ......discord.interaction import InteractionEvent

from ....converters import RegexMatcher
from ....response_modifier import ResponseModifier

from ..component_command import ComponentCommand


def _assert_fields_set(component_command):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    component_command : ``ComponentCommand``
        The command to checkout.
    """
    vampytest.assert_instance(component_command, ComponentCommand)
    vampytest.assert_instance(component_command._command_function, object)
    vampytest.assert_instance(component_command._exception_handlers, list, nullable = True)
    vampytest.assert_instance(component_command._keyword_parameter_converters, tuple)
    vampytest.assert_instance(component_command._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(component_command._positional_parameter_converters, tuple)
    vampytest.assert_instance(component_command._regex_custom_ids, tuple, nullable = True)
    vampytest.assert_instance(component_command._string_custom_ids, tuple, nullable = True)
    vampytest.assert_instance(component_command.name, str)
    vampytest.assert_instance(component_command.response_modifier, ResponseModifier, nullable = True)


def test__ComponentCommand__new():
    """
    Tests whether ``ComponentCommand.__new__`` works as intended.
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
    
    component_command = ComponentCommand(
        function, name, custom_id = custom_id, show_for_invoking_user_only = show_for_invoking_user_only
    )
    component_command.error(exception_handler)
    _assert_fields_set(component_command)
    
    vampytest.assert_is(component_command._command_function, function)
    vampytest.assert_eq(component_command.name, name)
    vampytest.assert_eq(component_command._exception_handlers, [exception_handler])
    vampytest.assert_eq(component_command._string_custom_ids, (custom_id_string,))
    vampytest.assert_eq(component_command._regex_custom_ids, (RegexMatcher(custom_id_regex),))
    vampytest.assert_eq(
        component_command.response_modifier,
        ResponseModifier({'show_for_invoking_user_only': show_for_invoking_user_only}),
    )


async def test__ComponentCommand__invoke():
    """
    Tests whether ``ComponentCommand.invoke`` works as intended.
    
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
    regex_match = None
    custom_id = ['hey_sister']
    
    component_command = ComponentCommand(function, name, custom_id = custom_id)
    
    client_id = 202410200002
    interaction_event_id = 202410200003
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    try:
        await component_command.invoke(client, interaction_event, regex_match)
        
        vampytest.assert_eq(function_called, 1)
    finally:
        client._delete()
        client = None
