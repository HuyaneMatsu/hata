import vampytest

from ..constants import NICK_LENGTH_MAX
from ..fields import validate_nick


def test__validate_nick__0():
    """
    Tests whether `validate_nick` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_nick(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_nick__1():
    """
    Tests whether `validate_nick` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (NICK_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_nick(input_value)


def test__validate_nick__2():
    """
    Tests whether `validate_nick` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_nick(input_value)
