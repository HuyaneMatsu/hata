import vampytest

from ....user import User

from ..owner_id import validate_owner_id


def test__validate_owner_id__0():
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: passing.
    """
    user_id = 202209140022
    
    for input_value, expected_output in (
        (None, 0),
        (user_id, user_id),
        (User.precreate(user_id), user_id),
        (str(user_id), user_id)
    ):
        output = validate_owner_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_owner_id__1():
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_owner_id(input_value)


def test__validate_owner_id__2():
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_owner_id(input_value)
