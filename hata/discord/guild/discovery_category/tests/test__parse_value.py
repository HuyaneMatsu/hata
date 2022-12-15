import vampytest

from ..fields import parse_value


def test__parse_value():
    """
    Tests whether ``parse_value`` works as intended.
    """
    value = 1
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': value}, value),
    ):
        output = parse_value(input_data)
        vampytest.assert_eq(output, expected_output)
