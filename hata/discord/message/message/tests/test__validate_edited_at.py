from datetime import datetime as DateTime

import vampytest

from ..fields import validate_edited_at


def test__validate_edited_at__0():
    """
    Tests whether ``validate_edited_at`` works as intended.
    
    Case: passing.
    """
    edited_at = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (edited_at, edited_at),
    ):
        output = validate_edited_at(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_edited_at__1():
    """
    Tests whether ``validate_edited_at`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_edited_at(input_parameter)
