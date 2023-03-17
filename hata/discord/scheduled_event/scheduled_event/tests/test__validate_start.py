from datetime import datetime as DateTime

import vampytest

from ..fields import validate_start


def test__validate_start__0():
    """
    Tests whether ``validate_start`` works as intended.
    
    Case: passing.
    """
    start = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (start, start),
    ):
        output = validate_start(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_start__1():
    """
    Tests whether ``validate_start`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_start(input_parameter)
