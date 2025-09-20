import vampytest

from .....discord import (
    Client, ComponentType, InteractionComponent, InteractionEvent, InteractionMetadataMessageComponent, InteractionType,
    Resolved, User
)

from ..message_component_keyword import ParameterConverterMessageComponentKeyword

from .helpers import _create_parameter


def _assert_fields_set(parameter_converter):
    """
    Asserts whether every attributes of the given parameter converter are set.
    
    Parameters
    ----------
    parameter_converter : ``ParameterConverterMessageComponentKeyword``
        The parameter converter to check.
    """
    vampytest.assert_instance(parameter_converter, ParameterConverterMessageComponentKeyword)
    vampytest.assert_instance(parameter_converter.default, object)
    vampytest.assert_instance(parameter_converter.parameter_name, str)


def test__ParameterConverterMessageComponentKeyword__new():
    """
    Tests whether ``ParameterConverterMessageComponentKeyword.__new__`` works as intended.
    """
    parameter_name = 'cake_type'
    default = 'pudding'
    parameter = _create_parameter(parameter_name, default = default)
    
    parameter_converter = ParameterConverterMessageComponentKeyword(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.default, default)
    vampytest.assert_is(parameter_converter.parameter_name, parameter_name)


async def test__ParameterConverterMessageComponentKeyword__call__hit():
    """
    Tests whether ``ParameterConverterMessageComponentKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: hit.
    """
    parameter_name = 'cake_type'
    client_id = 202509130000
    interaction_event_id = 202509130001
    parameter = _create_parameter(parameter_name)
    
    parameter_converter = ParameterConverterMessageComponentKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.message_component,
        component = InteractionComponent(
            ComponentType.text_input,
            custom_id = 'kokoro',
            value = 'love',
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, object, nullable = True)
        vampytest.assert_eq(output, 'love')
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterMessageComponentKeyword__call__miss():
    """
    Tests whether ``ParameterConverterMessageComponentKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: miss.
    """
    parameter_name = 'cake_type'
    client_id = 202509130002
    interaction_event_id = 202509130003
    default = 'radish'
    parameter = _create_parameter(parameter_name, annotation = parameter_name, default = default) 
    
    parameter_converter = ParameterConverterMessageComponentKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.message_component,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, object, nullable = True)
        vampytest.assert_eq(output, default)
        
    finally:
        client._delete()
        client = None



async def test__ParameterConverterMessageComponentKeyword__call__resolved():
    """
    Tests whether ``ParameterConverterMessageComponentKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: resolved.
    """
    parameter_name = 'cake_type'
    client_id = 202509130004
    interaction_event_id = 202509130005
    parameter = _create_parameter(parameter_name)
     
    user_0 = User.precreate(202509130006)
    user_1 = User.precreate(202509130007)
    
    parameter_converter = ParameterConverterMessageComponentKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.message_component,
        component = InteractionComponent(
            ComponentType.user_select,
            custom_id = 'kokoro',
            values = [str(user_0.id), str(user_1.id)],
        ),
        resolved = Resolved(
            users = [user_0, user_1]
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, object, nullable = True)
        vampytest.assert_eq(output, (user_0, user_1))
        
    finally:
        client._delete()
        client = None
