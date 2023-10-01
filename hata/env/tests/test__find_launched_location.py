import sys
from os import getlogin as get_login
from os.path import dirname as get_directory_name, join as join_paths, sep as PATH_SEPARATOR

import vampytest

from ..loading import find_launched_location


def test__find_launched_location():
    """
    Tests whether ``find_launched_location`` works as intended.
    """
    expected_location_0 = join_paths(get_directory_name(sys.modules['vampytest'].__spec__.origin), '__main__.py')
    expected_location_1 = join_paths(PATH_SEPARATOR, 'home', get_login(), '.local', 'bin', 'vampytest')
    
    output = find_launched_location()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_in(find_launched_location(), (expected_location_0, expected_location_1))
