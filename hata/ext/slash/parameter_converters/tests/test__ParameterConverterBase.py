import vampytest

from .....discord import ApplicationCommandOption, Client, InteractionEvent

from ...command import SlashCommandFunction

from ..base import ParameterConverterBase


def _assert_fields_set(parameter_converter):
    """
    Asserts whether every attributes of the given parameter converter are set.
    
    Parameters
    ----------
    parameter_converter : ``ParameterConverterBase``
        The parameter converter to check.
    """
    vampytest.assert_instance(parameter_converter, ParameterConverterBase)
    vampytest.assert_instance(parameter_converter.parameter_name, str)
    

def test__ParameterConverterBase__new():
    """
    Tests whether ``ParameterConverterBase.__new__`` works as intended.
    """
    parameter_name = 'cake_type'
    
    parameter_converter = ParameterConverterBase(parameter_name)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)


async def test__ParameterConverterBase__call():
    """
    Tests whether ``ParameterConverterBase.__call__`` works as intended.
    
    This function is a coroutine.
    """
    parameter_name = 'cake_type'
    client_id = 202503180000
    interaction_event_id = 202503180001
    value = 'potato'
    
    parameter_converter = ParameterConverterBase(parameter_name)
    
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, value)
        
        vampytest.assert_instance(output, type(None))
        vampytest.assert_is(output, None)
        
    finally:
        client._delete()
        client = None


def test__ParameterConverterBase__repr():
    """
    Tests whether ``ParameterConverterBase.__repr__`` works as intended.
    """
    parameter_name = 'cake_type'
    
    parameter_converter = ParameterConverterBase(parameter_name)
    
    output = repr(parameter_converter)
    vampytest.assert_in(type(parameter_converter).__name__, output)
    vampytest.assert_in(f'parameter_name = {parameter_name!r}', output)
    

def test__ParameterConverterBase__as_option():
    """
    Tests whether ``ParameterConverterBase.as_option`` works as intended.
    """
    parameter_name = 'cake_type'
    
    parameter_converter = ParameterConverterBase(parameter_name)
    
    output = parameter_converter.as_option()
    
    vampytest.assert_instance(output, ApplicationCommandOption, nullable = True)
    vampytest.assert_is(output, None)


def test__ParameterConverterBase__bind_parent__none():
    """
    Tests whether ``ParameterConverterBase.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    
    parameter_converter = ParameterConverterBase(parameter_name)
    
    parameter_converter.bind_parent(None)
    
    # Nothing to check here


def test__ParameterConverterBase__bind_parent__slash_command_function():
    """
    Tests whether ``ParameterConverterBase.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    
    parameter_converter = ParameterConverterBase(parameter_name)
    
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
