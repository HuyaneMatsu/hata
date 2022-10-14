import vampytest

from ....user import User, ZEROUSER

from ..fields import validate_bot


def test__validate_bot__0():
    """
    Tests whether `validate_bot` works as intended.
    
    Case: passing.
    """
    user = User.precreate(202210080011, name = 'Ken', bot = True)
    
    for input_value, expected_output in (
        (None, ZEROUSER),
        (ZEROUSER, ZEROUSER),
        (user, user),
    ):
        output = validate_bot(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_bot__1():
    """
    Tests whether `validate_bot` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_bot(input_value)
