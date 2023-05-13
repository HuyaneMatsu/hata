import vampytest

from types import FunctionType

from ..loading import load_dot_env_file


def test__load_dot_env_file__0():
    """
    Tests whether ``load_dot_env_file`` works as intended.
    
    Case: file not found.
    """
    open_called = False
    
    def open():
        nonlocal open_called
        open_called = True
        raise RuntimeError()
    
    find_dot_env_file = lambda : None
    
    load_dot_env_file_copy = FunctionType(
        load_dot_env_file.__code__,
        {**load_dot_env_file.__globals__, 'find_dot_env_file': find_dot_env_file, 'open': open},
        load_dot_env_file.__name__,
        load_dot_env_file.__defaults__,
        load_dot_env_file.__closure__,
    )
    
    load_dot_env_file_copy()
    
    vampytest.assert_false(open_called)


def test__load_dot_env_file__1():
    """
    Tests whether ``load_dot_env_file`` works as intended.
    
    Case: file found.
    """
    open_called = False
    insert_variables_called = False
    
    path = 'test_path'
    file_content = 'a=b\nc=d'
    
    expected_variables = {
        'a': 'b',
        'c': 'd',
    }
    
    class open:
        def __init__(self, input_path, mode):
            nonlocal open_called
            open_called = True
            
            vampytest.assert_eq(input_path, path)
            vampytest.assert_eq(mode, 'r')
        
        def __enter__(self):
            return self
        
        def __exit__(self, exception_type, exception_value, exception_traceback):
            return False
        
        def read(self):
            return file_content
    
    find_dot_env_file = lambda : path
    
    def insert_variables(variables):
        nonlocal insert_variables_called
        insert_variables_called = True
        
        vampytest.assert_eq(variables, expected_variables)
    
    load_dot_env_file_copy = FunctionType(
        load_dot_env_file.__code__,
        {
            **load_dot_env_file.__globals__,
            'find_dot_env_file': find_dot_env_file,
             'insert_variables': insert_variables,
            'open': open,
        },
        load_dot_env_file.__name__,
        load_dot_env_file.__defaults__,
        load_dot_env_file.__closure__,
    )
    
    load_dot_env_file_copy()
    
    vampytest.assert_true(open_called)
    vampytest.assert_true(insert_variables_called)
