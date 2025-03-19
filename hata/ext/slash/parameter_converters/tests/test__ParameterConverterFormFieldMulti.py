from re import compile as re_compile
from types import FunctionType

import vampytest

from .....discord import (
    ApplicationCommandOption, Client, ComponentType, InteractionComponent, InteractionEvent,
    InteractionMetadataFormSubmit, InteractionType
)

from ...command import SlashCommandFunction

from ..form_field_keyword import Pattern
from ..form_field_multi import ParameterConverterFormFieldMulti

from .helpers import _create_parameter


def _assert_fields_set(parameter_converter):
    """
    Asserts whether every attributes of the given parameter converter are set.
    
    Parameters
    ----------
    parameter_converter : ``ParameterConverterFormFieldMulti``
        The parameter converter to check.
    """
    vampytest.assert_instance(parameter_converter, ParameterConverterFormFieldMulti)
    vampytest.assert_instance(parameter_converter.annotation, str, Pattern)
    vampytest.assert_instance(parameter_converter.default, object)
    vampytest.assert_instance(parameter_converter.parameter_name, str)
    vampytest.assert_instance(parameter_converter.matcher, FunctionType)
    

def test__ParameterConverterFormFieldMulti__new__no_annotation():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__new__`` works as intended.
    
    Case: no annotation.
    """
    parameter_name = 'cake_type'
    default = 'potato'
    parameter = _create_parameter(parameter_name, default = default)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, parameter_name)
    vampytest.assert_eq(parameter_converter.default, default)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_string)


def test__ParameterConverterFormFieldMulti__new__string_annotation():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__new__`` works as intended.
    
    Case: string annotation.
    """
    parameter_name = 'cake_type'
    annotation = 'mamizou'
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_string)


def test__ParameterConverterFormFieldMulti__new__no_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__new__`` works as intended.
    
    Case: no group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('miau')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_regex)


def test__ParameterConverterFormFieldMulti__new__tuple_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__new__`` works as intended.
    
    Case: tuple group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('(miau)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_regex_group_tuple)


def test__ParameterConverterFormFieldMulti__new__dict_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__new__`` works as intended.
    
    Case: dict group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('(?P<name>miau)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_regex_group_dict)


def test__ParameterConverterFormFieldMulti__new__mixed_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__new__`` works as intended.
    
    Case: mixed group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('(?P<name>miau)(miau)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    with vampytest.assert_raises(ValueError):
        ParameterConverterFormFieldMulti(parameter)


async def test__ParameterConverterFormFieldMulti__call__string__hit():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: string & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180040
    interaction_event_id = 202503180041
    parameter = _create_parameter(parameter_name, annotation = parameter_name)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'kokoro',
                    value = 'love',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'cake_type',
                    value = 'potato',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'pudding_type',
                    value = 'flan',
                ),
            ],
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, ['potato'])
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldMulti__call__string__miss():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: string & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180042
    interaction_event_id = 202503180043
    parameter = _create_parameter(parameter_name, annotation = parameter_name) 
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_is(output, None)
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldMulti__call__regex_no_group__hit():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex no group & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180044
    interaction_event_id = 202503180045
    annotation = re_compile('[a-z]+_type')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'kokoro',
                    value = 'love',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'cake_type',
                    value = 'potato',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'pudding_type',
                    value = 'flan',
                ),
            ],
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, ['potato', 'flan'])
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldMulti__call__regex_no_group__miss():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex no group & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180046
    interaction_event_id = 202503180047
    annotation = re_compile('[a-z]+_type')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_is(output, None)
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldMulti__call__regex_tuple__hit():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex tuple group & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180048
    interaction_event_id = 202503180049
    annotation = re_compile('([a-z]+)_type')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'kokoro',
                    value = 'love',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'cake_type',
                    value =  'potato',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'pudding_type',
                    value = 'flan',
                ),
            ],
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, [(('cake', ), 'potato'), (('pudding', ), 'flan')])
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldMulti__call__regex_tuple__miss():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex tuple group & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180050
    interaction_event_id = 202503180051
    annotation = re_compile('([a-z]+)_type')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_is(output, None)
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldMulti__call__regex_dict__hit():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex dict group & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180052
    interaction_event_id = 202503180053
    annotation = re_compile('(?P<name>[a-z]+)_type')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'kokoro',
                    value = 'love',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'cake_type',
                    value = 'potato',
                ),
                InteractionComponent(
                    component_type = ComponentType.text_input,
                    custom_id = 'pudding_type',
                    value = 'flan',
                ),
            ],
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(output, [({'name': 'cake'}, 'potato'), ({'name': 'pudding'}, 'flan')])
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldMulti__call__regex_dict__miss():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex dict group & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180054
    interaction_event_id = 202503180055
    annotation = re_compile('(?P<name>[a-z]+)_type')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_is(output, None)
        
    finally:
        client._delete()
        client = None


def test__ParameterConverterFormFieldMulti__repr():
    """
    Tests whether ``ParameterConverterFormFieldMulti.__repr__`` works as intended.
    """
    parameter_name = 'cake_type'
    annotation = 'pudding'
    default = 'chocolate'
    parameter = _create_parameter(parameter_name, annotation = annotation, default = default)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    output = repr(parameter_converter)
    vampytest.assert_in(type(parameter_converter).__name__, output)
    vampytest.assert_in(f'parameter_name = {parameter_name!r}', output)
    vampytest.assert_in(f'annotation = {annotation!r}', output)
    vampytest.assert_in(f'default = {default!r}', output)
    

def test__ParameterConverterFormFieldMulti__as_option():
    """
    Tests whether ``ParameterConverterFormFieldMulti.as_option`` works as intended.
    """
    parameter_name = 'cake_type'
    parameter = _create_parameter(parameter_name)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    output = parameter_converter.as_option()
    
    vampytest.assert_instance(output, ApplicationCommandOption, nullable = True)
    vampytest.assert_is(output, None)


def test__ParameterConverterFormFieldMulti__bind_parent__none():
    """
    Tests whether ``ParameterConverterFormFieldMulti.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    parameter = _create_parameter(parameter_name)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
    parameter_converter.bind_parent(None)
    
    # Nothing to check here


def test__ParameterConverterFormFieldMulti__bind_parent__slash_command_function():
    """
    Tests whether ``ParameterConverterFormFieldMulti.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    parameter = _create_parameter(parameter_name)
    
    parameter_converter = ParameterConverterFormFieldMulti(parameter)
    
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
