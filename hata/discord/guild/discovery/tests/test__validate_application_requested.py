from datetime import datetime as DateTime

import vampytest

from ..fields import validate_application_requested


def test__validate_application_requested__0():
    """
    Tests whether ``validate_application_requested`` works as intended.
    
    Case: passing.
    """
    application_requested = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (application_requested, application_requested),
    ):
        output = validate_application_requested(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_application_requested__1():
    """
    Tests whether ``validate_application_requested`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_application_requested(input_parameter)
