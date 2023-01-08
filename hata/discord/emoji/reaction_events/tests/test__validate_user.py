import vampytest

from ....user import User

from ..fields import validate_user


def test__validate_user__0():
    """
    Tests whether ``validate_user`` works as intended.
    
    Case: Passing.
    """
    user = User.precreate(202301020012)
    
    for input_value, expected_output in (
        (user, user),
    ):
        output = validate_user(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_user__1():
    """
    Tests whether ``validate_user`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_user(input_value)
