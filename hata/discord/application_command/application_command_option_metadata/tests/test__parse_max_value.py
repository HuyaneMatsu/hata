import vampytest

from ..fields import parse_max_value


def test__parse_max_value():
    """
    Tests whether ``parse_max_value`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'max_value': None}, None),
        ({'max_value': 10}, 10),
        ({'max_value': 10.0}, 10.0),
    ):
        output = parse_max_value(input_data)
        vampytest.assert_eq(output, expected_output)
