from re import compile as re_compile
from types import FunctionType

import vampytest

from .....discord import (
    ApplicationCommandOption, Client, ComponentType, InteractionComponent, InteractionEvent, InteractionType, Resolved,
    User
)

from ...command import SlashCommandFunction

from ..form_field_keyword import ParameterConverterFormFieldKeyword, Pattern

from .helpers import _create_parameter


def _assert_fields_set(parameter_converter):
    """
    Asserts whether every attributes of the given parameter converter are set.
    
    Parameters
    ----------
    parameter_converter : ``ParameterConverterFormFieldKeyword``
        The parameter converter to check.
    """
    vampytest.assert_instance(parameter_converter, ParameterConverterFormFieldKeyword)
    vampytest.assert_instance(parameter_converter.annotation, str, Pattern)
    vampytest.assert_instance(parameter_converter.default, object)
    vampytest.assert_instance(parameter_converter.parameter_name, str)
    vampytest.assert_instance(parameter_converter.matcher, FunctionType)
    

def test__ParameterConverterFormFieldKeyword__new__no_annotation():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__new__`` works as intended.
    
    Case: no annotation.
    """
    parameter_name = 'cake_type'
    default = 'potato'
    parameter = _create_parameter(parameter_name, default = default)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, parameter_name)
    vampytest.assert_eq(parameter_converter.default, default)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_string)


def test__ParameterConverterFormFieldKeyword__new__string_annotation():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__new__`` works as intended.
    
    Case: string annotation.
    """
    parameter_name = 'cake_type'
    annotation = 'mamizou'
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_string)


def test__ParameterConverterFormFieldKeyword__new__no_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__new__`` works as intended.
    
    Case: no group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('miau')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_regex)


def test__ParameterConverterFormFieldKeyword__new__tuple_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__new__`` works as intended.
    
    Case: tuple group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('(miau)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_regex_group_tuple)


def test__ParameterConverterFormFieldKeyword__new__dict_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__new__`` works as intended.
    
    Case: dict group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('(?P<name>miau)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.annotation, annotation)
    vampytest.assert_is(parameter_converter.default, None)
    vampytest.assert_is(parameter_converter.matcher, type(parameter_converter)._converter_regex_group_dict)


def test__ParameterConverterFormFieldKeyword__new__mixed_group_regex():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__new__`` works as intended.
    
    Case: mixed group regex.
    """
    parameter_name = 'cake_type'
    annotation = re_compile('(?P<name>miau)(miau)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    with vampytest.assert_raises(ValueError):
        ParameterConverterFormFieldKeyword(parameter)


async def test__ParameterConverterFormFieldKeyword__call__string__hit():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: string & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180012
    interaction_event_id = 202503180013
    parameter = _create_parameter(parameter_name, annotation = parameter_name)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'kokoro',
                value = 'love',
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'cake_type',
                value = 'potato',
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'pudding_type',
                value = 'flan',
            ),
        ],
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, object, nullable = True)
        vampytest.assert_eq(output, 'potato')
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldKeyword__call__string__miss():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: string & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180030
    interaction_event_id = 202503180031
    default = 'radish'
    parameter = _create_parameter(parameter_name, annotation = parameter_name, default = default) 
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
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


async def test__ParameterConverterFormFieldKeyword__call__string__resolved():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: string & resolved.
    """
    parameter_name = 'cake_type'
    client_id = 202509130008
    interaction_event_id = 202509130009
    parameter = _create_parameter(parameter_name, annotation = parameter_name)
     
    user_0 = User.precreate(202509130010)
    user_1 = User.precreate(202509130011)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                ComponentType.user_select,
                custom_id = 'cake_type',
                values = [str(user_0.id), str(user_1.id)],
            ),
        ],
        resolved = Resolved(
            users = [user_0, user_1],
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


async def test__ParameterConverterFormFieldKeyword__call__regex_no_group__hit():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex no group & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180014
    interaction_event_id = 202503180015
    annotation = re_compile(parameter_name)
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'kokoro',
                value = 'love',
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'cake_type',
                value = 'potato',
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'pudding_type',
                value = 'flan',
            ),
        ],
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, object, nullable = True)
        vampytest.assert_eq(output, 'potato')
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldKeyword__call__regex_no_group__miss():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex no group & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180032
    interaction_event_id = 202503180033
    annotation = re_compile(parameter_name)
    default = 'radish'
    parameter = _create_parameter(parameter_name, annotation = annotation, default = default)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
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



