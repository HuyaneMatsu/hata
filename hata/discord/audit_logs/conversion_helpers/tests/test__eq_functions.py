import vampytest

from ..helpers import _eq_functions


def _iter_options():
    def test_function_0():
        value = 6
        return value
    
    def test_function_1():
        value = 6
        return value

    def test_function_2():
        value = 5
        return value
    
    
    yield test_function_0, test_function_0, True
    yield test_function_0, test_function_1, True
    yield test_function_0, test_function_2, False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__eq_functions(function_0, function_1):
    """
    Tests whether ``_eq_functions`` works as intended.
    
    Parameters
    ----------
    function_0 : `FunctionType | MethodType`
        Function to equal with.
    function_1 : `FunctionType | MethodType`
        Function to equal with.
    
    Returns
    -------
    output : `bool`
    """
    output = _eq_functions(function_0, function_1)
    vampytest.assert_instance(output, bool)
    return output
