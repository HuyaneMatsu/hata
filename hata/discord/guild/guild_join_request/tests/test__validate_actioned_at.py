from datetime import datetime as DateTime

import vampytest

from ..fields import validate_actioned_at


def test__validate_actioned_at__0():
    """
    Tests whether ``validate_actioned_at`` works as intended.
    
    Case: passing.
    """
    actioned_at = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (actioned_at, actioned_at),
    ):
        output = validate_actioned_at(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_actioned_at__1():
    """
    Tests whether ``validate_actioned_at`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_actioned_at(input_parameter)
