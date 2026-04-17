from os.path import join as join_paths
from types import FunctionType

import vampytest

from ..helpers import _validate_name


def test__validate_name__fail_directory_non_empty():
    """
    Tests whether ``_validate_name`` is working as intended.
    
    Case: Directory but not empty.
    """
    base = 'tengu'
    path = 'aya'
    
    validate_name_copy = FunctionType(
        _validate_name.__code__,
        {
            **_validate_name.__globals__,
            'absolute_path': lambda x: join_paths(base, x),
            'is_directory': lambda x: True,
            'list_directory': lambda x: ['ayaya'],
        },
        _validate_name.__name__,
        _validate_name.__defaults__,
        _validate_name.__closure__,
    )
    
    output = validate_name_copy(path)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_is(output[0], None)
    vampytest.assert_instance(output[1], str)


def test__validate_name__pass_directory_empty():
    """
    Tests whether ``_validate_name`` is working as intended.
    
    Case: Directory and empty.
    """
    base = 'tengu'
    path = 'aya'
    
    validate_name_copy = FunctionType(
        _validate_name.__code__,
        {
            **_validate_name.__globals__,
            'absolute_path': lambda x: join_paths(base, x),
            'is_directory': lambda x: True,
            'list_directory': lambda x: [],
        },
        _validate_name.__name__,
        _validate_name.__defaults__,
        _validate_name.__closure__,
    )
    
    output = validate_name_copy(path)
    vampytest.assert_eq(output, (join_paths(base, path), None))


def test__validate_name__fail_exists_and_not_directory():
    """
    Tests whether ``_validate_name`` is working as intended.
    
    Case: Exists but not a directory.
    """
    base = 'tengu'
    path = 'aya'
    
    validate_name_copy = FunctionType(
        _validate_name.__code__,
        {
            **_validate_name.__globals__,
            'absolute_path': lambda x: join_paths(base, x),
            'is_directory': lambda x: False,
            'exists': lambda x: True,
        },
        _validate_name.__name__,
        _validate_name.__defaults__,
        _validate_name.__closure__,
    )
    
    output = validate_name_copy(path)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_is(output[0], None)
    vampytest.assert_instance(output[1], str)


def test__validate_name__fail_parent_not_directory():
    """
    Tests whether ``_validate_name`` is working as intended.
    
    Case: Parent is not a directory.
    """
    base = 'tengu'
    path = 'aya'
    
    validate_name_copy = FunctionType(
        _validate_name.__code__,
        {
            **_validate_name.__globals__,
            'absolute_path': lambda x: join_paths(base, x),
            'is_directory': lambda x: False,
            'exists': lambda x: x == base,
        },
        _validate_name.__name__,
        _validate_name.__defaults__,
        _validate_name.__closure__,
    )
    
    output = validate_name_copy(path)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_is(output[0], None)
    vampytest.assert_instance(output[1], str)


def test__validate_name__pass_parent_is_directory():
    """
    Tests whether ``_validate_name`` is working as intended.
    
    Case: Parent is a directory.
    """
    base = 'tengu'
    path = 'aya'
    
    validate_name_copy = FunctionType(
        _validate_name.__code__,
        {
            **_validate_name.__globals__,
            'absolute_path': lambda x: join_paths(base, x),
            'is_directory': lambda x: x == base,
            'exists': lambda x: False,
        },
        _validate_name.__name__,
        _validate_name.__defaults__,
        _validate_name.__closure__,
    )
    
    output = validate_name_copy(path)
    vampytest.assert_eq(output, (join_paths(base, path), None))


def test__validate_name__pass_joined_path():
    """
    Tests whether ``_validate_name`` is working as intended.
    
    Case: Parent is a directory.
    """
    base = 'tengu'
    path = join_paths('aya', 'ya')
    
    validate_name_copy = FunctionType(
        _validate_name.__code__,
        {
            **_validate_name.__globals__,
            'absolute_path': lambda x: join_paths(base, x),
            'is_directory': lambda x: True,
            'list_directory': lambda x: [],
        },
        _validate_name.__name__,
        _validate_name.__defaults__,
        _validate_name.__closure__,
    )
    
    output = validate_name_copy(path)
    vampytest.assert_eq(output, (join_paths(base, path), None))
