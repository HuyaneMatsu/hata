import vampytest

from ..constants import AFK_TIMEOUT_DEFAULT
from ..fields import validate_afk_timeout


def test__validate_afk_timeout__0():
    """
    Tests whether `validate_afk_timeout` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (AFK_TIMEOUT_DEFAULT, AFK_TIMEOUT_DEFAULT),
        (60, 60),
    ):
        output = validate_afk_timeout(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_afk_timeout__1():
    """
    Tests whether `validate_afk_timeout` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
        +1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_afk_timeout(input_value)


def test__validate_afk_timeout__2():
    """
    Tests whether `validate_afk_timeout` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_afk_timeout(input_value)
