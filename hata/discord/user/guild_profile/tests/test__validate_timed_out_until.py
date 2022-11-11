from datetime import datetime as DateTime

import vampytest

from ..fields import validate_timed_out_until


def test__validate_timed_out_until__0():
    """
    Tests whether ``validate_timed_out_until`` works as intended.
    
    Case: passing.
    """
    timed_out_until = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (timed_out_until, timed_out_until),
    ):
        output = validate_timed_out_until(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_timed_out_until__1():
    """
    Tests whether ``validate_timed_out_until`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_timed_out_until(input_parameter)
