import vampytest

from ..exception_handler import ExceptionHandlerInterface


class TestExceptionHandlerInterface(ExceptionHandlerInterface):
    __slots__ = ('_exception_handlers',)
    
    def __new__(cls):
        self = object.__new__(cls)
        self._exception_handlers = None
        return self


def test__ExceptionHandlerInterface__store_exception_handler():
    """
    Tests whether ``ExceptionHandlerInterface._store_exception_handler`` works as intended.
    """
    async def exception_handler_function_0(client, interaction_event, command, exception):
        pass
    
    async def exception_handler_function_1(client, interaction_event, command, exception):
        pass
    
    async def exception_handler_function_2(client, interaction_event, command, exception):
        pass
    
    interface = TestExceptionHandlerInterface()
    
    output = interface._store_exception_handler(exception_handler_function_0, False)
    vampytest.assert_eq(output, (True, exception_handler_function_0))
    
    vampytest.assert_eq(interface._exception_handlers, [exception_handler_function_0])

    output = interface._store_exception_handler(exception_handler_function_1, False)
    vampytest.assert_eq(output, (True, exception_handler_function_1))
    
    vampytest.assert_eq(interface._exception_handlers, [exception_handler_function_0, exception_handler_function_1])

    output = interface._store_exception_handler(exception_handler_function_2, True)
    vampytest.assert_eq(output, (True, exception_handler_function_2))
    
    vampytest.assert_eq(
        interface._exception_handlers,
        [exception_handler_function_2, exception_handler_function_0, exception_handler_function_1],
    )


def test__ExceptionHandlerInterface__register_exception_handler():
    """
    Tests whether ``ExceptionHandlerInterface._register_exception_handler`` works as intended.
    """
    interface = TestExceptionHandlerInterface()
    
    async def exception_handler_function(client, interaction_event, command, exception):
        pass
    
    exception_handler = interface._register_exception_handler(exception_handler_function, False)
    
    vampytest.assert_is(exception_handler, exception_handler_function)
    
    vampytest.assert_eq(interface._exception_handlers, [exception_handler])


def test__ExceptionHandlerInterface__register_exception_handler__invalid_type():
    """
    Tests whether ``ExceptionHandlerInterface._register_exception_handler`` works as intended.
    """
    interface = TestExceptionHandlerInterface()
    
    with vampytest.assert_raises(TypeError):
        interface._register_exception_handler(object(), False)



def test__TestExceptionHandlerInterface__error__function_given():
    """
    Tests whether ``TestExceptionHandlerInterface.error`` works as intended.
    
    Case: Function given.
    """
    interface = TestExceptionHandlerInterface()
    
    async def exception_handler_function(client, interaction_event, command, exception):
        pass
    
    exception_handler = interface.error(exception_handler_function, first = True)
    
    vampytest.assert_is(exception_handler, exception_handler_function)
    
    vampytest.assert_eq(interface._exception_handlers, [exception_handler])


def test__TestExceptionHandlerInterface__error__decoration():
    """
    Tests whether ``TestExceptionHandlerInterface.error`` works as intended.
    
    Case: Decorator.
    """
    interface = TestExceptionHandlerInterface()
    
    async def exception_handler_function(client, interaction_event, command, exception):
        pass
    
    exception_handler = interface.error(first = True)(exception_handler_function)
    
    vampytest.assert_is(exception_handler, exception_handler_function)
    
    vampytest.assert_eq(interface._exception_handlers, [exception_handler_function])


def test__TestExceptionHandlerInterface__error__decoration_with_none():
    """
    Tests whether ``TestExceptionHandlerInterface.error`` works as intended.
    
    Case: Decorator but passing `None`.
    """
    interface = TestExceptionHandlerInterface()
    
    with vampytest.assert_raises(TypeError):
        interface.error(first = True)(None)
