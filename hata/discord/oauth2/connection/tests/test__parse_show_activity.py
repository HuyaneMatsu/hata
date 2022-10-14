import vampytest

from ..fields import parse_show_activity


def test__parse_show_activity():
    """
    Tests whether ``parse_show_activity`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'show_activity': False}, False),
        ({'show_activity': True}, True),
    ):
        output = parse_show_activity(input_data)
        vampytest.assert_eq(output, expected_output)
