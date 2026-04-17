import vampytest

from ..fields import parse_launcher


def test__parse_launcher():
    """
    Tests whether ``parse_launcher`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'is_launcher': False}, False),
        ({'is_launcher': True}, True),
    ):
        output = parse_launcher(input_data)
        vampytest.assert_eq(output, expected_output)
