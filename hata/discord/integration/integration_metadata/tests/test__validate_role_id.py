import vampytest

from ....role import Role

from ..fields import validate_role_id


def test__validate_role_id__0():
    """
    Tests whether `validate_role_id` works as intended.
    
    Case: passing.
    """
    role_id = 202210090000
    
    for input_value, expected_output in (
        (None, 0),
        (role_id, role_id),
        (Role.precreate(role_id), role_id),
        (str(role_id), role_id)
    ):
        output = validate_role_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_role_id__1():
    """
    Tests whether `validate_role_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_role_id(input_value)


def test__validate_role_id__2():
    """
    Tests whether `validate_role_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_role_id(input_value)
