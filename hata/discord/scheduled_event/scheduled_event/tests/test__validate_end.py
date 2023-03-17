from datetime import datetime as DateTime

import vampytest

from ..fields import validate_end


def test__validate_end__0():
    """
    Tests whether ``validate_end`` works as intended.
    
    Case: passing.
    """
    end = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (end, end),
    ):
        output = validate_end(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_end__1():
    """
    Tests whether ``validate_end`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_end(input_parameter)
