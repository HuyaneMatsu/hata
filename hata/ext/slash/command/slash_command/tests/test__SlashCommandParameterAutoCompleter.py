import vampytest
from scarletio import WeakReferer

from ....constants import APPLICATION_COMMAND_FUNCTION_DEEPNESS

from ..slash_command import SlashCommand
from ..slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


def _assert_fields_set(slash_command_parameter_auto_completer):
    """
    Asserts whether every fields are set of the given auto completer.
    
    Parameters
    ----------
    slash_command_parameter_auto_completer : ``SlashCommandParameterAutoCompleter``
        The auto completer to check.
    """
    vampytest.assert_instance(slash_command_parameter_auto_completer, SlashCommandParameterAutoCompleter)
    vampytest.assert_instance(slash_command_parameter_auto_completer._command_function, object)
    vampytest.assert_instance(slash_command_parameter_auto_completer._exception_handlers, list, nullable = True)
    vampytest.assert_instance(slash_command_parameter_auto_completer._parameter_converters, tuple)
    vampytest.assert_instance(slash_command_parameter_auto_completer._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(slash_command_parameter_auto_completer.deepness, int)
    vampytest.assert_instance(slash_command_parameter_auto_completer.name_pairs, frozenset)


def test__SlashCommandParameterAutoCompleter__new():
    """
    Tests whether ``SlashCommandParameterAutoCompleter.__new__`` works as intended.
    """
    async def function(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    deepness = 2
    parent = SlashCommand(None, 'yuuka')
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, parent,
    )
    _assert_fields_set(slash_command_parameter_auto_completer)
    
    vampytest.assert_is(slash_command_parameter_auto_completer._command_function, function)
    vampytest.assert_eq(slash_command_parameter_auto_completer._parent_reference, parent.get_self_reference())
    vampytest.assert_eq(slash_command_parameter_auto_completer.deepness, deepness)
    vampytest.assert_eq(
        slash_command_parameter_auto_completer.name_pairs,
        frozenset((('hey_mister', 'hey-mister'), ('hey-sister', 'hey-sister'))),
    )


def test__SlashCommandParameterAutoCompleter__repr():
    """
    Tests whether ``SlashCommandParameterAutoCompleter.__repr__`` works as intended.
    """
    async def function(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    deepness = 2
    parent = SlashCommand(None, 'yuuka')
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, parent,
    )
    slash_command_parameter_auto_completer.error(exception_handler)
    
    output = repr(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(slash_command_parameter_auto_completer).__name__, output)
    vampytest.assert_in(f'name_pairs = {slash_command_parameter_auto_completer.name_pairs!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)
    vampytest.assert_in(f'command_function = {function!r}', output)
    vampytest.assert_in(f'deepness = {deepness!r}', output)


def test__SlashCommandParameterAutoCompleter__hash():
    """
    Tests whether ``SlashCommandParameterAutoCompleter.__hash__`` works as intended.
    """
    async def function(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    deepness = 2
    parent = SlashCommand(None, 'yuuka')
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, parent,
    )
    slash_command_parameter_auto_completer.error(exception_handler)
    
    output = hash(slash_command_parameter_auto_completer)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    async def function_0(value):
        return None
    
    async def function_1(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    deepness = 2
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function_0,
        'parameter_names': parameter_names,
        'deepness': deepness,
        'parent': None,
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
            'parameter_names': ['kazami'],
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'deepness': 1,
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
def test__SlashCommandParameterAutoCompleter__eq(
    keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1
):
    """
    Tests whether ``SlashCommandParameterAutoCompleter.__eq__`` works as intended.
    
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
    slash_command_parameter_auto_completer_0 = SlashCommandParameterAutoCompleter(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        slash_command_parameter_auto_completer_0.error(exception_handler)
    
    slash_command_parameter_auto_completer_1 = SlashCommandParameterAutoCompleter(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        slash_command_parameter_auto_completer_1.error(exception_handler)
    
    output = slash_command_parameter_auto_completer_0 == slash_command_parameter_auto_completer_1
    vampytest.assert_instance(output, bool)
    return output


def test__SlashCommandParameterAutoCompleter__copy():
    """
    Tests whether ``SlashCommandParameterAutoCompleter.copy`` works as intended.
    """
    async def function(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    deepness = 2
    parent = SlashCommand(None, 'yuuka')
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, parent,
    )
    slash_command_parameter_auto_completer.error(exception_handler)
    
    output = slash_command_parameter_auto_completer.copy()
    _assert_fields_set(output)
    vampytest.assert_eq(output, slash_command_parameter_auto_completer)


def test__SlashCommandParameterAutoCompleter__bind_parent__no_old_parent():
    """
    Tests whether ``SlashCommandParameterAutoCompleter._bind_parent`` works as intended.
    
    Case: No old parent.
    """
    async def function(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    deepness = 2
    old_parent = None
    new_parent = SlashCommand(None, 'yuuka')
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, old_parent,
    )
    
    output = slash_command_parameter_auto_completer._bind_parent(new_parent)
    _assert_fields_set(output)
    vampytest.assert_eq(output._parent_reference, new_parent.get_self_reference())
    vampytest.assert_is(output, slash_command_parameter_auto_completer)
    vampytest.assert_eq(output, slash_command_parameter_auto_completer)


def test__SlashCommandParameterAutoCompleter__bind_parent__with_old_parent():
    """
    Tests whether ``SlashCommandParameterAutoCompleter._bind_parent`` works as intended.
    
    Case: With old parent.
    """
    async def function(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    deepness = 2
    old_parent = SlashCommand(None, 'okuu')
    new_parent = SlashCommand(None, 'yuuka')
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, old_parent,
    )
    
    output = slash_command_parameter_auto_completer._bind_parent(new_parent)
    _assert_fields_set(output)
    vampytest.assert_eq(output._parent_reference, new_parent.get_self_reference())
    vampytest.assert_not_is(output, slash_command_parameter_auto_completer)
    vampytest.assert_eq(output, slash_command_parameter_auto_completer)


def _iter_options__is_deeper_than():
    yield APPLICATION_COMMAND_FUNCTION_DEEPNESS, APPLICATION_COMMAND_FUNCTION_DEEPNESS, False
    yield APPLICATION_COMMAND_FUNCTION_DEEPNESS, 2, True
    yield 2, APPLICATION_COMMAND_FUNCTION_DEEPNESS, False
    yield 2, 2, False
    yield 2, 1, True
    yield 1, 1, False
    yield 1, 2, False


@vampytest._(vampytest.call_from(_iter_options__is_deeper_than()).returning_last())
def test__SlashCommandParameterAutoCompleter__is_deeper_than(deepness_0, deepness_1):
    """
    Tests whether ``SlashCommandParameterAutoCompleter._is_deeper_than`` works as intended.
    
    Parameters
    ----------
    deepness_0 : `int`
        Deepness to create instance with.
    
    deepness_1 : `int`
        Deepness to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    async def function(value):
        return None
    
    parameter_names = ['hey_mister', 'hey-sister']
    parent = None
    
    slash_command_parameter_auto_completer_0 = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness_0, parent,
    )
    
    slash_command_parameter_auto_completer_1 = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness_1, parent,
    )
    
    output = slash_command_parameter_auto_completer_0._is_deeper_than(slash_command_parameter_auto_completer_1)
    vampytest.assert_instance(output, bool)
    return output


# skip _difference_match_parameters


def test__SlashCommandParameterAutoCompleter__get_command_function():
    """
    Tests whether ``SlashCommandParameterAutoCompleter.get_command_function`` works as intended.
    """
    async def function():
        pass
    
    parameter_names = ['hey_mister', 'hey-sister']
    parent = None
    deepness = 2
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, parent
    )
    
    output = slash_command_parameter_auto_completer.get_command_function()
    vampytest.assert_instance(output, object)
    vampytest.assert_is(output, function)


def test__SlashCommandParameterAutoCompleter__error():
    """
    Tests whether ``SlashCommandParameterAutoCompleter.error`` works as intended.
    """
    async def function():
        pass
    
    parameter_names = ['hey_mister', 'hey-sister']
    parent = None
    deepness = 2
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    slash_command_parameter_auto_completer = SlashCommandParameterAutoCompleter(
        function, parameter_names, deepness, parent
    )
    slash_command_parameter_auto_completer.error(exception_handler)
    
    vampytest.assert_eq(slash_command_parameter_auto_completer._exception_handlers, [exception_handler])
