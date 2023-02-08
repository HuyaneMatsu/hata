from datetime import datetime as DateTime

import vampytest

from ..fields import validate_created_at


def test__validate_created_at__0():
    """
    Tests whether ``validate_created_at`` works as intended.
    
    Case: passing.
    """
    created_at = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (created_at, created_at),
    ):
        output = validate_created_at(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_created_at__1():
    """
    Tests whether ``validate_created_at`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
        None,
    ):
        with vampytest.assert_raises(TypeError):
            validate_created_at(input_parameter)
