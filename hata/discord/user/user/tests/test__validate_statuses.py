import vampytest

from ..fields import validate_statuses


def test__validate_statuses__0():
    """
    Tests whether `validate_statuses` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ({}, None),
        ({'mobile': 'online'}, {'mobile': 'online'}),
    ):
        output = validate_statuses(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_statuses__1():
    """
    Tests whether `validate_statuses` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        {12.6: 'aya'},
        {'aya': 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_statuses(input_value)
