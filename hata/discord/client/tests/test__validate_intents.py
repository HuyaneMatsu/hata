import vampytest

from ...events import IntentFlag
from ..fields import validate_intents


def test__validate_intents__0():
    """
    Tests whether `validate_intents` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, IntentFlag(1)),
        (IntentFlag(1), IntentFlag(1)),
    ):
        output = validate_intents(input_value)
        vampytest.assert_instance(output, IntentFlag)
        vampytest.assert_eq(output, expected_output)


def test__validate_intents__1():
    """
    Tests whether `validate_intents` works as intended.
    
    Case: type error
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_intents(input_value)
