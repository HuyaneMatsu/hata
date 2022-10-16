import vampytest

from ..constants import BITRATE_DEFAULT
from ..fields import validate_bitrate


def test__validate_bitrate__0():
    """
    Validates whether ``validate_bitrate`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (BITRATE_DEFAULT, BITRATE_DEFAULT),
    ):
        output = validate_bitrate(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_bitrate__1():
    """
    Validates whether ``validate_bitrate`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_bitrate(input_value)


def test__validate_bitrate__2():
    """
    Validates whether ``validate_bitrate`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_bitrate(input_value)
