from enum import Enum
from types import FunctionType

import vampytest

from .....discord import (
    ApplicationCommandOption, ApplicationCommandOptionChoice, ApplicationCommandOptionType, Client, InteractionEvent
)

from ...command import SlashCommandFunction, SlashCommandParameterAutoCompleter
from ...constants import APPLICATION_COMMAND_FUNCTION_DEEPNESS
from ...converter_constants import ANNOTATION_TYPE_STR, ANNOTATION_TYPE_USER
from ...converters import converter_str, converter_user

from ..slash_command import ParameterConverterSlashCommand


async def _auto_completer(value):
    pass


def _assert_fields_set(parameter_converter):
    """
    Asserts whether every attributes of the given parameter converter are set.
    
    Parameters
    ----------
    parameter_converter : ``ParameterConverterSlashCommand``
        The parameter converter to check.
    """
    vampytest.assert_instance(parameter_converter, ParameterConverterSlashCommand)
    vampytest.assert_instance(parameter_converter.auto_completer, SlashCommandParameterAutoCompleter, nullable = True)
    vampytest.assert_instance(parameter_converter.channel_types, tuple, nullable = True)
    vampytest.assert_subtype(parameter_converter.choice_enum_type, Enum, nullable = True)
    vampytest.assert_instance(parameter_converter.choices, dict, nullable = True)
    vampytest.assert_instance(parameter_converter.converter, FunctionType)
    vampytest.assert_instance(parameter_converter.default, object)
    vampytest.assert_instance(parameter_converter.description, str, nullable = True)
    vampytest.assert_instance(parameter_converter.max_length, int)
    vampytest.assert_instance(parameter_converter.max_value, int, float, nullable = True)
    vampytest.assert_instance(parameter_converter.min_length, int)
    vampytest.assert_instance(parameter_converter.min_value, int, float, nullable = True)
    vampytest.assert_instance(parameter_converter.name, str)
    vampytest.assert_instance(parameter_converter.parameter_name, str)
    vampytest.assert_instance(parameter_converter.required, bool)
    vampytest.assert_instance(parameter_converter.type, int)


def test__ParameterConverterSlashCommand__new():
    """
    Tests whether ``ParameterConverterSlashCommand.__new__`` works as intended.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = 'pudding'
    required = False
    choice_enum_type = None
    choices = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = _auto_completer
    max_length = 100
    min_length = 1
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    _assert_fields_set(parameter_converter)
    
    vampytest.assert_is_not(parameter_converter.auto_completer, None)
    vampytest.assert_is(parameter_converter.auto_completer._command_function, auto_completer_function)
    vampytest.assert_eq(parameter_converter.auto_completer.name_pairs, frozenset((('cake_type', 'cake-type'),)))
    vampytest.assert_eq(parameter_converter.auto_completer.deepness, APPLICATION_COMMAND_FUNCTION_DEEPNESS)
    vampytest.assert_eq(parameter_converter.channel_types, channel_types)
    vampytest.assert_is(parameter_converter.choice_enum_type, choice_enum_type)
    vampytest.assert_eq(parameter_converter.choices, choices)
    vampytest.assert_is(parameter_converter.converter, converter)
    vampytest.assert_eq(parameter_converter.default, default)
    vampytest.assert_eq(parameter_converter.description, description)
    vampytest.assert_eq(parameter_converter.max_length, max_length)
    vampytest.assert_eq(parameter_converter.max_value, max_value)
    vampytest.assert_eq(parameter_converter.min_length, min_length)
    vampytest.assert_eq(parameter_converter.min_value, min_value)
    vampytest.assert_eq(parameter_converter.name, name)
    vampytest.assert_eq(parameter_converter.parameter_name, parameter_name)
    vampytest.assert_eq(parameter_converter.required, required)
    vampytest.assert_eq(parameter_converter.type, converter_type)


async def test__ParameterConverterSlashCommand__call():
    """
    Tests whether ``ParameterConverterSlashCommand.__call__`` works as intended.
    
    This function is a coroutine.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = 'pudding'
    required = False
    choice_enum_type = None
    choices = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = _auto_completer
    max_length = 100
    min_length = 1
    client_id = 202503180070
    interaction_event_id = 202503180071
    value = 'potato'
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        output = await parameter_converter(client, interaction_event, value)
        
        vampytest.assert_instance(output, str, nullable = True)
        vampytest.assert_eq(output, value)
        
    finally:
        client._delete()
        client = None


