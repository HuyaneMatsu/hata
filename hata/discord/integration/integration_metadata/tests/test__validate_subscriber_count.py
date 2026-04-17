import vampytest

from ..constants import SUBSCRIBER_COUNT_DEFAULT
from ..fields import validate_subscriber_count


def test__validate_subscriber_count__0():
    """
    Tests whether ``validate_subscriber_count`` works as intended.
    
    Case: passing.
    """
    for input_parameter, expected_output in (
        (SUBSCRIBER_COUNT_DEFAULT, SUBSCRIBER_COUNT_DEFAULT),
    ):
        output = validate_subscriber_count(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_subscriber_count__1():
    """
    Tests whether ``validate_subscriber_count`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_subscriber_count(input_parameter)


def test__validate_subscriber_count__2():
    """
    Tests whether ``validate_subscriber_count`` works as intended.
    
    Case: `ValueError`.
    """
    for input_parameter in (
        -2,
    ):
        with vampytest.assert_raises(ValueError):
            validate_subscriber_count(input_parameter)
