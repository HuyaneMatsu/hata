from os.path import join as join_paths
from types import FunctionType

import vampytest

from ..helpers import create_directory_recursive


def test__create_directory_recursive():
    """
    Tests whether ``create_directory_recursive`` works as intended.
    """
    base = 'aya'
    parts = ['nue', 'Hatate']
    created_directories = []
    
    def create_directory(directory):
        nonlocal created_directories
        created_directories.append(directory)
    
    create_directory_recursive_copy = FunctionType(
        create_directory_recursive.__code__,
        {
            **create_directory_recursive.__globals__,
            'exists': lambda x: x == base,
            'create_directory': create_directory,
        },
        create_directory_recursive.__name__,
        create_directory_recursive.__defaults__,
        create_directory_recursive.__closure__,
    )
    
    create_directory_recursive_copy(join_paths(base, *parts))
    
    vampytest.assert_eq(
        created_directories,
        [
            join_paths(base, *parts[:1]),
            join_paths(base, *parts[:2]),
        ],
    )
