import vampytest

from types import FunctionType

from ..loading import DotEnvResult, load_dot_env_from_file


def test__load_dot_env_from_file():
    """
    Tests whether ``load_dot_env_from_file`` works as intended.
    """
    open_called = False
    
    file_path = 'test_path'
    file_content = 'a=b\nc=d'
    
    expected_variables = {
        'a': 'b',
        'c': 'd',
    }
    
    class open:
        def __init__(self, input_path, mode):
            nonlocal open_called
            open_called = True
            
            vampytest.assert_eq(input_path, file_path)
            vampytest.assert_eq(mode, 'r')
        
        def __enter__(self):
            return self
        
        def __exit__(self, exception_type, exception_value, exception_traceback):
            return False
        
        def read(self):
            return file_content
    
    
    load_dot_env_from_file_copy = FunctionType(
        load_dot_env_from_file.__code__,
        {
            **load_dot_env_from_file.__globals__,
            'open': open,
        },
        load_dot_env_from_file.__name__,
        load_dot_env_from_file.__defaults__,
        load_dot_env_from_file.__closure__,
    )
    
    output = load_dot_env_from_file_copy(file_path)
    
    vampytest.assert_true(open_called)
    
    vampytest.assert_instance(output, DotEnvResult)
    vampytest.assert_eq(output.variables, expected_variables)
    vampytest.assert_eq(output.file_path, file_path)
