import vampytest

from ..fields import parse_widget_enabled


def test__parse_widget_enabled():
    """
    Tests whether ``parse_widget_enabled`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'widget_enabled': False}, False),
        ({'widget_enabled': True}, True),
    ):
        output = parse_widget_enabled(input_data)
        vampytest.assert_eq(output, expected_output)
