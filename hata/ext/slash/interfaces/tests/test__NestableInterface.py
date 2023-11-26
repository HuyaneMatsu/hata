from types import FunctionType

import vampytest

from ..nestable import NestableInterface


class TestCommand:
    __slots__ = ('_command_function',)
    
    def __new__(cls, function):
        self = object.__new__(cls)
        self._command_function = function
        return self


class TestNestableInterface(NestableInterface):
    __slots__ = ('registered', 'nestable')
    
    def __new__(cls, nestable):
        self = object.__new__(cls)
        self.registered = []
        self.nestable = nestable
        return self
    
    
    def _is_nestable(self):
        return self.nestable
    
    
    def _store_command_instance(self, function):
        if isinstance(function, TestCommand):
            self.registered.append(function)
            return True, function
        
        return False, None
    
    
    def _make_command_instance_from_parameters(self, function, positional_parameters, keyword_parameters):
        if not isinstance(function, FunctionType):
            raise TypeError
        
        return TestCommand(function)


def test__NestableInterface__store_command_instance__success():
    """
    Tests whether ``NestableInterface._store_command_instance`` works as intended.
    
    Case: success.
    """
    interface = TestNestableInterface(True)
    
    async def command_function():
        pass
    
    command = TestCommand(command_function)
    
    output = interface._store_command_instance(command)
    vampytest.assert_eq(output, (True, command))
    vampytest.assert_eq(interface.registered, [command])


def test__NestableInterface__store_command_instance__failure():
    """
    Tests whether ``NestableInterface._store_command_instance`` works as intended.
    
    Case: success.
    """
    interface = TestNestableInterface(True)
    command = object()
    
    output = interface._store_command_instance(command)
    vampytest.assert_eq(output, (False, None))


def test__NestableInterface__make_command_instance_from_parameters():
    """
    Tests whether ``NestableInterface._make_command_instance_from_parameters`` works as intended.
    """
    interface = TestNestableInterface(True)
    
    async def command_function():
        pass
    
    output = interface._make_command_instance_from_parameters(command_function, (), {})
    vampytest.assert_instance(output, TestCommand)
    vampytest.assert_is(output._command_function, command_function)



def test__NestableInterface__create_event__first_hit():
    """
    Tests whether ``NestableInterface.create_event`` works as intended.
    
    Case: First hit.
    """
    interface = TestNestableInterface(True)
    
    async def command_function():
        pass
    
    command = TestCommand(command_function)
    
    output = interface.create_event(command)
    vampytest.assert_is(output, command)
    vampytest.assert_eq(interface.registered, [command])


def test__NestableInterface__create_event__second_hit():
    """
    Tests whether ``NestableInterface.create_event`` works as intended.
    
    Case: Second hit.
    """
    interface = TestNestableInterface(True)
    
    async def command_function():
        pass
    
    output = interface.create_event(command_function)
    vampytest.assert_instance(output, TestCommand)
    vampytest.assert_is(output._command_function, command_function)
    vampytest.assert_eq(interface.registered, [output])


def test__NestableInterface__create_event__not_nestable():
    """
    Tests whether ``NestableInterface.create_event`` works as intended.
    
    Case: not nestable.
    """
    interface = TestNestableInterface(False)
    
    async def command_function():
        pass
    
    with vampytest.assert_raises(RuntimeError):
        interface.create_event(command_function)


def test__NestableInterface__interactions__function_given():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: Function given.
    """
    interface = TestNestableInterface(True)
    
    async def command_function():
        pass
    
    command = interface.interactions(function = command_function)
    
    vampytest.assert_instance(command, TestCommand)
    vampytest.assert_is(command._command_function, command_function)
    
    vampytest.assert_eq(interface.registered, [command])


def test__NestableInterface__interactions__decoration():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: Decorator.
    """
    interface = TestNestableInterface(True)
    
    async def command_function():
        pass
    
    command = interface.interactions()(command_function)
    
    vampytest.assert_instance(command, TestCommand)
    vampytest.assert_is(command._command_function, command_function)
    
    vampytest.assert_eq(interface.registered, [command])


def test__NestableInterface__interactions__decoration_with_none():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: Decorator.
    """
    interface = TestNestableInterface(True)
    
    with vampytest.assert_raises(TypeError):
        interface.interactions()(None)


def test__NestableInterface__interactions__not_nestable():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: Not nestable.
    """
    interface = TestNestableInterface(False)
    
    with vampytest.assert_raises(RuntimeError):
        interface.interactions()


def test__NestableInterface__interactions__is_nestable__false():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: false.
    """
    interface = TestNestableInterface(False)
    
    output = interface._is_nestable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__NestableInterface__interactions__is_nestable__true():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: true.
    """
    interface = TestNestableInterface(True)
    
    output = interface._is_nestable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__NestableInterface__interactions__check_supports_nesting__false():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: false.
    """
    interface = TestNestableInterface(False)
    
    with vampytest.assert_raises(RuntimeError):
        interface._check_supports_nesting()


def test__NestableInterface__interactions__check_supports_nesting__true():
    """
    Tests whether ``NestableInterface.interactions`` works as intended.
    
    Case: true.
    """
    interface = TestNestableInterface(True)
    
    interface._check_supports_nesting()
