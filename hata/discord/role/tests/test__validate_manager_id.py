import vampytest

from ..fields import validate_manager_id


def test__validate_manager_id__0():
    """
    Tests whether `validate_manager_id` works as intended.
    
    Case: passing.
    """
    manager_id = 202211010017
    
    for input_value, expected_output in (
        (manager_id, manager_id),
        (str(manager_id), manager_id)
    ):
        output = validate_manager_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_manager_id__1():
    """
    Tests whether `validate_manager_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_manager_id(input_value)


def test__validate_manager_id__2():
    """
    Tests whether `validate_manager_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_manager_id(input_value)
