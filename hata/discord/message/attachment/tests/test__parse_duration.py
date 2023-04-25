import vampytest

from ..fields import parse_duration


def test__parse_duration():
    """
    Tests whether ``parse_duration`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0.0),
        ({'duration_sec': 1.0}, 1.0),
    ):
        output = parse_duration(input_data)
        vampytest.assert_eq(output, expected_output)