def test__ParameterConverterSlashCommand__repr():
    """
    Tests whether ``ParameterConverterSlashCommand.__repr__`` works as intended.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = 'pudding'
    required = False
    choice_enum_type = None
    choices = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = _auto_completer
    max_length = 100
    min_length = 1
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    output = repr(parameter_converter)
    vampytest.assert_in(type(parameter_converter).__name__, output)
    vampytest.assert_in(f'parameter_name = {parameter_name!r}', output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'type = str', output)
    vampytest.assert_in(f'description = {description!r}', output)
    vampytest.assert_in(f'required = {required!r}', output)
    vampytest.assert_in(f'default = {default!r}', output)
    vampytest.assert_not_in(f'choices = {choices!r}', output)
    vampytest.assert_in(f'auto_completer = {parameter_converter.auto_completer!r}', output)
    vampytest.assert_not_in(f'channel_types = {channel_types!r}', output)
    vampytest.assert_not_in(f'min_value = {min_value!r}', output)
    vampytest.assert_not_in(f'max_value = {max_value!r}', output)
    vampytest.assert_in(f'min_length = {min_length!r}', output)
    vampytest.assert_in(f'max_length = {max_length!r}', output)


def test__ParameterConverterSlashCommand__as_option():
    """
    Tests whether ``ParameterConverterSlashCommand.as_option`` works as intended.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = 'pudding'
    required = False
    choice_enum_type = None
    choices = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = _auto_completer
    max_length = 100
    min_length = 1
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    output = parameter_converter.as_option()
    
    vampytest.assert_instance(output, ApplicationCommandOption, nullable = True)
    vampytest.assert_eq(
        output,
        ApplicationCommandOption(
            name,
            description,
            ApplicationCommandOptionType.string,
            autocomplete = True,
            channel_types = None,
            choices = None,
            required = required,
            min_value = min_value,
            max_value = max_value,
            min_length = min_length,
            max_length = max_length,
        )
    )


def test__ParameterConverterSlashCommand__as_option__with_choices():
    """
    Tests whether ``ParameterConverterSlashCommand.as_option`` works as intended.
    
    Case: with choices.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = None
    required = True
    choice_enum_type = None
    choices = {
        'flandre': 'pudding',
        'koishi': 'cake',
        'sakuya': 'tea',
    }
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = None
    max_length = 0
    min_length = 0
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    output = parameter_converter.as_option()
    
    vampytest.assert_instance(output, ApplicationCommandOption, nullable = True)
    vampytest.assert_eq(
        output,
        ApplicationCommandOption(
            name,
            description,
            ApplicationCommandOptionType.string,
            autocomplete = False,
            channel_types = None,
            choices = [
                ApplicationCommandOptionChoice('pudding', 'flandre'),
                ApplicationCommandOptionChoice('cake', 'koishi'),
                ApplicationCommandOptionChoice('tea', 'sakuya'),
            ],
            required = required,
            min_value = min_value,
            max_value = max_value,
            min_length = min_length,
            max_length = max_length,
        )
    )


def _iter_options__can_be_auto_completed():
    yield ANNOTATION_TYPE_STR, converter_str, None, True
    yield ANNOTATION_TYPE_STR, converter_str, {'koishi': 'pudding'}, False
    yield ANNOTATION_TYPE_USER, converter_user, None, False


@vampytest._(vampytest.call_from(_iter_options__can_be_auto_completed()).returning_last())
def test__ParameterConverterSlashCommand__can_be_auto_completed(converter_type, converter, choices):
    """
    Tests whether ``ParameterConverterSlashCommand.can_be_auto_completed`` works as intended.
    
    Parameters
    ----------
    converter_type : `int`
        Internal identifier of the converter.
    
    converter : `CoroutineFunctionType`
        The converter to use to convert a value to it's desired type.
    
    choices : `None | dict<int | float | str | Enum, str>`
        The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
    
    Returns
    -------
    output : `bool`
    """
    parameter_name = 'cake_type'
    name = 'cake-type'
    description = 'The type of the cake'
    default = None
    required = True
    choice_enum_type = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = None
    max_length = 0
    min_length = 0
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    output = parameter_converter.can_be_auto_completed()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__is_auto_completed():
    yield None, False
    yield _auto_completer, True


@vampytest._(vampytest.call_from(_iter_options__is_auto_completed()).returning_last())
def test__ParameterConverterSlashCommand__is_auto_completed(auto_completer_function):
    """
    Tests whether ``ParameterConverterSlashCommand.is_auto_completed`` works as intended.
    
    Parameters
    ----------
    auto_completer_function : `None | async-callable`
        Auto completer if defined.
    
    Returns
    -------
    output : `bool`
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = None
    required = True
    choice_enum_type = None
    choices = None
    channel_types = None
    max_value = None
    min_value = None
    max_length = 0
    min_length = 0
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    output = parameter_converter.is_auto_completed()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__register_auto_completer__passing():
    new_auto_completer_0 = SlashCommandParameterAutoCompleter(
        _auto_completer, ['pudding'], APPLICATION_COMMAND_FUNCTION_DEEPNESS, None
    )
    
    new_auto_completer_1 = SlashCommandParameterAutoCompleter(
        _auto_completer, ['pudding'], 2, None
    )
    
    old_auto_completer_0 = SlashCommandParameterAutoCompleter(
        _auto_completer, ['cake'], APPLICATION_COMMAND_FUNCTION_DEEPNESS, None
    )
    
    old_auto_completer_1 = SlashCommandParameterAutoCompleter(
        _auto_completer, ['cake'], 2, None
    )
    
    yield (
        'no old, new with max deepness',
        ANNOTATION_TYPE_STR,
        converter_str,
        None,
        None,
        new_auto_completer_0,
        (1, new_auto_completer_0),
    )
    
    yield (
        'no old, new with not max deepness',
        ANNOTATION_TYPE_STR,
        converter_str,
        None,
        None,
        new_auto_completer_1,
        (1, new_auto_completer_1),
    )
    
    yield (
        'same deepness, with max',
        ANNOTATION_TYPE_STR,
        converter_str,
        None,
        old_auto_completer_0,
        new_auto_completer_0,
        (0, old_auto_completer_0),
    )
    
    yield (
        'same deepness, with not max',
        ANNOTATION_TYPE_STR,
        converter_str,
        None,
        old_auto_completer_1,
        new_auto_completer_1,
        (0, old_auto_completer_1),
    )
    
    yield (
        'higher deepness',
        ANNOTATION_TYPE_STR,
        converter_str,
        None,
        old_auto_completer_1,
        new_auto_completer_0,
        (1, new_auto_completer_0),
    )
    
    yield (
        'lower deepness',
        ANNOTATION_TYPE_STR,
        converter_str,
        None,
        old_auto_completer_0,
        new_auto_completer_1,
        (0, old_auto_completer_0),
    )


