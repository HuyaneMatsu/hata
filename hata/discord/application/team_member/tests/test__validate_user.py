import vampytest

from ....user import User

from ..fields import validate_user


def test__validate_user__0():
    """
    Tests whether `validate_user` works as intended.
    
    Case: passing.
    """
    user = User.precreate(202211230002, name = 'Ken')
    
    for input_value, expected_output in (
        (user, user),
    ):
        output = validate_user(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_user__1():
    """
    Tests whether `validate_user` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_user(input_value)
