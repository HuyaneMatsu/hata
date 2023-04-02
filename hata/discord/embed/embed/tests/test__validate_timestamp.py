from datetime import datetime as DateTime

import vampytest

from ..fields import validate_timestamp


def test__validate_timestamp__0():
    """
    Tests whether ``validate_timestamp`` works as intended.
    
    Case: passing.
    """
    archived_at = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (archived_at, archived_at),
    ):
        output = validate_timestamp(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_timestamp__1():
    """
    Tests whether ``validate_timestamp`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_timestamp(input_parameter)
