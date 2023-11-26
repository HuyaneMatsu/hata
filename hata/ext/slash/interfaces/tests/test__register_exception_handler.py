import vampytest

from ..exception_handler import _register_exception_handler, ExceptionHandlerInterface


class TestExceptionHandlerInterface(ExceptionHandlerInterface):
    __slots__ = (
        'register_called', 'register_called_with_function', 'register_called_with_first', 'register_output'
    )
    
    def __new__(cls, register_output):
        self = object.__new__(cls)
        self.register_called = False
        self.register_called_with_function = None
        self.register_called_with_first = None
        self.register_output = register_output
        return self
    
    
    def _register_exception_handler(self, function, first):
        self.register_called = True
        self.register_called_with_function = function
        self.register_called_with_first = first
        return self.register_output


def test__register_exception_handler__registering():
    """
    Tests whether ``_register_exception_handler`` works as intended.
    
    Case: registering.
    """
    expected_output = object()
    first = True
    parent = TestExceptionHandlerInterface(expected_output)
    
    async def exception_handler_function(value):
        pass
    
    output = _register_exception_handler(parent, first, exception_handler_function)
    
    vampytest.assert_is(output, expected_output)
    
    vampytest.assert_eq(parent.register_called, True)
    vampytest.assert_is(parent.register_called_with_function, exception_handler_function)
    vampytest.assert_eq(parent.register_called_with_first, first)
