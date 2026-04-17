import vampytest

from .....discord import ApplicationCommandOption, Client, InteractionEvent

from ...command import SlashCommandFunction
from ...converters import RegexMatch

from ..regex import ParameterConverterRegex

from .helpers import _create_parameter


def _assert_fields_set(parameter_converter):
    """
    Asserts whether every attributes of the given parameter converter are set.
    
    Parameters
    ----------
    parameter_converter : ``ParameterConverterRegex``
        The parameter converter to check.
    """
    vampytest.assert_instance(parameter_converter, ParameterConverterRegex)
    vampytest.assert_instance(parameter_converter.default, object)
    vampytest.assert_instance(parameter_converter.index, int)
    vampytest.assert_instance(parameter_converter.parameter_name, str)
    vampytest.assert_instance(parameter_converter.required, bool)
    

def test__ParameterConverterRegex__new():
    """
    Tests whether ``ParameterConverterRegex.__new__`` works as intended.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    required = False
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.index, index)
    vampytest.assert_eq(parameter_converter.default, default)
    vampytest.assert_eq(parameter_converter.required, required)


async def test__ParameterConverterRegex__call__in_match__tuple():
    """
    Tests whether ``ParameterConverterRegex.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: In match; tuple.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    required = False
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    client_id = 202503180006
    interaction_event_id = 202503180007
    value = RegexMatch(False, ('koishi', 'kokoro', 'nue', 'mamizou', 'byakuren'))
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, value)
        
        vampytest.assert_instance(output, str, nullable = True)
        vampytest.assert_eq(output, 'mamizou')
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterRegex__call__in_match__dict():
    """
    Tests whether ``ParameterConverterRegex.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: In match; dict.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    required = False
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    client_id = 202503180008
    interaction_event_id = 202503180009
    value = RegexMatch(True, {parameter_name: 'mamizou'})
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, value)
        
        vampytest.assert_instance(output, str, nullable = True)
        vampytest.assert_eq(output, 'mamizou')
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterRegex__call__out_of_match__tuple():
    """
    Tests whether ``ParameterConverterRegex.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: In match; tuple.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    required = False
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    client_id = 202503180010
    interaction_event_id = 202503180011
    value = RegexMatch(False, ('koishi', 'kokoro', 'nue'))
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, value)
        
        vampytest.assert_instance(output, str, nullable = True)
        vampytest.assert_eq(output, default)
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterRegex__call__out_of_match__dict():
    """
    Tests whether ``ParameterConverterRegex.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: In match; dict.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    required = False
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    client_id = 202503180012
    interaction_event_id = 202503180013
    value = RegexMatch(True, {'mrr': 'mamizou'})
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, value)
        
        vampytest.assert_instance(output, str, nullable = True)
        vampytest.assert_eq(output, default)
        
    finally:
        client._delete()
        client = None


def test__ParameterConverterRegex__repr():
    """
    Tests whether ``ParameterConverterRegex.__repr__`` works as intended.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    required = False
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    output = repr(parameter_converter)
    vampytest.assert_in(type(parameter_converter).__name__, output)
    vampytest.assert_in(f'parameter_name = {parameter_name!r}', output)
    vampytest.assert_in(f'index = {index!r}', output)
    vampytest.assert_in(f'default = {default!r}', output)


def test__ParameterConverterRegex__as_option():
    """
    Tests whether ``ParameterConverterRegex.as_option`` works as intended.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    required = False
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    output = parameter_converter.as_option()
    
    vampytest.assert_instance(output, ApplicationCommandOption, nullable = True)
    vampytest.assert_is(output, None)


def test__ParameterConverterRegex__bind_parent__none():
    """
    Tests whether ``ParameterConverterRegex.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    parameter_converter.bind_parent(None)
    
    # Nothing to check here


def test__ParameterConverterRegex__bind_parent__slash_command_function():
    """
    Tests whether ``ParameterConverterRegex.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    default = 'sanae'
    parameter = _create_parameter(parameter_name, default = default)
    index = 3
    
    parameter_converter = ParameterConverterRegex(parameter, index)
    
    async def function():
        return None
    
    parameter_converters = ()
    name = 'yuuka'
    description = 'rember happy day'
    response_modifier = None
    default = False
    
    slash_command_function = SlashCommandFunction(
        function, parameter_converters, name, description, response_modifier, default
    )
    
    parameter_converter.bind_parent(slash_command_function)
    
    # Nothing to check here
