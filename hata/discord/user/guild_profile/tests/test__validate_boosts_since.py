from datetime import datetime as DateTime

import vampytest

from ..fields import validate_boosts_since


def test__validate_boosts_since__0():
    """
    Tests whether ``validate_boosts_since`` works as intended.
    
    Case: passing.
    """
    boosts_since = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (boosts_since, boosts_since),
    ):
        output = validate_boosts_since(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_boosts_since__1():
    """
    Tests whether ``validate_boosts_since`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_boosts_since(input_parameter)
