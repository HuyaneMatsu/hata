import vampytest

from .....user import User

from ..users import validate_users


def test__validate_users__0():
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: passing.
    """
    user_id_1 = 202209150002
    user_id_2 = 202209150003
    
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    for input_value, expected_output in (
        ([], []),
        ([user_id_1], [user_1]),
        ([user_1], [user_1]),
        ([user_2, user_1], [user_1, user_2]),
    ):
        output = validate_users(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_users__1():
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_users(input_value)
