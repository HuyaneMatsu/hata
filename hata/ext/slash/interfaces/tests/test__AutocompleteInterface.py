import vampytest

from ...command import SlashCommandParameterAutoCompleter

from ..autocomplete import AutocompleteInterface


class TestAutocompleteInterface(AutocompleteInterface):
    __slots__ = ('_auto_completers',)
    
    def __new__(cls):
        self = object.__new__(cls)
        self._auto_completers = None
        return self


def test__AutocompleteInterface__make_auto_completer__default():
    """
    Tests whether ``AutocompleteInterface._make_auto_completer`` works as intended.
    
    Case: Default.
    """
    async def autocomplete_function(value):
        pass
    
    parameter_names = ['koishi', 'satori']
    
    auto_completer = TestAutocompleteInterface()._make_auto_completer(autocomplete_function, parameter_names)
    
    vampytest.assert_instance(auto_completer, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(auto_completer._command_function, autocomplete_function)
    vampytest.assert_eq(auto_completer.name_pairs, frozenset((('koishi', 'koishi'), ('satori', 'satori'))))


def test__AutocompleteInterface__make_auto_completer__re_pass():
    """
    Tests whether ``AutocompleteInterface._make_auto_completer`` works as intended.
    
    Case: Re-passing.
    """
    async def autocomplete_function(value):
        pass
    
    parameter_names = ['koishi', 'satori']
    
    test_auto_completer = TestAutocompleteInterface()._make_auto_completer(autocomplete_function, parameter_names)
    auto_completer = TestAutocompleteInterface()._make_auto_completer(test_auto_completer, parameter_names)
    
    vampytest.assert_instance(auto_completer, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(auto_completer._command_function, autocomplete_function)
    vampytest.assert_eq(auto_completer.name_pairs, frozenset((('koishi', 'koishi'), ('satori', 'satori'))))


def test__AutocompleteInterface__store_auto_completer():
    """
    Tests whether ``AutocompleteInterface._store_auto_completer`` works as intended.
    """
    async def autocomplete_function_0(value):
        pass
    
    async def autocomplete_function_1(value):
        pass
    
    parameter_names_0 = ['koishi', 'satori']
    parameter_names_1 = ['nue']
    
    interface = TestAutocompleteInterface()
    
    auto_completer_0 = interface._make_auto_completer(autocomplete_function_0, parameter_names_0)
    output = interface._store_auto_completer(auto_completer_0)
    vampytest.assert_eq(output, (True, auto_completer_0))
    
    vampytest.assert_eq(interface._auto_completers, [auto_completer_0])


    auto_completer_1 = interface._make_auto_completer(autocomplete_function_1, parameter_names_1)
    output = interface._store_auto_completer(auto_completer_1)
    vampytest.assert_eq(output, (True, auto_completer_1))
    
    vampytest.assert_eq(interface._auto_completers, [auto_completer_0, auto_completer_1])


def test__AutocompleteInterface__register_auto_completer():
    """
    Tests whether ``AutocompleteInterface._register_auto_completer`` works as intended.
    """
    interface = TestAutocompleteInterface()
    
    async def autocomplete_function(value):
        pass
    
    parameter_names = ['koishi', 'satori']
    
    auto_completer = interface._register_auto_completer(autocomplete_function, parameter_names)
    
    vampytest.assert_instance(auto_completer, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(auto_completer._command_function, autocomplete_function)
    vampytest.assert_eq(auto_completer.name_pairs, frozenset((('koishi', 'koishi'), ('satori', 'satori'))))
    
    vampytest.assert_eq(interface._auto_completers, [auto_completer])


def test__TestAutocompleteInterface__autocomplete__function_given():
    """
    Tests whether ``TestAutocompleteInterface.autocomplete`` works as intended.
    
    Case: Function given.
    """
    interface = TestAutocompleteInterface()
    
    async def autocomplete_function(value):
        pass
    
    parameter_names = ['koishi', 'satori']
    
    auto_completer = interface.autocomplete(*parameter_names, function = autocomplete_function)
    
    vampytest.assert_instance(auto_completer, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(auto_completer._command_function, autocomplete_function)
    vampytest.assert_eq(auto_completer.name_pairs, frozenset((('koishi', 'koishi'), ('satori', 'satori'))))
    
    vampytest.assert_eq(interface._auto_completers, [auto_completer])


def test__TestAutocompleteInterface__autocomplete__decoration():
    """
    Tests whether ``TestAutocompleteInterface.autocomplete`` works as intended.
    
    Case: Decorator.
    """
    interface = TestAutocompleteInterface()
    
    async def autocomplete_function(value):
        pass
    
    parameter_names = ['koishi', 'satori']
    
    auto_completer = interface.autocomplete(*parameter_names)(autocomplete_function)
    
    vampytest.assert_instance(auto_completer, SlashCommandParameterAutoCompleter)
    vampytest.assert_is(auto_completer._command_function, autocomplete_function)
    vampytest.assert_eq(auto_completer.name_pairs, frozenset((('koishi', 'koishi'), ('satori', 'satori'))))
    
    vampytest.assert_eq(interface._auto_completers, [auto_completer])


def test__TestAutocompleteInterface__autocomplete__decoration_with_none():
    """
    Tests whether ``TestAutocompleteInterface.autocomplete`` works as intended.
    
    Case: Decorator but passing `None`.
    """
    interface = TestAutocompleteInterface()
    
    parameter_names = ['koishi', 'satori']
    
    with vampytest.assert_raises(TypeError):
        interface.autocomplete(*parameter_names)(None)
