from datetime import datetime as DateTime
from os.path import join as join_paths

import vampytest

from ..profiling import get_profile_names


def test__get_profile_names():
    """
    Tests whether ``get_profile_names`` works as intended.
    """
    directory_name = '.profiles'
    directory_path = join_paths('root', 'pudding', directory_name)
    
    files = {
        join_paths(directory_path, value) for value in
        ('pudding', 'latest.prof', '2024_03_10_18_29_48.prof', '2024_03_10_19_11_32.prof', '2024_03_10_19_31_03.prof',)
    }
    directories = {
        join_paths(directory_path, value) for value in
        ('puddings', )
    }
    
    directory_content = [
        'pudding', 'puddings', '2024_03_10_18_29_48.prof', '2024_03_10_19_11_32.prof', '2024_03_10_19_31_03.prof',
        'latest.prof',
    ]
    
    creations = {
        join_paths(directory_path,              'latest.prof') : DateTime(2024, 3, 10, 19, 31,  3),
        join_paths(directory_path, '2024_03_10_19_31_03.prof') : DateTime(2024, 3, 10, 19, 31,  3),
        join_paths(directory_path, '2024_03_10_19_11_32.prof') : DateTime(2024, 3, 10, 19, 11, 32),
        join_paths(directory_path, '2024_03_10_18_29_48.prof') : DateTime(2024, 3, 10, 18, 29, 48),
    }
    
    
    def mock_is_directory(value):
        vampytest.assert_eq(value, directory_path)
        return True
    
    
    def mock_absolute_path(value):
        nonlocal directory_name
        nonlocal directory_path
        vampytest.assert_eq(value, directory_name)
        return directory_path
    
    
    def mock_list_directory(value):
        nonlocal directory_path
        nonlocal directory_content
        vampytest.assert_eq(value, directory_path)
        return directory_content.copy()
    
    
    def mock_is_file(value):
        nonlocal files
        nonlocal directories
        
        if value in files:
            return True
        
        if value in directories:
            return False
        
        raise RuntimeError
    
    
    def mock_get_creation_time(value):
        nonlocal creations
        try:
            return creations[value]
        except KeyError as exception:
            raise RuntimeError from exception
    
    
    mocked = vampytest.mock_globals(
        get_profile_names,
        is_directory = mock_is_directory,
        absolute_path = mock_absolute_path,
        list_directory = mock_list_directory,
        is_file = mock_is_file,
        get_creation_time = mock_get_creation_time,
    )
    
    output = mocked()
    
    vampytest.assert_instance(output, list)
    for value in output:
        vampytest.assert_instance(value, str)
    
    vampytest.assert_eq(
        output,
        [
            'latest',
            '2024_03_10_19_31_03',
            '2024_03_10_19_11_32',
            '2024_03_10_18_29_48',
        ]
    )
