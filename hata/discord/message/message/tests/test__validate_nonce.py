import vampytest

from ..constants import NONCE_LENGTH_MAX
from ..fields import validate_nonce


def test__validate_nonce__0():
    """
    Tests whether `validate_nonce` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_nonce(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_nonce__1():
    """
    Tests whether `validate_nonce` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_nonce(input_value)


def test__validate_nonce__2():
    """
    Tests whether `validate_nonce` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (NONCE_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_nonce(input_value)