def _iter_options__register_auto_completer__runtime_error():
    new_auto_completer = SlashCommandParameterAutoCompleter(
        _auto_completer, ['pudding'], APPLICATION_COMMAND_FUNCTION_DEEPNESS, None
    )
    
    yield (
        'has choices',
        ANNOTATION_TYPE_STR,
        converter_str,
        {'koishi': 'pudding'},
        None,
        new_auto_completer,
    )
    
    yield (
        'not auto completable',
        ANNOTATION_TYPE_USER,
        converter_user,
        None,
        None,
        new_auto_completer,
    )


@vampytest._(vampytest.call_from(_iter_options__register_auto_completer__passing()).named_first().returning_last())
@vampytest._(vampytest.call_from(_iter_options__register_auto_completer__runtime_error()).named_first().raising(RuntimeError))
def test__ParameterConverterSlashCommand__register_auto_completer(
    converter_type, converter, choices, auto_completer, new_auto_completer
):
    """
    Tests whether ``ParameterConverterSlashCommand.register_auto_completer`` works as intended.
    
    Parameters
    ----------
    converter_type : `int`
        Internal identifier of the converter.
    
    converter : `CoroutineFunctionType`
        The converter to use to convert a value to it's desired type.
    
    choices : `None | dict<int | float | str | Enum, str>`
        The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
    
    auto_completer : `None | SlashCommandParameterAutoCompleter`
        Auto completer to bind first.
    
    new_auto_completer : `None | SlashCommandParameterAutoCompleter`
        Auto completer to bind as part of the test.
    
    Returns
    -------
    output_and_bound_auto_completer : `int, None | SlashCommandParameterAutoCompleter`
    
    Raises
    ------
    RuntimeError
    """
    parameter_name = 'cake_type'
    name = 'cake-type'
    description = 'The type of the cake'
    default = None
    required = True
    choice_enum_type = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = None
    max_length = 0
    min_length = 0
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    if (auto_completer is not None):
        parameter_converter.register_auto_completer(auto_completer)
    
    output = parameter_converter.register_auto_completer(new_auto_completer)
    vampytest.assert_instance(output, int)
    return output, parameter_converter.auto_completer


def test__ParameterConverterSlashCommand__bind_parent__none():
    """
    Tests whether ``ParameterConverterSlashCommand.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = 'pudding'
    required = False
    choice_enum_type = None
    choices = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = _auto_completer
    max_length = 100
    min_length = 1
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
    parameter_converter.bind_parent(None)
    vampytest.assert_is_not(parameter_converter.auto_completer, None)
    vampytest.assert_is(parameter_converter.auto_completer._parent_reference, None)


def test__ParameterConverterSlashCommand__bind_parent__slash_command_function():
    """
    Tests whether ``ParameterConverterSlashCommand.bind_parent`` works as intended.
    
    Case: no parent.
    """
    parameter_name = 'cake_type'
    converter_type = ANNOTATION_TYPE_STR
    converter = converter_str
    name = 'cake-type'
    description = 'The type of the cake'
    default = 'pudding'
    required = False
    choice_enum_type = None
    choices = None
    channel_types = None
    max_value = None
    min_value = None
    auto_completer_function = _auto_completer
    max_length = 100
    min_length = 1
    
    parameter_converter = ParameterConverterSlashCommand(
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    )
    
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
    
    vampytest.assert_is_not(parameter_converter.auto_completer, None)
    vampytest.assert_is_not(parameter_converter.auto_completer._parent_reference, None)
    vampytest.assert_is(parameter_converter.auto_completer._parent_reference(), slash_command_function)