async def test__ParameterConverterFormFieldKeyword__call__regex_no_group__resolved():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex no group & resolved.
    """
    parameter_name = 'cake_type'
    client_id = 202509130012
    interaction_event_id = 202503180013
    annotation = re_compile(parameter_name)
    parameter = _create_parameter(parameter_name, annotation = annotation)
     
    user_0 = User.precreate(202503180014)
    user_1 = User.precreate(202503180015)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                ComponentType.user_select,
                custom_id = 'cake_type',
                values = [str(user_0.id), str(user_1.id)],
            ),
        ],
        resolved = Resolved(
            users = [user_0, user_1],
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


async def test__ParameterConverterFormFieldKeyword__call__regex_tuple__hit():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex tuple group & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180016
    interaction_event_id = 202503180017
    annotation = re_compile('cake_([a-z]+)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'kokoro',
                value = 'love',
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'cake_type',
                value =  'potato',
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'pudding_type',
                value = 'flan',
            ),
        ],
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(output, (('type', ), 'potato'))
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldKeyword__call__regex_tuple__miss():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex tuple group & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180034
    interaction_event_id = 202503180035
    annotation = re_compile('cake_([a-z]+)')
    default = 'radish'
    parameter = _create_parameter(parameter_name, annotation = annotation, default = default)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(output, (None, default))
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldKeyword__call__regex_tuple__resolved():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex tuple group & resolved.
    """
    parameter_name = 'cake_type'
    client_id = 202509130016
    interaction_event_id = 202509130017
    annotation = re_compile('cake_([a-z]+)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
     
    user_0 = User.precreate(202509130018)
    user_1 = User.precreate(202509130019)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                ComponentType.user_select,
                custom_id = 'cake_type',
                values = [str(user_0.id), str(user_1.id)],
            ),
        ],
        resolved = Resolved(
            users = [user_0, user_1],
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(output, (('type', ), (user_0, user_1)))
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldKeyword__call__regex_dict__hit():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex dict group & hit.
    """
    parameter_name = 'cake_type'
    client_id = 202503180018
    interaction_event_id = 202503180019
    annotation = re_compile('cake_(?P<name>[a-z]+)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
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
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(output, ({'name': 'type'}, 'potato'))
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldKeyword__call__regex_dict__miss():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex dict group & miss.
    """
    parameter_name = 'cake_type'
    client_id = 202503180036
    interaction_event_id = 202503180037
    annotation = re_compile('cake_(?P<name>[a-z]+)')
    default = 'radish'
    parameter = _create_parameter(parameter_name, annotation = annotation, default = default)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(output, (None, default))
        
    finally:
        client._delete()
        client = None


async def test__ParameterConverterFormFieldKeyword__call__regex_dict__resolved():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: Regex dict group & resolved.
    """
    parameter_name = 'cake_type'
    client_id = 202509130020
    interaction_event_id = 202509130021
    annotation = re_compile('cake_(?P<name>[a-z]+)')
    parameter = _create_parameter(parameter_name, annotation = annotation)
     
    user_0 = User.precreate(202509130022)
    user_1 = User.precreate(202509130023)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                component_type = ComponentType.text_input,
                custom_id = 'kokoro',
                value = 'love',
            ),
            InteractionComponent(
                component_type = ComponentType.user_select,
                custom_id = 'cake_type',
                values = [str(user_0.id), str(user_1.id)],
            ),
        ],
        resolved = Resolved(
            users = [user_0, user_1],
        ),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, None)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(output, ({'name': 'type'}, (user_0, user_1)))
        
    finally:
        client._delete()
        client = None


def test__ParameterConverterFormFieldKeyword__repr():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.__repr__`` works as intended.
    """
    parameter_name = 'cake_type'
    annotation = 'pudding'
    default = 'chocolate'
    parameter = _create_parameter(parameter_name, annotation = annotation, default = default)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    output = repr(parameter_converter)
    vampytest.assert_in(type(parameter_converter).__name__, output)
    vampytest.assert_in(f'parameter_name = {parameter_name!r}', output)
    vampytest.assert_in(f'annotation = {annotation!r}', output)
    vampytest.assert_in(f'default = {default!r}', output)
    

def test__ParameterConverterFormFieldKeyword__as_option():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.as_option`` works as intended.
    """
    parameter_name = 'cake_type'
    parameter = _create_parameter(parameter_name)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    output = parameter_converter.as_option()
    
    vampytest.assert_instance(output, ApplicationCommandOption, nullable = True)
    vampytest.assert_is(output, None)


def test__ParameterConverterFormFieldKeyword__bind_parent__none():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    parameter = _create_parameter(parameter_name)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
    parameter_converter.bind_parent(None)
    
    # Nothing to check here


def test__ParameterConverterFormFieldKeyword__bind_parent__slash_command_function():
    """
    Tests whether ``ParameterConverterFormFieldKeyword.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    parameter = _create_parameter(parameter_name)
    
    parameter_converter = ParameterConverterFormFieldKeyword(parameter)
    
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
