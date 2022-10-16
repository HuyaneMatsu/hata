import vampytest

from ..fields import parse_position


def test__parse_position():
    """
    Tests whether ``parse_position`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'position': 1}, 1),
    ):
        output = parse_position(input_data)
        vampytest.assert_eq(output, expected_output)
