import vampytest

from os.path import join as join_paths
from types import FunctionType

from ..loading import find_dot_env_file_in_current_working_directory


def test__find_dot_env_file_in_current_working_directory__none():
    """
    Tests whether ``find_dot_env_file_in_current_working_directory`` works as intended.
    
    Case: Launched location is `None`.
    """
    get_current_working_directory = lambda : None
    
    expected_output = None
    
    find_dot_env_file_in_current_working_directory_copy = FunctionType(
        find_dot_env_file_in_current_working_directory.__code__,
        {
            **find_dot_env_file_in_current_working_directory.__globals__,
            'get_current_working_directory': get_current_working_directory,
        },
        find_dot_env_file_in_current_working_directory.__name__,
        find_dot_env_file_in_current_working_directory.__defaults__,
        find_dot_env_file_in_current_working_directory.__closure__,
    )
    
    output = find_dot_env_file_in_current_working_directory_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)


def test__find_dot_env_file_in_current_working_directory__not_exists():
    """
    Tests whether ``find_dot_env_file_in_current_working_directory`` works as intended.
    
    Case: Env file not exists.
    """
    base_location = 'test'
    get_current_working_directory = lambda : join_paths(base_location, '__init__.py')
    is_file = lambda path : False
    
    expected_output = None
    
    
    find_dot_env_file_in_current_working_directory_copy = FunctionType(
        find_dot_env_file_in_current_working_directory.__code__,
        {
            **find_dot_env_file_in_current_working_directory.__globals__,
            'get_current_working_directory': get_current_working_directory,
            'is_file': is_file,
        },
        find_dot_env_file_in_current_working_directory.__name__,
        find_dot_env_file_in_current_working_directory.__defaults__,
        find_dot_env_file_in_current_working_directory.__closure__,
    )
    
    output = find_dot_env_file_in_current_working_directory_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)


def test__find_dot_env_file_in_current_working_directory__exists():
    """
    Tests whether ``find_dot_env_file_in_current_working_directory`` works as intended.
    
    Case: Env file exists.
    """
    base_location = 'test'
    get_current_working_directory = lambda : join_paths(base_location, '__init__.py')
    is_file = lambda path : True
    
    expected_output = join_paths(base_location, '.env')
    
    find_dot_env_file_in_current_working_directory_copy = FunctionType(
        find_dot_env_file_in_current_working_directory.__code__,
        {
            **find_dot_env_file_in_current_working_directory.__globals__,
            'get_current_working_directory': get_current_working_directory,
            'is_file': is_file,
        },
        find_dot_env_file_in_current_working_directory.__name__,
        find_dot_env_file_in_current_working_directory.__defaults__,
        find_dot_env_file_in_current_working_directory.__closure__,
    )
    
    output = find_dot_env_file_in_current_working_directory_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)
