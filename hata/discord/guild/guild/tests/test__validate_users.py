import vampytest

from ....user import User

from ..fields import validate_users


def test__validate_users__0():
    """
    Tests whether ``validate_users`` works as intended.
    
    Case: passing.
    """
    user_id = 202306150007
    user_name = 'Koishi'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    for input_value, expected_output in (
        (None, {}),
        ([], {}),
        ({}, {}),
        ([user], {user_id: user}),
        ({user_id: user}, {user_id: user}),
    ):
        output = validate_users(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_users__1():
    """
    Tests whether ``validate_users`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_users(input_value)
