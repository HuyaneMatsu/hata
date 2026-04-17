from os.path import join as join_paths
from types import FunctionType

import vampytest

from ..structure import create_file


def test__create_file():
    """
    Tests whether ``create_file`` works as intended.
    """
    open_called = False
    write_called = False
    
    directory_path = 'aya'
    file_name = 'ya'
    expected_path = join_paths(directory_path, file_name)
    content_input = 'hey mister'
    
    class open:
        def __init__(self, input_path, mode, *, encoding):
            nonlocal open_called
            nonlocal expected_path
            vampytest.assert_in(encoding, ('utf-8', 'utf8'))
            open_called = True
            
            vampytest.assert_eq(input_path, expected_path)
            vampytest.assert_eq(mode, 'w')
        
        def __enter__(self):
            return self
        
        def __exit__(self, exception_type, exception_value, exception_traceback):
            return False
        
        def write(self, content):
            nonlocal write_called
            nonlocal content_input
            
            write_called = True
            
            vampytest.assert_instance(content, str)
            vampytest.assert_eq(content, content_input)
    
    
    create_file_copy = FunctionType(
        create_file.__code__,
        {
            **create_file.__globals__,
            'open': open,
        },
        create_file.__name__,
        create_file.__defaults__,
        create_file.__closure__,
    )
    
    create_file_copy(directory_path, file_name, content_input)
    
    vampytest.assert_true(open_called)
    vampytest.assert_true(write_called)
