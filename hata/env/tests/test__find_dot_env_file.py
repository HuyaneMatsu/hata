import vampytest

from os.path import join as join_paths
from types import FunctionType

from ..loading import find_dot_env_file


def test__find_dot_env_file__0():
    """
    Tests whether ``find_dot_env_file`` works as intended.
    
    Case: Launched location is `None`.
    """
    find_launched_location = lambda : None
    
    expected_output = None
    
    find_dot_env_file_copy = FunctionType(
        find_dot_env_file.__code__,
        {**find_dot_env_file.__globals__, 'find_launched_location': find_launched_location},
        find_dot_env_file.__name__,
        find_dot_env_file.__defaults__,
        find_dot_env_file.__closure__,
    )
    
    output = find_dot_env_file_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)


def test__find_dot_env_file__1():
    """
    Tests whether ``find_dot_env_file`` works as intended.
    
    Case: Env file not exists.
    """
    base_location = 'test'
    find_launched_location = lambda : join_paths(base_location, '__init__.py')
    is_file = lambda path : False
    
    expected_output = None
    
    
    find_dot_env_file_copy = FunctionType(
        find_dot_env_file.__code__,
        {**find_dot_env_file.__globals__, 'find_launched_location': find_launched_location, 'is_file': is_file},
        find_dot_env_file.__name__,
        find_dot_env_file.__defaults__,
        find_dot_env_file.__closure__,
    )
    
    output = find_dot_env_file_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)


def test__find_dot_env_file__2():
    """
    Tests whether ``find_dot_env_file`` works as intended.
    
    Case: Env file exists.
    """
    base_location = 'test'
    find_launched_location = lambda : join_paths(base_location, '__init__.py')
    is_file = lambda path : True
    
    expected_output = join_paths(base_location, '.env')
    
    find_dot_env_file_copy = FunctionType(
        find_dot_env_file.__code__,
        {**find_dot_env_file.__globals__, 'find_launched_location': find_launched_location, 'is_file': is_file},
        find_dot_env_file.__name__,
        find_dot_env_file.__defaults__,
        find_dot_env_file.__closure__,
    )
    
    output = find_dot_env_file_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)
