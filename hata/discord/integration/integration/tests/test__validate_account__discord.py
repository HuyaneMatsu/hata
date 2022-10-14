import vampytest

from ....user import User

from ..fields import validate_account__discord


def test__validate_account__discord__0():
    """
    Tests whether ``validate_account__discord`` works as intended.
    
    Case: Passing.
    """
    account_id = 202210140017
    name = 'hell'
    
    user = User.precreate(account_id, name = name, bot = True)
    
    for input_value, expected_output in (
        (user, user),
    ):
        output = validate_account__discord(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_account__discord__1():
    """
    Tests whether ``validate_account__discord`` works as intended.
    
    Case: `TypeError`
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_account__discord(input_value)
