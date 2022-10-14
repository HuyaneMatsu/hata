from datetime import datetime as DateTime

import vampytest

from ..archived_at import validate_archived_at


def test__validate_archived_at__0():
    """
    Tests whether ``validate_archived_at`` works as intended.
    
    Case: passing.
    """
    archived_at = DateTime(2016, 9, 9)
    
    for input_parameter, expected_output in (
        (None, None),
        (archived_at, archived_at),
    ):
        output = validate_archived_at(input_parameter)
        vampytest.assert_is(output, expected_output)


def test__validate_archived_at__1():
    """
    Tests whether ``validate_archived_at`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_archived_at(input_parameter)
