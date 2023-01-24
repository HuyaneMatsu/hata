from datetime import datetime as DateTime

import vampytest

from ..fields import validate_requested_to_speak_at


def test__validate_requested_to_speak_at__0():
    """
    Tests whether ``validate_requested_to_speak_at`` works as intended.
    
    Case: passing.
    """
    requested_to_speak_at = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (requested_to_speak_at, requested_to_speak_at),
    ):
        output = validate_requested_to_speak_at(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_requested_to_speak_at__1():
    """
    Tests whether ``validate_requested_to_speak_at`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_requested_to_speak_at(input_parameter)
