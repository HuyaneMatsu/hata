import vampytest

from ....user import User

from ..fields import validate_bot_id


def test__validate_bot_id__0():
    """
    Tests whether `validate_bot_id` works as intended.
    
    Case: passing.
    """
    bot_id = 202212160002   
    
    for input_value, expected_output in (
        (None, 0),
        (bot_id, bot_id),
        (User.precreate(bot_id), bot_id),
        (str(bot_id), bot_id)
    ):
        output = validate_bot_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_bot_id__1():
    """
    Tests whether `validate_bot_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_bot_id(input_value)


def test__validate_bot_id__2():
    """
    Tests whether `validate_bot_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_bot_id(input_value)
