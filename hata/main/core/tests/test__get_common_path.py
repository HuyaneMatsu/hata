import vampytest

from ..helpers import get_common_path


def test__get_common_path__passing():
    """
    Tests whether ``get_common_path`` works as intended.
    
    Case: passing.
    """
    path_0 = '/pudding/eater'
    path_1 = '/pudding/consumed'
    path_output = '/pudding'
    inputted_paths = None
    
    def mock_get_common_path(input_paths):
        nonlocal inputted_paths
        nonlocal path_output
        inputted_paths = input_paths
        return path_output
    
    mocked = vampytest.mock_globals(get_common_path, _get_common_path = mock_get_common_path)
    
    output = mocked((path_0, path_1),)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, path_output)
    
    vampytest.assert_eq(inputted_paths, (path_0, path_1))


def test__get_common_path__value_error_drive():
    """
    Tests whether ``get_common_path`` works as intended.
    Case: value error, different drive.
    """
    path_0 = '/pudding/eater'
    path_1 = '/pudding/consumed'
    inputted_paths = None
    exception = ValueError('Paths don\'t have the same drive')
    
    def mock_get_common_path(input_paths):
        nonlocal inputted_paths
        nonlocal exception
        inputted_paths = input_paths
        raise exception
    
    mocked = vampytest.mock_globals(get_common_path, _get_common_path = mock_get_common_path)
    
    output = mocked((path_0, path_1),)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, '')
    
    vampytest.assert_eq(inputted_paths, (path_0, path_1))


def test__get_common_path__value_error_other():
    """
    Tests whether ``get_common_path`` works as intended.
    Case: value error, different drive.
    """
    path_0 = '/pudding/eater'
    path_1 = '/pudding/consumed'
    inputted_paths = None
    exception = ValueError('something else')
    
    def mock_get_common_path(input_paths):
        nonlocal inputted_paths
        nonlocal exception
        inputted_paths = input_paths
        raise exception
    
    mocked = vampytest.mock_globals(get_common_path, _get_common_path = mock_get_common_path)
    
    with vampytest.assert_raises(exception):
        mocked((path_0, path_1),)
    
    vampytest.assert_eq(inputted_paths, (path_0, path_1))
