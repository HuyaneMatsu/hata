from types import FunctionType

import vampytest

from .....discord import ApplicationCommandOption, Client, InteractionEvent

from ...command import SlashCommandFunction
from ...converter_constants import ANNOTATION_TYPE_SELF_CLIENT
from ...converters import converter_self_client

from ..internal import ParameterConverterInternal


def _assert_fields_set(parameter_converter):
    """
    Asserts whether every attributes of the given parameter converter are set.
    
    Parameters
    ----------
    parameter_converter : ``ParameterConverterInternal``
        The parameter converter to check.
    """
    vampytest.assert_instance(parameter_converter, ParameterConverterInternal)
    vampytest.assert_instance(parameter_converter.converter, FunctionType)
    vampytest.assert_instance(parameter_converter.parameter_name, str)
    vampytest.assert_instance(parameter_converter.type, int)
    

def test__ParameterConverterInternal__new():
    """
    Tests whether ``ParameterConverterInternal.__new__`` works as intended.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_SELF_CLIENT
    converter = converter_self_client
    
    parameter_converter = ParameterConverterInternal(parameter_name, converter_type, converter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.converter, converter)
    vampytest.assert_eq(parameter_converter.type, converter_type)


async def test__ParameterConverterInternal__call():
    """
    Tests whether ``ParameterConverterInternal.__call__`` works as intended.
    
    This function is a coroutine.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_SELF_CLIENT
    converter = converter_self_client
    client_id = 202503180002
    interaction_event_id = 202503180003
    value = 'potato'
    
    parameter_converter = ParameterConverterInternal(parameter_name, converter_type, converter)
    
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, value)
        
        vampytest.assert_instance(output, Client)
        vampytest.assert_is(output, client)
        
    finally:
        client._delete()
        client = None


def test__ParameterConverterInternal__repr():
    """
    Tests whether ``ParameterConverterInternal.__repr__`` works as intended.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_SELF_CLIENT
    converter = converter_self_client
    
    parameter_converter = ParameterConverterInternal(parameter_name, converter_type, converter)
    
    output = repr(parameter_converter)
    vampytest.assert_in(type(parameter_converter).__name__, output)
    vampytest.assert_in(f'parameter_name = {parameter_name!r}', output)
    vampytest.assert_in(f'type = client', output)
    

def test__ParameterConverterInternal__as_option():
    """
    Tests whether ``ParameterConverterInternal.as_option`` works as intended.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_SELF_CLIENT
    converter = converter_self_client
    
    parameter_converter = ParameterConverterInternal(parameter_name, converter_type, converter)
    
    output = parameter_converter.as_option()
    
    vampytest.assert_instance(output, ApplicationCommandOption, nullable = True)
    vampytest.assert_is(output, None)


def test__ParameterConverterInternal__bind_parent__none():
    """
    Tests whether ``ParameterConverterInternal.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_SELF_CLIENT
    converter = converter_self_client
    
    parameter_converter = ParameterConverterInternal(parameter_name, converter_type, converter)
    
    parameter_converter.bind_parent(None)
    
    # Nothing to check here


def test__ParameterConverterInternal__bind_parent__slash_command_function():
    """
    Tests whether ``ParameterConverterInternal.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_SELF_CLIENT
    converter = converter_self_client
    
    parameter_converter = ParameterConverterInternal(parameter_name, converter_type, converter)
    
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
