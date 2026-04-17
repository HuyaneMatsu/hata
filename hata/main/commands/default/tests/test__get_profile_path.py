from os.path import join as join_paths

import vampytest

from ..profiling import get_profile_path


def test__get_profile_path():
    """
    Tests whether ``get_profile_path`` works as intended.
    """
    directory_name = '.profiles'
    directory_path = join_paths('root', 'pudding', directory_name)
    
    files = {
        join_paths(directory_path, value) for value in
        ('latest.prof',)
    }
    
    def mock_absolute_path(value):
        nonlocal directory_name
        nonlocal directory_path
        vampytest.assert_eq(value, directory_name)
        return directory_path
    
    
    def mock_is_file(value):
        nonlocal files
        
        if value in files:
            return True
        
        return False
    
    
    mocked = vampytest.mock_globals(
        get_profile_path,
        absolute_path = mock_absolute_path,
        is_file = mock_is_file,
    )
    
    output = mocked('latest')
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, join_paths(directory_path, 'latest.prof'))
    
    output = mocked('puddings')
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, None)
