import vampytest

from ..constants import TOPIC_LENGTH_MAX
from ..fields import validate_topic


def test__validate_topic__0():
    """
    Tests whether `validate_topic` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_topic(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_topic__1():
    """
    Tests whether `validate_topic` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a' * (TOPIC_LENGTH_MAX + 1),
    ):
        with vampytest.assert_raises(ValueError):
            validate_topic(input_value)


def test__validate_topic__2():
    """
    Tests whether `validate_topic` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_topic(input_value)
