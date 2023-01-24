import vampytest

from ...user import User

from ..fields import validate_user_id


def test__validate_user_id__0():
    """
    Tests whether `validate_user_id` works as intended.
    
    Case: passing.
    """
    user_id = 202301230002
    
    for input_value, expected_output in (
        (None, 0),
        (user_id, user_id),
        (User.precreate(user_id), user_id),
        (str(user_id), user_id)
    ):
        output = validate_user_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_user_id__1():
    """
    Tests whether `validate_user_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_user_id(input_value)


def test__validate_user_id__2():
    """
    Tests whether `validate_user_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_user_id(input_value)
