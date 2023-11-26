from types import FunctionType

import vampytest

from ..exception_handler import validate_exception_handler


def _iter_options__passing():
    # Exact
    async def _test_function__passing__0(client, interaction_event, command, exception):
        return True
    
    yield _test_function__passing__0, _test_function__passing__0
    
    # Extra but with default
    async def _test_function__passing__1(client, interaction_event, command, exception = None, fumo = None):
        return True
    
    yield _test_function__passing__1, _test_function__passing__1
    
    # Extra positional
    async def _test_function__passing__2(*positional_parameters):
        return True

    yield _test_function__passing__2, _test_function__passing__2


def _iter_options__type_error():
    # not function
    yield object()
    
    # not funtion
    yield None
    
    # generic function
    def _test_function__type_error__0(client, interaction_event, command, exception):
        return True
    
    yield _test_function__type_error__0
    
    # generator function
    def _test_function__type_error__1(client, interaction_event, command, exception):
        return True
        yield
    
    yield _test_function__type_error__1
    
    # coroutine generator function
    async def _test_function__type_error__2(client, interaction_event, command, exception):
        return
        yield
    
    yield _test_function__type_error__2
    
    # too less parameters
    async def _test_function__type_error__3(client, interaction_event, command):
        return True
    
    yield _test_function__type_error__3
    
    # too much parameters
    async def _test_function__type_error__4(client, interaction_event, command, exception, fumo):
        return True
    
    yield _test_function__type_error__4


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_exception_handler(input_value):
    """
    Tests whether ``validate_exception_handler`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test with.
    
    Returns
    -------
    output : `CoroutineFunctionType`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_exception_handler(input_value)
    vampytest.assert_instance(output, FunctionType)
    return output
