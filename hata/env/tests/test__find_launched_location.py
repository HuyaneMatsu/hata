import sys
from os.path import dirname as get_directory_name, join as join_paths

import vampytest

from ..loading import find_launched_location


def test__find_launched_location():
    """
    Tests whether ``find_launched_location`` works as intended.
    """
    expected_location = join_paths(get_directory_name(sys.modules['vampytest'].__spec__.origin), '__main__.py')
    output = find_launched_location()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(expected_location, find_launched_location())
