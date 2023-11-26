import vampytest

from ..autocomplete import _register_auto_completer, AutocompleteInterface


class TestAutocompleteInterface(AutocompleteInterface):
    __slots__ = (
        'register_called', 'register_called_with_function', 'register_called_with_parameter_names', 'register_output'
    )
    
    def __new__(cls, register_output):
        self = object.__new__(cls)
        self.register_called = False
        self.register_called_with_function = None
        self.register_called_with_parameter_names = None
        self.register_output = register_output
        return self
    
    
    def _register_auto_completer(self, function, parameter_names):
        self.register_called = True
        self.register_called_with_function = function
        self.register_called_with_parameter_names = parameter_names
        return self.register_output


def test___register_auto_completer__registering():
    """
    Tests whether ``_register_auto_completer`` works as intended.
    
    Case: registering.
    """
    expected_output = object()
    parameter_names = ['koishi', 'satori']
    parent = TestAutocompleteInterface(expected_output)
    
    async def auto_complete_function(value):
        pass
    
    output = _register_auto_completer(parent, parameter_names.copy(), auto_complete_function)
    
    vampytest.assert_is(output, expected_output)
    
    vampytest.assert_eq(parent.register_called, True)
    vampytest.assert_is(parent.register_called_with_function, auto_complete_function)
    vampytest.assert_eq(parent.register_called_with_parameter_names, parameter_names)
