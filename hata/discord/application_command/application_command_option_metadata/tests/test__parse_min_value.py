import vampytest

from ..fields import parse_min_value


def test__parse_min_value():
    """
    Tests whether ``parse_min_value`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'min_value': None}, None),
        ({'min_value': 10}, 10),
        ({'min_value': 10.0}, 10.0),
    ):
        output = parse_min_value(input_data)
        vampytest.assert_eq(output, expected_output)
