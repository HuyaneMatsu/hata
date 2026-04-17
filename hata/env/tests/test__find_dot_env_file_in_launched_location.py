import vampytest

from os.path import join as join_paths
from types import FunctionType

from ..loading import find_dot_env_file_in_launched_location


def test__find_dot_env_file_in_launched_location__none():
    """
    Tests whether ``find_dot_env_file_in_launched_location`` works as intended.
    
    Case: Launched location is `None`.
    """
    find_launched_location = lambda : None
    
    expected_output = None
    
    find_dot_env_file_in_launched_location_copy = FunctionType(
        find_dot_env_file_in_launched_location.__code__,
        {**find_dot_env_file_in_launched_location.__globals__, 'find_launched_location': find_launched_location},
        find_dot_env_file_in_launched_location.__name__,
        find_dot_env_file_in_launched_location.__defaults__,
        find_dot_env_file_in_launched_location.__closure__,
    )
    
    output = find_dot_env_file_in_launched_location_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)


def test__find_dot_env_file_in_launched_location__not_exists():
    """
    Tests whether ``find_dot_env_file_in_launched_location`` works as intended.
    
    Case: Env file not exists.
    """
    base_location = 'test'
    find_launched_location = lambda : join_paths(base_location, '__init__.py')
    is_file = lambda path : False
    
    expected_output = None
    
    
    find_dot_env_file_in_launched_location_copy = FunctionType(
        find_dot_env_file_in_launched_location.__code__,
        {**find_dot_env_file_in_launched_location.__globals__, 'find_launched_location': find_launched_location, 'is_file': is_file},
        find_dot_env_file_in_launched_location.__name__,
        find_dot_env_file_in_launched_location.__defaults__,
        find_dot_env_file_in_launched_location.__closure__,
    )
    
    output = find_dot_env_file_in_launched_location_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)


def test__find_dot_env_file_in_launched_location__exists():
    """
    Tests whether ``find_dot_env_file_in_launched_location`` works as intended.
    
    Case: Env file exists.
    """
    base_location = 'test'
    find_launched_location = lambda : join_paths(base_location, '__init__.py')
    is_file = lambda path : True
    
    expected_output = join_paths(base_location, '.env')
    
    find_dot_env_file_in_launched_location_copy = FunctionType(
        find_dot_env_file_in_launched_location.__code__,
        {**find_dot_env_file_in_launched_location.__globals__, 'find_launched_location': find_launched_location, 'is_file': is_file},
        find_dot_env_file_in_launched_location.__name__,
        find_dot_env_file_in_launched_location.__defaults__,
        find_dot_env_file_in_launched_location.__closure__,
    )
    
    output = find_dot_env_file_in_launched_location_copy()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, expected_output)
