import vampytest

from ..fields import validate_friend_sync


def test__validate_friend_sync__0():
    """
    Tests whether `validate_friend_sync` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_friend_sync(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_friend_sync__1():
    """
    Tests whether `validate_friend_sync` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_friend_sync(input_value)
