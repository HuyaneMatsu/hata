import vampytest

from ....user import User

from ..fields import validate_user


def test__validate_user__0():
    """
    Tests whether ``validate_user`` works as intended.
    
    Case: Passing.
    """
    user = User.precreate(202210280008)
    
    for input_value in (
        None,
        user,
    ):
        validate_user(input_value)


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
